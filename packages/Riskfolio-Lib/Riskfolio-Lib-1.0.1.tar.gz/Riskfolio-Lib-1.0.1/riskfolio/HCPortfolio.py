""""""  #
"""
Copyright (c) 2020-2021, Dany Cajas
All rights reserved.
This work is licensed under BSD 3-Clause "New" or "Revised" License.
License available at https://github.com/dcajasn/Riskfolio-Lib/blob/master/LICENSE.txt
"""

import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hr
from scipy.spatial.distance import squareform
import riskfolio.RiskFunctions as rk
import riskfolio.AuxFunctions as af
import riskfolio.ParamsEstimation as pe
import riskfolio.DBHT as db


class HCPortfolio(object):
    r"""
    Class that creates a portfolio object with all properties needed to
    calculate optimal portfolios.

    Parameters
    ----------
    returns : DataFrame, optional
        A dataframe that containts the returns of the assets.
        The default is None.
    alpha : float, optional
        Significance level of CVaR, EVaR, CDaR and EDaR. The default is 0.05.
    w_max : Series, optional
        Upper bound constraint for hierarchical risk parity weights :cite:`c-Pfitzinger`.
    w_min : Series, optional
        Lower bound constraint for hierarchical risk parity weights :cite:`c-Pfitzinger`.
    """

    def __init__(self, returns=None, alpha=0.05, w_max=None, w_min=None):
        self._returns = returns
        self.alpha = alpha
        self.asset_order = None
        self.clusters = None
        self.cov = None
        self.codep = None
        self.codep_sorted = None
        self.w_max = w_max
        self.w_min = w_min

    @property
    def returns(self):
        if self._returns is not None and isinstance(self._returns, pd.DataFrame):
            return self._returns
        else:
            raise NameError("returns must be a DataFrame")

    @returns.setter
    def returns(self, value):
        if value is not None and isinstance(value, pd.DataFrame):
            self._returns = value
        else:
            raise NameError("returns must be a DataFrame")

    @property
    def assetslist(self):
        if self._returns is not None and isinstance(self._returns, pd.DataFrame):
            return self._returns.columns.tolist()

    # get naive-risk weights
    def _naive_risk(self, returns, cov, rm="MV", rf=0):
        assets = returns.columns.tolist()
        n = len(assets)

        if rm == "equal":
            weight = np.ones((n, 1)) * 1 / n
        else:
            inv_risk = np.zeros((n, 1))
            for i in assets:
                k = assets.index(i)
                w = np.zeros((n, 1))
                w[k, 0] = 1
                w = pd.DataFrame(w, columns=["weights"], index=assets)
                if rm == "vol":
                    risk = rk.Sharpe_Risk(
                        w, cov=cov, returns=returns, rm="MV", rf=rf, alpha=self.alpha
                    )
                else:
                    risk = rk.Sharpe_Risk(
                        w, cov=cov, returns=returns, rm=rm, rf=rf, alpha=self.alpha
                    )
                inv_risk[k, 0] = risk

            if rm == "MV":
                inv_risk = 1 / np.power(inv_risk, 2)
            else:
                inv_risk = 1 / inv_risk
            weight = inv_risk * (1 / np.sum(inv_risk))

        weight = weight.reshape(-1, 1)

        return weight

    # Create hierarchical clustering
    def _hierarchical_clustering(
        self,
        model="HRP",
        linkage="ward",
        codependence="pearson",
        max_k=10,
        leaf_order=True,
    ):

        # Calculating distance
        if codependence in {"pearson", "spearman"}:
            dist = np.sqrt(np.clip((1 - self.codep) / 2, a_min=0.0, a_max=1.0))
        elif codependence in {"abs_pearson", "abs_spearman", "distance"}:
            dist = np.sqrt(np.clip((1 - self.codep), a_min=0.0, a_max=1.0))
        elif codependence in {"mutual_info"}:
            dist = af.var_info_matrix(self.returns).astype(float)
        elif codependence in {"tail"}:
            dist = -np.log(af.ltdi_matrix(self.returns, alpha=self.alpha).astype(float))

        # Hierarchcial clustering
        dist = dist.to_numpy()
        dist = pd.DataFrame(dist, columns=self.codep.columns, index=self.codep.index)
        if linkage == "DBHT":
            # different choices for D, S give different outputs!
            D = dist.to_numpy()  # dissimilatity matrix
            if codependence in {"pearson", "spearman"}:
                codep = 1 - dist ** 2
                S = codep.to_numpy()  # similarity matrix
            else:
                S = self.codep.to_numpy()  # similarity matrix
            (_, _, _, _, _, clustering) = db.DBHTs(
                D, S, leaf_order=leaf_order
            )  # DBHT clustering
        else:
            p_dist = squareform(dist, checks=False)
            clustering = hr.linkage(p_dist, method=linkage, optimal_ordering=leaf_order)

        if model in ["HERC", "HERC2"]:
            # optimal number of clusters
            k = af.two_diff_gap_stat(self.codep, dist, clustering, max_k)
        else:
            k = None

        return clustering, k

    # sort clustered items by distance
    def _seriation(self, clusters):
        return hr.leaves_list(clusters)

    # compute HRP weight allocation through recursive bisection
    def _recursive_bisection(self, sort_order, rm="MV", rf=0):

        if isinstance(self.w_max, pd.Series) and isinstance(self.w_min, pd.Series):
            if (self.w_max.all() >= self.w_min.all()).item():
                flag = True
            else:
                raise NameError("All upper bounds must be higher than lower bounds")
        else:
            flag = False

        weight = pd.Series(1, index=sort_order)  # set initial weights to 1
        items = [sort_order]

        while len(items) > 0:  # loop while weights is under 100%
            items = [
                i[j:k]
                for i in items
                for j, k in (
                    (0, len(i) // 2),
                    (len(i) // 2, len(i)),
                )  # get cluster indi
                if len(i) > 1
            ]

            # allocate weight to left and right cluster
            for i in range(0, len(items), 2):
                left_cluster = items[i]
                right_cluster = items[i + 1]

                # Left cluster
                left_cov = self.cov.iloc[left_cluster, left_cluster]
                left_returns = self.returns.iloc[:, left_cluster]
                left_weight = self._naive_risk(left_returns, left_cov, rm=rm, rf=rf)

                if rm == "vol":
                    left_risk = rk.Sharpe_Risk(
                        left_weight,
                        cov=left_cov,
                        returns=left_returns,
                        rm="MV",
                        rf=rf,
                        alpha=self.alpha,
                    )
                else:
                    left_risk = rk.Sharpe_Risk(
                        left_weight,
                        cov=left_cov,
                        returns=left_returns,
                        rm=rm,
                        rf=rf,
                        alpha=self.alpha,
                    )
                    if rm == "MV":
                        left_risk = np.power(left_risk, 2)

                # Right cluster
                right_cov = self.cov.iloc[right_cluster, right_cluster]
                right_returns = self.returns.iloc[:, right_cluster]
                right_weight = self._naive_risk(right_returns, right_cov, rm=rm, rf=rf)

                if rm == "vol":
                    right_risk = rk.Sharpe_Risk(
                        right_weight,
                        cov=right_cov,
                        returns=right_returns,
                        rm="MV",
                        rf=rf,
                        alpha=self.alpha,
                    )
                else:
                    right_risk = rk.Sharpe_Risk(
                        right_weight,
                        cov=right_cov,
                        returns=right_returns,
                        rm=rm,
                        rf=rf,
                        alpha=self.alpha,
                    )
                    if rm == "MV":
                        right_risk = np.power(right_risk, 2)

                # Allocate weight to clusters
                alpha_1 = 1 - left_risk / (left_risk + right_risk)

                # Weights constraints
                if flag:
                    a1 = np.sum(self.w_max[left_cluster]) / weight[left_cluster[0]]
                    a2 = np.max(
                        [
                            np.sum(self.w_min[left_cluster]) / weight[left_cluster[0]],
                            alpha_1,
                        ]
                    )
                    alpha_1 = np.min([a1, a2])
                    a1 = np.sum(self.w_max[right_cluster]) / weight[right_cluster[0]]
                    a2 = np.max(
                        [
                            np.sum(self.w_min[right_cluster])
                            / weight[right_cluster[0]],
                            1 - alpha_1,
                        ]
                    )
                    alpha_1 = 1 - np.min([a1, a2])

                weight[left_cluster] *= alpha_1  # weight 1
                weight[right_cluster] *= 1 - alpha_1  # weight 2

        weight.index = self.asset_order

        return weight

    # compute HRP weight allocation through cluster-based bisection
    def _hierarchical_recursive_bisection(
        self, Z, rm="MV", rf=0, linkage="ward", model="HERC"
    ):

        # Transform linkage to tree and reverse order
        root, nodes = hr.to_tree(Z, rd=True)
        nodes = np.array(nodes)
        nodes_1 = np.array([i.dist for i in nodes])
        idx = np.argsort(nodes_1)
        nodes = nodes[idx][::-1].tolist()

        weight = pd.Series(1, index=self.cov.index)  # Set initial weights to 1

        clustering_inds = hr.fcluster(Z, self.k, criterion="maxclust")
        clusters = {
            i: [] for i in range(min(clustering_inds), max(clustering_inds) + 1)
        }
        for i, v in enumerate(clustering_inds):
            clusters[v].append(i)

        # Loop through k clusters
        for i in nodes[: self.k - 1]:
            if i.is_leaf() == False:  # skip leaf-nodes
                left = i.get_left().pre_order()  # lambda i: i.id) # get left cluster
                right = i.get_right().pre_order()  # lambda i: i.id) # get right cluster
                left_set = set(left)
                right_set = set(right)
                left_risk = 0
                right_risk = 0

                # Allocate weight to clusters
                if rm == "equal":
                    alpha_1 = 0.5

                else:
                    for j in clusters.keys():
                        if set(clusters[j]).issubset(left_set):
                            # Left cluster
                            left_cov = self.cov.iloc[clusters[j], clusters[j]]
                            left_returns = self.returns.iloc[:, clusters[j]]
                            left_weight = self._naive_risk(
                                left_returns, left_cov, rm=rm, rf=rf
                            )

                            if rm == "vol":
                                left_risk_ = rk.Sharpe_Risk(
                                    left_weight,
                                    cov=left_cov,
                                    returns=left_returns,
                                    rm="MV",
                                    rf=rf,
                                    alpha=self.alpha,
                                )
                            else:
                                left_risk_ = rk.Sharpe_Risk(
                                    left_weight,
                                    cov=left_cov,
                                    returns=left_returns,
                                    rm=rm,
                                    rf=rf,
                                    alpha=self.alpha,
                                )
                                if rm == "MV":
                                    left_risk_ = np.power(left_risk_, 2)

                            left_risk += left_risk_

                        elif set(clusters[j]).issubset(right_set):
                            # Right cluster
                            right_cov = self.cov.iloc[clusters[j], clusters[j]]
                            right_returns = self.returns.iloc[:, clusters[j]]
                            right_weight = self._naive_risk(
                                right_returns, right_cov, rm=rm, rf=rf
                            )

                            if rm == "vol":
                                right_risk_ = rk.Sharpe_Risk(
                                    right_weight,
                                    cov=right_cov,
                                    returns=right_returns,
                                    rm="MV",
                                    rf=rf,
                                    alpha=self.alpha,
                                )
                            else:
                                right_risk_ = rk.Sharpe_Risk(
                                    right_weight,
                                    cov=right_cov,
                                    returns=right_returns,
                                    rm=rm,
                                    rf=rf,
                                    alpha=self.alpha,
                                )
                                if rm == "MV":
                                    right_risk_ = np.power(right_risk_, 2)

                            right_risk += right_risk_

                    alpha_1 = 1 - left_risk / (left_risk + right_risk)

                weight[left] *= alpha_1  # weight 1
                weight[right] *= 1 - alpha_1  # weight 2

        # Get constituents of k clusters
        clustered_assets = pd.Series(
            hr.cut_tree(Z, n_clusters=self.k).flatten(), index=self.cov.index
        )

        # Multiply within-cluster weight with inter-cluster weight
        for i in range(self.k):
            cluster = clustered_assets.loc[clustered_assets == i]
            cluster_cov = self.cov.loc[cluster.index, cluster.index]
            cluster_returns = self.returns.loc[:, cluster.index]
            if model == "HERC":
                cluster_weights = pd.Series(
                    self._naive_risk(
                        cluster_returns, cluster_cov, rm=rm, rf=rf
                    ).flatten(),
                    index=cluster_cov.index,
                )
            elif model == "HERC2":
                cluster_weights = pd.Series(
                    self._naive_risk(
                        cluster_returns, cluster_cov, rm="equal", rf=rf
                    ).flatten(),
                    index=cluster_cov.index,
                )
            weight.loc[cluster_weights.index] *= cluster_weights

        return weight

    # Allocate weights
    def optimization(
        self,
        model="HRP",
        codependence="pearson",
        covariance="hist",
        rm="MV",
        rf=0,
        linkage="single",
        k=None,
        max_k=10,
        alpha_tail=0.05,
        leaf_order=True,
        d=0.94,
    ):
        r"""
        This method calculates the optimal portfolio according to the
        optimization model selected by the user.

        Parameters
        ----------
        model : str, can be {'HRP', 'HERC' or 'HERC2'}
            The hierarchical cluster portfolio model used for optimize the
            portfolio. The default is 'HRP'. Posible values are:

            - 'HRP': Hierarchical Risk Parity.
            - 'HERC': Hierarchical Equal Risk Contribution.
            - 'HERC2': HERC but splitting weights equally within clusters.

        codependence : str, can be {'pearson', 'spearman', 'abs_pearson', 'abs_spearman', 'distance', 'mutual_info' or 'tail'}
            The codependence or similarity matrix used to build the distance
            metric and clusters. The default is 'pearson'. Posible values are:

            - 'pearson': pearson correlation matrix. Distance formula: :math:`D_{i,j} = \sqrt{0.5(1-\rho^{pearson}_{i,j})}`.
            - 'spearman': spearman correlation matrix. Distance formula: :math:`D_{i,j} = \sqrt{0.5(1-\rho^{spearman}_{i,j})}`.
            - 'abs_pearson': absolute value pearson correlation matrix. Distance formula: :math:`D_{i,j} = \sqrt{(1-|\rho^{pearson}_{i,j}|)}`.
            - 'abs_spearman': absolute value spearman correlation matrix. Distance formula: :math:`D_{i,j} = \sqrt{(1-|\rho^{spearman}_{i,j}|)}`.
            - 'distance': distance correlation matrix. Distance formula :math:`D_{i,j} = \sqrt{(1-\rho^{distance}_{i,j})}`.
            - 'mutual_info': mutual information matrix. Distance used is variation information matrix.
            - 'tail': lower tail dependence index matrix. Dissimilarity formula :math:`D_{i,j} = -\log{\lambda_{i,j}}`.

        covariance : str, can be {'hist', 'ewma1', 'ewma2', 'ledoit', 'oas' or 'shrunk'}
            The method used to estimate the covariance matrix:
            The default is 'hist'.

            - 'hist': use historical estimates.
            - 'ewma1'': use ewma with adjust=True, see `EWM <https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows>`_ for more details.
            - 'ewma2': use ewma with adjust=False, see `EWM <https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows>`_ for more details.
            - 'ledoit': use the Ledoit and Wolf Shrinkage method.
            - 'oas': use the Oracle Approximation Shrinkage method.
            - 'shrunk': use the basic Shrunk Covariance method.

        rm : str, optional
            The risk measure used to optimze the portfolio.
            The default is 'MV'. Posible values are:

            - 'equal': Equally weighted.
            - 'vol': Standard Deviation.
            - 'MV': Variance.
            - 'MAD': Mean Absolute Deviation.
            - 'MSV': Semi Standard Deviation.
            - 'FLPM': First Lower Partial Moment (Omega Ratio).
            - 'SLPM': Second Lower Partial Moment (Sortino Ratio).
            - 'VaR': Value at Risk.
            - 'CVaR': Conditional Value at Risk.
            - 'EVaR': Entropic Value at Risk.
            - 'WR': Worst Realization (Minimax)
            - 'MDD': Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
            - 'ADD': Average Drawdown of uncompounded cumulative returns.
            - 'DaR': Drawdown at Risk of uncompounded cumulative returns.
            - 'CDaR': Conditional Drawdown at Risk of uncompounded cumulative returns.
            - 'EDaR': Entropic Drawdown at Risk of uncompounded cumulative returns.
            - 'UCI': Ulcer Index of uncompounded cumulative returns.
            - 'MDD_Rel': Maximum Drawdown of compounded cumulative returns (Calmar Ratio).
            - 'ADD_Rel': Average Drawdown of compounded cumulative returns.
            - 'DaR_Rel': Drawdown at Risk of compounded cumulative returns.
            - 'CDaR_Rel': Conditional Drawdown at Risk of compounded cumulative returns.
            - 'EDaR_Rel': Entropic Drawdown at Risk of compounded cumulative returns.
            - 'UCI_Rel': Ulcer Index of compounded cumulative returns.

        rf : float, optional
            Risk free rate, must be in the same period of assets returns.
            The default is 0.
        linkage : string, optional
            Linkage method of hierarchical clustering, see `linkage <https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html?highlight=linkage#scipy.cluster.hierarchy.linkage>`_ for more details.
            The default is 'single'. Posible values are:

            - 'single'.
            - 'complete'.
            - 'average'.
            - 'weighted'.
            - 'centroid'.
            - 'median'.
            - 'ward'.
            - 'DBHT': Direct Bubble Hierarchical Tree.

        k : int, optional
            Number of clusters. This value is took instead of the optimal number
            of clusters calculated with the two difference gap statistic.
            The default is None.
        max_k : int, optional
            Max number of clusters used by the two difference gap statistic
            to find the optimal number of clusters. The default is 10.
        alpha_tail : float, optional
            Significance level for lower tail dependence index. The default is 0.05.
        leaf_order : bool, optional
            Indicates if the cluster are ordered so that the distance between
            successive leaves is minimal. The default is True.
        d : scalar
            The smoothing factor of ewma methods.
            The default is 0.94.

        Returns
        -------
        w : DataFrame
            The weights of optimal portfolio.

        """

        # Covariance matrix
        self.cov = pe.covar_matrix(self.returns, method=covariance, d=0.94)

        # Codependence matrix
        if codependence in {"pearson", "spearman"}:
            self.codep = self.returns.corr(method=codependence).astype(float)
        elif codependence in {"abs_pearson", "abs_spearman"}:
            self.codep = np.abs(self.returns.corr(method=codependence[4:])).astype(
                float
            )
        elif codependence in {"distance"}:
            self.codep = af.dcorr_matrix(self.returns).astype(float)
        elif codependence in {"mutual_info"}:
            self.codep = af.mutual_info_matrix(self.returns).astype(float)
        elif codependence in {"tail"}:
            self.codep = af.ltdi_matrix(self.returns, alpha=self.alpha).astype(float)

        # Step-1: Tree clustering
        self.clusters, self.k = self._hierarchical_clustering(
            model, linkage, codependence, max_k, leaf_order=leaf_order
        )
        if k is not None:
            self.k = int(k)

        # Step-2: Seriation (Quasi-Diagnalization)
        self.sort_order = self._seriation(self.clusters)
        asset_order = self.assetslist
        asset_order[:] = [self.assetslist[i] for i in self.sort_order]
        self.asset_order = asset_order.copy()
        self.codep_sorted = self.codep.reindex(
            index=self.asset_order, columns=self.asset_order
        )

        if isinstance(self.w_max, pd.Series) and isinstance(self.w_min, pd.Series):
            self.w_max = self.w_max.reindex(index=self.asset_order)
            self.w_max.index = self.sort_order
            self.w_min = self.w_min.reindex(index=self.asset_order)
            self.w_min.index = self.sort_order

        # Step-3: Recursive bisection
        if model == "HRP":
            weights = self._recursive_bisection(self.sort_order, rm=rm, rf=rf)
        elif model in ["HERC", "HERC2"]:
            weights = self._hierarchical_recursive_bisection(
                self.clusters, rm=rm, rf=rf, linkage=linkage, model=model
            )

        if isinstance(self.w_max, pd.Series) and isinstance(self.w_min, pd.Series):
            self.w_max = self.w_max.sort_index()
            self.w_max.index = self.assetslist
            self.w_min = self.w_min.sort_index()
            self.w_max.index = self.assetslist

        weights = weights.loc[self.assetslist].to_frame()
        weights.columns = ["weights"]

        return weights
