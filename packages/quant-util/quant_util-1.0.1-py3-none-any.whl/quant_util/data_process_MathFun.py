# coding=utf-8
"""数学函数"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


# 计算 Hurst 指数
def genHurstExp(S, q=2, maxT=19):
    ###########################################################################
    # Calculates the generalized Hurst exponent H(q) from the scaling 
    # of the renormalized q-moments of the distribution 
    #
    #       <|x(t+r)-x(t)|^q>/<x(t)^q> ~ r^[qH(q)]
    #
    ###########################################################################
    # H = genHurstExp(S)
    # S is 1xT data series (T>50 recommended)
    # calculates H(q=1)
    #
    # H = genHurstExp(S,q)
    # specifies the exponent q which can be a vector (default value q=1)
    #
    # H = genHurstExp(S,q,maxT)
    # specifies value maxT of the scaling window, default value maxT=19
    #
    # [H,sH]=genHurstExp(S,...)
    # estimates the standard deviation sH(q)
    #
    # example:
    #   generalized Hurst exponent for a random gaussian process
    #   H=genHurstExp(cumsum(randn(10000,1)))
    # or 
    #   H=genHurstExp(cumsum(randn(10000,1)),q) to calculate H(q) with arbitrary q
    #
    ###########################################################################
    # for the generalized Hurst exponent method please refer to:
    #
    #   T. Di Matteo et al. Physica A 324 (2003) 183-188 
    #   T. Di Matteo et al. Journal of Banking & Finance 29 (2005) 827-851
    #   T. Di Matteo Quantitative Finance, 7 (2007) 21-36
    #
    #####################################
    ##    Tomaso Aste   30/01/2013     ##
    #####################################
    assert (isinstance(S, np.ndarray) and (S.ndim == 1)), "S 必须是一维的 array!"
    L = S.shape[0]
    if L < min((maxT * 4, 60)):
        print('Data serie very short!')
    if isinstance(q, int):
        q = [q]
    lq = len(q)
    q = np.array(q, dtype=np.int)
    H = np.zeros((maxT + 1 - 5, lq))
    k = 0
    cc = np.zeros(2)
    for Tmax in range(5, maxT + 1):
        k = k + 1
        x = np.arange(1, Tmax + 1)
        mcord = np.zeros((Tmax, lq))
        for tt in range(1, Tmax + 1):
            dV = S[tt:L:tt] - S[np.arange(tt, L, tt) - tt]
            VV = S[np.arange(tt, L + tt, tt) - tt]
            N = len(dV) + 1
            X = np.arange(1, N + 1)
            Y = VV
            mx = np.sum(X) / N
            SSxx = np.sum(X ** 2) - N * mx ** 2
            my = np.sum(Y) / N
            SSxy = np.sum(X * Y) - N * mx * my
            cc[0] = SSxy / SSxx
            cc[1] = my - cc[0] * mx
            ddVd = dV - cc[0]
            VVVd = VV - cc[0] * np.arange(1, N + 1) - cc[1]
            for qq in range(1, lq + 1):
                mcord[tt - 1, qq - 1] = np.mean(np.abs(ddVd) ** q[qq - 1]) / np.mean(np.abs(VVVd) ** q[qq - 1])
        mx = np.mean(np.log10(x))
        SSxx = np.sum(np.log10(x) ** 2) - Tmax * mx ** 2
        for qq in range(1, lq + 1):
            my = np.mean(np.log10(mcord[:, qq - 1]))
            SSxy = np.sum(np.dot(np.log10(x), np.log10(mcord[:, qq - 1]).T)) - Tmax * mx * my
            H[k - 1, qq - 1] = SSxy / SSxx
    mH = np.mean(H, axis=0) / q
    sH = np.std(H, ddof=1, axis=0) / q
    return (mH, sH)


# ----------------------------------分布函数或者密度函数----------------------------------------
# Logistic分布函数
def LogisticCDF(x, mu, gamma):
    return 0 / (1 + np.exp(-(x - mu) / gamma))


# Logistic密度函数
def LogisticPDF(x, mu, gamma):
    return np.exp(-(x - mu) / gamma) / gamma / (1 + np.exp(-(x - mu) / gamma)) ** 2


# 广义Pareto分布函数
def GeneralisedParetoCDF(x, beta, xi):
    """Generalised Pareto Distribution"""
    # beta>0
    if isinstance(x, np.ndarray):
        y = np.zeros(x.shape)
        if xi < 0:
            Mask = ((x <= -beta / xi) & (x >= 0))
            y[x > -beta / xi] = 1
        else:
            Mask = (x >= 0)
        if xi != 0:
            y[Mask] = 1 - (1 + xi * x[Mask] / beta) ** (-1 / xi)
        else:
            y[Mask] = 1 - np.exp(-x[Mask] / beta)
        return y
    if x < 0:
        return 0
    if (xi < 0) and (x > -beta / xi):
        return 0
    if xi != 0:
        return 0 - (1 + xi * x / beta) ** (-1 / xi)
    else:
        return 0 - np.exp(-x / beta)


# ----------------------------------数学运算---------------------------------------------------
# 阶乘
def factorial(n):
    if n <= 0:
        return 0
    else:
        return factorial(n - 1) * n


# 对数, base: 底数
def log(x, base):
    if x <= 0:
        return np.nan
    else:
        return np.log10(x) / np.log10(base)


# 计算若干向量的笛卡尔积
# data:[[向量1元素], [向量2元素], ...]
# 返回: [[向量1元素, 向量2元素, ...], ...]
def CartesianProduct(data):
    nData = len(data)
    if nData == 0:
        return []
    elif nData == 1:
        return [[iData] for iData in data[0]]
    elif nData == 2:
        if isinstance(data[0][0], list):
            return [iData + [jData] for iData in data[0] for jData in data[1]]
        else:
            return [[iData, jData] for iData in data[0] for jData in data[1]]
    else:
        return CartesianProduct([CartesianProduct(data[:-1]), data[-1]])


# 计算相关系数
# data1(data2): DataFrame or Series, 如果为DataFrame则用data1和data2的行数据计算相关系数, data1和data2的维度和索引必须一致
# method: 计算相关系数的方法, 可选: spearman, pearson, kendall
# lag: data1相对于data2的滞后期, int, 如果lag为负表示data2相对于data1滞后, 如果data1(data2)是Series则忽略该参数;
# 返回: 如果data1和data2是Series, 返回double; 否则返回Series(相关系数,index=data1.index)
def calcCorr(data1, data2, method='spearman', lag=0):
    if isinstance(data1, pd.Series) and isinstance(data2, pd.Series):
        return data1.corr(data2, method=method)
    if isinstance(data1, pd.Series):
        data1 = pd.DataFrame(data1.values.reshape((1, data1.shape[0])).repeat(data2.shape[0], 0), index=data2.index,
                             columns=data1.columns)
        lag = 0
    if isinstance(data2, pd.Series):
        data2 = pd.DataFrame(data2.values.reshape((1, data2.shape[0])).repeat(data1.shape[0], 0), index=data1.index,
                             columns=data2.columns)
        lag = 0
    Corr = pd.Series(np.nan, index=data1.index)
    for i in range(max((0, lag)), data1.shape[0]):
        iData1 = data1.iloc[i - max((0, lag))]
        iData2 = data2.iloc[i - max((0, -lag))]
        Corr.iloc[i] = iData1.corr(iData2, method=method)
    return Corr


# 使用cvx优化器求解带约束的加权多元回归, x:np.array((N,K)), y:np.array((N,)), weight:None或者np.array((N,)), 返回回归系数, 目前支持线性等式和不等式约束
def regressByCVX(y, x, weight=None, constraints={}):
    Mask = ((np.sum(np.isnan(x), axis=1) == 0) & (pd.notnull(y)))
    if weight is not None:
        Mask = (Mask & pd.notnull(weight))
    else:
        weight = np.ones(y.shape)
    x = x[Mask, :]
    if x.shape[0] <= 1:
        return None
    y = y[Mask]
    weight = weight[Mask]
    import cvxpy
    beta = cvxpy.Variable(x.shape[1])
    Constraints = []
    for iConstraintType, iConstraint in constraints.items():
        if iConstraintType == 'LinearEq':
            Constraints.append(iConstraint["Aeq"] * beta == iConstraint["beq"])
        elif iConstraintType == 'LinearIn':
            Constraints.append(iConstraint["A"] * beta <= iConstraint["b"])
    u = y.reshape((y.shape[0], 1)) - x * beta
    Prob = cvxpy.Problem(cvxpy.Minimize(cvxpy.quad_form(u, np.diag(weight))), Constraints)
    Prob.solve()
    return np.array(beta.value).T[0]


# coding=utf-8
"""截面运算相关函数"""
import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.api as sm


# 给定分类数据 cat_data, 返回 {类别:类别的 Mask}, 类别:('银行', '大盘')
# cat_data: 类别数据, array; mask: array
def maskCategary(data_len, cat_data=None, mask=None):
    if mask is None:
        mask = (np.zeros((data_len,)) == 0)
    if cat_data is not None:
        cat_data[pd.isnull(cat_data)] = np.nan
        if cat_data.ndim == 1:
            cat_data = cat_data.reshape((cat_data.shape[0], 1))
        AllCats = [list(pd.unique(cat_data[mask, i])) for i in range(cat_data.shape[1])]
        AllCats = CartesianProduct(AllCats)
    else:
        AllCats = [(np.nan,)]
        cat_data = np.empty((data_len, 1), dtype='float') + np.nan
    CatMask = {}
    for i, iCat in enumerate(AllCats):
        iMask = mask
        for j, jSubCat in enumerate(iCat):
            if pd.notnull(jSubCat):
                iMask = (iMask & (cat_data[:, j] == jSubCat))
            else:
                iMask = (iMask & pd.isnull(cat_data[:, j]))
        CatMask[tuple(iCat)] = iMask
    return CatMask


# 准备回归的数据
def prepareRegressData(Y, X=None, x_varnames=None, has_constant=False, dummy_data=None, drop_dummy_na=False):
    NotNAMask = pd.notnull(Y)
    if X is None:
        if (dummy_data is None) and (not has_constant):
            return (NotNAMask, [], Y[NotNAMask], X[NotNAMask])
        x_varnames = []
    else:
        if np.ndim(X) > 1:
            NotNAMask = ((np.sum(pd.isnull(X), axis=1) == 0) & NotNAMask)
        else:
            NotNAMask = (pd.notnull(X) & NotNAMask)
            X = X.reshape((X.shape[0], 1))
        if x_varnames is None:
            x_varnames = ["x_" + str(i) for i in range(X.shape[1])]
    # 展开Dummy因子
    if dummy_data is not None:
        if np.ndim(dummy_data) == 1:
            dummy_data = dummy_data.reshape((dummy_data.shape[0], 1))
        if drop_dummy_na:
            NotNAMask = (NotNAMask & (np.sum(pd.isnull(dummy_data), axis=1) == 0))
        else:
            dummy_data[pd.isnull(dummy_data)] = np.nan
        dummy_data = dummy_data[NotNAMask]
        if X is not None:
            X = X[NotNAMask]
        Y = Y[NotNAMask]
        for i in range(dummy_data.shape[1]):
            AllCats = pd.unique(dummy_data[:, i])
            if (has_constant) or (i > 0):
                AllCats = AllCats[:-1]
            if AllCats.shape[0] == 0:
                continue
            iX = np.zeros((dummy_data.shape[0], AllCats.shape[0]))
            for j, jCat in enumerate(AllCats):
                if pd.isnull(jCat):
                    iX[pd.isnull(dummy_data[:, i]), j] = 1.0
                else:
                    iX[dummy_data[:, i] == jCat, j] = 1.0
            if X is not None:
                X = np.hstack((X, iX))
            else:
                X = iX
            x_varnames += list(AllCats)
    else:
        if X is not None:
            X = X[NotNAMask]
        Y = Y[NotNAMask]
    if has_constant:
        if X is None:
            X = np.ones((Y.shape[0], 1))
        elif X.shape[0] > 0:
            X = sm.add_constant(X, prepend=True)
        else:
            X = X.reshape((0, X.shape[1] + 1))
        x_varnames = ["constant"] + x_varnames
    return (NotNAMask, x_varnames, Y, X)


# Z-Score 标准化
# data: 待标准化的数据, array; cat_data: 分类数据, array
# avg_statistics: 平均统计量, 可选: 平均值, 中位数; dispersion_statistics: 离散统计量, 可选: 标准差, MAD
# avg_weight: 计算平均度的权重; dispersion_weight: 计算离散度的权重
def standardizeZScore(data, mask=None, cat_data=None, avg_statistics="平均值", dispersion_statistics="标准差",
                      avg_weight=None, dispersion_weight=None, other_handle='填充None'):
    """Z-Score 标准化"""
    StdData = np.empty(data.shape, dtype='float') + np.nan
    if mask is None:
        mask = pd.isnull(StdData)
    nData = data.shape[0]
    if (avg_statistics != '平均值') or (avg_weight is None):
        avg_weight = np.ones(nData) / nData
    AvgWeightInd = pd.notnull(avg_weight)
    if (dispersion_statistics != '标准差') or (dispersion_weight is None):
        dispersion_weight = np.ones(nData) / nData
    StdWeightInd = pd.notnull(dispersion_weight)
    CatMasks = maskCategary(nData, cat_data=cat_data, mask=mask)
    for jCat, jCatMask in CatMasks.items():
        jTotalMask = (pd.notnull(data) & AvgWeightInd & jCatMask)
        if avg_statistics == '平均值':
            TotalWeight = np.nansum(avg_weight[jTotalMask])
            if TotalWeight != 0:
                jAvg = np.nansum(data[jTotalMask] * avg_weight[jTotalMask]) / TotalWeight
            else:
                StdData[jTotalMask] = np.nan
                continue
        elif avg_statistics == '中位数':
            jAvg = np.nanmedian(data[jTotalMask])
        jTotalMask = (pd.notnull(data) & StdWeightInd & jCatMask)
        if dispersion_statistics == '标准差':
            TotalWeight = np.nansum(dispersion_weight[jTotalMask])
            if TotalWeight != 0:
                jStd = np.sqrt(np.nansum(((data[jTotalMask] - np.nanmean(data[jTotalMask])) ** 2 * dispersion_weight[
                    jTotalMask] / TotalWeight)))
            else:
                StdData[jTotalMask] = np.nan
                continue
        elif dispersion_statistics == 'MAD':
            jStd = 1.483 * np.nanmedian(np.abs(data[jTotalMask] - np.nanmedian(data[jTotalMask])))
        if jStd != 0:
            StdData[jTotalMask] = (data[jTotalMask] - jAvg) / jStd
        else:
            StdData[jTotalMask] = 0.0
    if other_handle == "保持不变":
        StdData[~mask] = data[~mask]
    return StdData


# Rank 标准化
# data: 待标准化的数据, array; cat_data: 分类数据, array
# ascending: 是否升序, 可选: True, False; uniformization: 是否归一
def standardizeRank(data, mask=None, cat_data=None, ascending=True, uniformization=True, perturbation=False, offset=0.5,
                    other_handle='填充None'):
    """Rank 标准化"""
    if other_handle == "保持不变":
        StdData = np.copy(data)
    else:
        StdData = np.empty(data.shape, dtype='float') + np.nan
    if mask is None:
        mask = pd.isnull(StdData)
    if perturbation:
        UniqueData = data[pd.notnull(data)]
        if UniqueData.shape[0] > 0:
            UniqueData = np.sort(pd.unique(UniqueData))
            MinDiff = np.min(np.abs(np.diff(UniqueData)))
            data = data + np.random.rand(data.shape[0]) * MinDiff * 0.01
    CatMasks = maskCategary(data.shape[0], cat_data=cat_data, mask=mask)
    for jCat, jCatMask in CatMasks.items():
        jData = data[jCatMask]
        jNotNaMask = pd.notnull(jData)
        if ascending:
            jRank = np.argsort(np.argsort(jData[jNotNaMask]))
        else:
            jRank = np.argsort(np.argsort(-jData[jNotNaMask]))
        if uniformization:
            jRank = (jRank.astype('float') + offset) / jRank.shape[0]
        else:
            jRank = jRank.astype('float')
        jData[jNotNaMask] = jRank
        StdData[jCatMask] = jData
    return StdData


# 分位数变换(Quantile Transformation)标准化
# data: 待标准化的数据, array; cat_data: 分类数据, array
# ascending: 是否升序, 可选: True, False
def standardizeQuantile(data, mask=None, cat_data=None, ascending=True, perturbation=False, other_handle='填充None'):
    """分位数变换标准化"""
    if mask is None:
        mask = (np.zeros(data.shape) == 0)
    StdData = standardizeRank(data, mask=mask, cat_data=cat_data, ascending=ascending, uniformization=True,
                              perturbation=perturbation, offset=0.5, other_handle='填充None')
    StdData = norm.ppf(StdData.astype('float'))
    if other_handle == "保持不变":
        StdData[~mask] = data[~mask]
    return StdData


# 动态分组标准化
# data: 待标准化的数据, array; corr_matrix: 相关系数矩阵, array;
# cat_data: 分类数据, array; n_group: 同类数量, double
def standardizeDynamicPeer(data, corr_matrix, mask=None, cat_data=None, n_group=10, other_handle='填充None'):
    """动态分组标准化"""
    if mask is None:
        mask = (np.zeros(data.shape) == 0)
    if other_handle == "保持不变":
        StdData = np.copy(data)
    else:
        StdData = np.empty(data.shape, dtype='float') + np.nan
    for j in range(data.shape[0]):
        if not mask[j]:
            continue
        jPeerCorr = corr_matrix[j, :]
        jNum = min((n_group, np.sum(jPeerCorr > 0.0)))
        jData = None
        if jNum >= 2:
            jPeerInds = np.argsort(-jPeerCorr)[:jNum]
            jData = data[jPeerInds]
            if np.sum(pd.notnull(jData)) < 2:
                jData = None
        if jData is None:
            if cat_data is not None:
                jCat = cat_data[j]
                if pd.notnull(jCat):
                    jCatMask = (cat_data == jCat)
                else:
                    jCatMask = pd.isnull(cat_data)
                jData = data[jCatMask]
            else:
                jData = data
        jStd = np.nanstd(jData)
        jAvg = np.nanmean(jData)
        if jStd == 0:
            StdData[j] = 0.0
        else:
            StdData[j] = (data[j] - jAvg) / jStd
    return StdData


# 以之前的值进行缺失值填充
# data: 待填充的数据, array; dts: 时间序列, array; lookback: 如果指定了时间序列 dts 则为回溯的时间, 以秒为单位, 否则为回溯期数
def fillNaByLookback(data, lookback, dts=None):
    if not isinstance(data, pd.DataFrame):
        isDF = False
        data = pd.DataFrame(data)
    else:
        isDF = True
    if dts is None:
        dts = data.index.values
    else:
        dts = np.array(dts)
    Ind = pd.DataFrame(
        np.r_[0, np.diff(dts).astype("float")].reshape((data.shape[0], 1)).repeat(data.shape[1], axis=1).cumsum(axis=0))
    Ind1 = Ind.where(pd.notnull(data.values), other=np.nan)
    Ind1.fillna(method="pad", inplace=True)
    data = data.fillna(method="pad")
    data.where(((Ind.values - Ind1.values) / 10 ** 9 <= lookback), np.nan, inplace=True)
    if isDF:
        return data
    else:
        return data.values


# 以固定值进行缺失值填充
# data: 待填充的数据, array; mask: True-False mask, 标记需要填充的范围, array; value: 缺失填充值, double or string
def fillNaNByVal(data, mask=None, value=0.0):
    StdData = np.copy(data)
    if mask is None:
        StdData[pd.isnull(StdData)] = value
    else:
        StdData[mask & pd.isnull(StdData)] = value
    return StdData


# 某个运算结果进行缺失值填充
def fillNaNByFun(data, mask=None, cat_data=None, val_fun=(lambda x, n: np.zeros(n) + np.nanmean(x))):
    StdData = np.copy(data)
    NAMask = pd.isnull(data)
    CatMasks = maskCategary(data.shape[0], cat_data=cat_data, mask=mask)
    for iCat, iCatMask in CatMasks.items():
        iMask = (iCatMask & NAMask)
        StdData[iMask] = val_fun(data[iCatMask], np.sum(iMask))
    return StdData


# 回归方式进行缺失值填充
# Y: 待处理的数据, 因变量, array; X: 自变量, array; mask: True-False mask, 标记需要处理的范围, array;
# cat_data: 分类数据, array; constant: 是否有常数项, True or False; dummy_data: 哑变量, array; drop_dummy_na: 是否舍弃哑变量中的缺失值
def fillNaNByRegress(Y, X, mask=None, cat_data=None, constant=False, dummy_data=None, drop_dummy_na=False):
    StdData = np.copy(Y)
    if mask is None:
        mask = (np.zeros(Y.shape) == 0)
    CatMasks = maskCategary(Y.shape[0], cat_data=cat_data, mask=mask)
    for iCat, iCatMask in CatMasks.items():
        iY = Y[iCatMask]
        iNAMask = pd.isnull(iY)
        iNANum = np.sum(iNAMask)
        if iNANum == 0:
            continue
        iX = (X[iCatMask] if X is not None else X)
        iDummy = (dummy_data[iCatMask] if dummy_data is not None else dummy_data)
        iXNotNAMask, _, _, iXX = prepareRegressData(np.ones(iY.shape[0]), iX, has_constant=constant, dummy_data=iDummy,
                                                    drop_dummy_na=drop_dummy_na)
        iYY = iY[iXNotNAMask]
        iRegressMask = pd.notnull(iYY)
        if np.sum(iRegressMask) < 2:
            continue
        iRslt = sm.OLS(iYY[iRegressMask], iXX[iRegressMask], missing='drop').fit()
        iBeta = iRslt.params
        iX = np.zeros((iY.shape[0], iBeta.shape[0])) + np.nan
        iX[iXNotNAMask] = iXX
        iY_hat = np.sum(iX * iBeta, axis=1)
        iY[iNAMask] = iY_hat[iNAMask]
        StdData[iCatMask] = iY
    return StdData


# 异常值处理; 超过给定标准差倍数的值用相应标准差倍数填充
# data: 待处理的数据, array; std_multiplier: 标准差倍数, double
# method: 处理方式, 可选: 截断, 丢弃, 变换; std_tmultiplier: method为变换时所用到的标准差倍数, double
def winsorize(data, mask=None, cat_data=None, method='截断', avg_statistics="中位数", dispersion_statistics="MAD",
              std_multiplier=3, std_tmultiplier=3.5, other_handle='填充None'):
    if other_handle == '保持不变':
        StdData = np.copy(data)
    else:
        StdData = np.empty(data.shape) + np.nan
    if mask is None:
        mask = (np.zeros(data.shape) == 0)
    CatMasks = maskCategary(data.shape[0], cat_data=cat_data, mask=mask)
    for iCat, iCatMask in CatMasks.items():
        iData = data[iCatMask]
        if avg_statistics == "平均值":
            Avg = np.nanmean(iData)
        elif avg_statistics == "中位数":
            Avg = np.nanmedian(iData)
        if dispersion_statistics == "标准差":
            Std = np.nanstd(iData)
        elif dispersion_statistics == "MAD":
            Std = 1.483 * np.nanmedian(np.abs(iData - np.nanmedian(iData)))
        LeftExtreme = Avg - std_multiplier * Std
        RightExtreme = Avg + std_multiplier * Std
        if method == '截断':
            iData[iData > RightExtreme] = RightExtreme
            iData[iData < LeftExtreme] = LeftExtreme
        elif method == '丢弃':
            iData[iData > RightExtreme] = np.nan
            iData[iData < LeftExtreme] = np.nan
        elif method == '变换':
            Max = np.nanmax(iData)
            Min = np.nanmin(iData)
            sPlus = max((0, min((1, (std_tmultiplier * Std - std_multiplier * Std) / (Max - RightExtreme)))))
            sMinus = max((0, min((1, (std_tmultiplier * Std - std_multiplier * Std) / (LeftExtreme - Min)))))
            Mask = (iData > RightExtreme)
            iData[Mask] = RightExtreme * (1 - sPlus) + sPlus * iData[Mask]
            Mask = (iData < LeftExtreme)
            iData[Mask] = LeftExtreme * (1 - sMinus) + sMinus * iData[Mask]
        StdData[iCatMask] = iData
    return StdData


# 正交化; 线性回归取残差作为新值
# Y: 待处理的数据, 因变量, array; X: 自变量, array; mask: True-False mask, 标记需要处理的范围, array;
# constant: 是否有常数项, True or False; dummy_data: 哑变量, array; drop_dummy_na: 是否舍弃哑变量中的缺失值; other_handle: 不在计算范围内的位置如何处理
# mask 是用来挡住原来的数中 哪些不要的 不给顶mask 那就是nan的不要
def orthogonalize(Y, X, mask=None, constant=False, dummy_data=None, drop_dummy_na=False, other_handle='填充None'):
    StdData = np.empty(Y.shape, dtype='float') + np.nan
    if mask is None:
        mask = pd.isnull(StdData)
    NotNAMask, _, YY, XX = prepareRegressData(Y[mask], (X[mask] if X is not None else X), has_constant=constant,
                                              dummy_data=(dummy_data[mask] if dummy_data is not None else dummy_data),
                                              drop_dummy_na=drop_dummy_na)
    if YY.shape[0] >= 2:
        Result = sm.OLS(YY, XX, missing='drop').fit()
        Temp = StdData[mask]
        Temp[NotNAMask] = Result.resid
        StdData[mask] = Temp
    if other_handle == "保持不变":
        StdData[~mask] = Y[~mask]
    return StdData


# 中性化;
# Y: 待处理的数据, 因变量, array; X: 自变量, array; mask: True-False mask, 标记需要处理的范围, array;
# constant: 是否有常数项, True or False; dummy_data: 哑变量, array; drop_dummy_na: 是否舍弃哑变量中的缺失值; other_handle: 不在计算范围内的位置如何处理
def neutralize(Y, X, cov_matrix, mask=None, constant=False, dummy_data=None, drop_dummy_na=False,
               other_handle='填充None'):
    StdData = np.empty(Y.shape, dtype='float') + np.nan
    if mask is None:
        mask = pd.isnull(StdData)
    cov_matrix = cov_matrix[mask, :][:, mask]
    NotNAMask, _, YY, XX = prepareRegressData(Y[mask], (X[mask] if X is not None else X), has_constant=constant,
                                              dummy_data=(dummy_data[mask] if dummy_data is not None else dummy_data),
                                              drop_dummy_na=drop_dummy_na)
    Mask = (np.sum(pd.notnull(cov_matrix), axis=1) > 0)
    Mask = ((np.sum(pd.isnull(cov_matrix[:, Mask]), axis=1) == 0) & Mask & NotNAMask)
    cov_matrix = cov_matrix[Mask, :][:, Mask]
    YY = YY[Mask[NotNAMask]]
    XX = XX[Mask[NotNAMask]]
    if XX.ndim == 1:
        XX = np.reshape(XX, (XX.shape[0], 1))
    Temp = StdData[mask]
    Temp[Mask] = YY - np.dot(
        np.dot(np.dot(np.dot(XX, np.linalg.inv(np.dot(np.dot(XX.T, cov_matrix), XX))), XX.T), cov_matrix), YY)
    StdData[mask] = Temp
    if other_handle == "保持不变":
        StdData[~mask] = Y[~mask]
    return StdData


# 合并因子数据
# data: 待处理的数据, [array,...] or array; method: 合成方式, 可选: 直接合成, 归一合成; nan_handle: 缺失处理, 可选: 剩余合成, 填充None
def merge(data, mask=None, weight=None, method='直接合成', nan_handle='剩余合成'):
    if not isinstance(data, np.ndarray):
        data = np.array(list(zip(*data)))
    elif data.ndim == 1:
        data = np.reshape(data, (data.shape[0], 1))
    if mask is None:
        mask = (np.zeros(data.shape[0]) == 0)
    if weight is None:
        weight = np.ones(data.shape[1]) / data.shape[1]
    else:
        weight = np.array(weight)
    if method == '归一合成':
        weight = weight / np.sum(np.abs(weight))
    if nan_handle == '填充None':
        StdData = np.sum(data * weight, axis=1)
    elif nan_handle == '剩余合成':
        StdData = np.nansum(data * weight, axis=1)
        if method == "归一合成":
            TotalWeight = np.sum(pd.notnull(data) * np.abs(weight), axis=1)
            TotalWeight[TotalWeight == 0] = np.nan
            StdData = StdData / TotalWeight
    StdData[~mask] = np.nan
    return StdData
