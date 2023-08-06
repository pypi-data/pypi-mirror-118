"""
@Author        : 林泽明
@Time          : 2021-06-07 22:26:17
@Function      :
算子 基于single indicator
"""
import numpy as np
import pandas as pd
from quant_util.data_process_MathFun import winsorize, orthogonalize


def bs_add(p1, p2):
    return p1 + p2


def bs_sub(p1, p2):
    return p1 - p2


def bs_mul(p1, p2):
    return p1 * p2


def bs_div(p1, p2):
    return p1 / p2


def bs_sqrt(p1):
    return np.sqrt(p1)


def bs_abs(p1):
    return np.abs(p1)


def bs_log(p1):
    return np.log(p1)


def bs_inv(p1):
    return 1 / p1


def ts_rank(p1, c1):
    return p1.rolling(c1).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_prod(p1, c1):  # 效率很慢
    return p1.rolling(c1).agg(lambda x: x.prod())


def ts_mean(p1, c1):
    return p1.rolling(c1).mean()


def ts_std(p1, c1):
    return p1.rolling(c1).std()


def ts_zscore(p1, c1):
    return (p1 - p1.rolling(c1).mean()) / p1.rolling(c1).std()


def ts_delta(p1, c1):
    return p1.diff(c1)


def ts_argmin(p1, c1):
    return p1.rolling(c1).agg(np.argmin)


def ts_argmax(p1, c1):
    return p1.rolling(c1).agg(np.argmax)


def ts_min(p1, c1):
    return p1.rolling(c1).min()


def ts_max(p1, c1):
    return p1.rolling(c1).max()


def ts_sum(p1, c1):
    return p1.rolling(c1).sum()


def ts_backward_pct_chg(p1, c1):
    return p1.pct_change(c1)


def ts_corr(p1, p2, c1):
    return p1.rolling(c1).corr(p2)


def ts_cov(p1, p2, c1):
    return p1.rolling(c1).cov(p2)


def ts_scale(x: pd.DataFrame):
    return x / np.abs(x).sum()


def ts_delay(p1, c1):
    return p1.shift(c1)


def cs_rank(p1):
    return p1.rank(axis=1, pct=True)


def cs_zscore(p1):
    def _cs_mean(df: pd.DataFrame):
        return df.mean(axis=1)

    def _cs_std(df: pd.DataFrame):
        return df.std(axis=1)

    return (p1.sub(_cs_mean(p1), axis=0)).div(_cs_std(p1), axis=0)


def sigmoid(p1):
    return 1 / (1 + np.exp(-p1))


def rank_sub(p1, p2):
    return (rank(p1) - rank(p2))


def rank_div(X, Y):
    return (rank(X) / rank(Y))


def rank(x):
    return x.rank(axis=0, pct=True)


def cs_winsorize(p1):
    res = p1.apply(lambda x: winsorize(x), axis=0)
    return res


def ts_count(p1, c1):
    return p1.rolling(c1).count()


def ts_var(p1, c1):
    return p1.rolling(c1).var()


def ts_kurt(p1, c1):
    return p1.rolling(c1).kurt()


def ts_skew(p1, c1):
    return p1.rolling(c1).skew()


def ts_median(p1, c1):
    return p1.rolling(c1).median()


def cs_orthogonalize(p1, p2):
    def calc_ortho(_y, _x):
        a = _y.to_numpy()
        b = _x.loc[_y.name].to_numpy()
        c = orthogonalize(a, b)
        return pd.Series(c, index=_y.index, name=_y.name)

    res = p1.apply(lambda z: calc_ortho(z, p2), axis=1)
    return res
