"""
@Author        : 林泽明
@Time          : 2021-06-07 22:26:17
@Function      :
算子 基于single indicator
"""
import numpy as np
import pandas as pd



def bs_add(df1, df2):
    return df1 + df2


def bs_sub(df1, df2):
    return df1 - df2


def bs_mul(df1, df2):
    return df1 * df2


def bs_div(df1, df2):
    return df1 / df2


def bs_sqrt(df):
    return np.sqrt(df)


def bs_abs(df):
    return np.abs(df)


def bs_log(df):
    return np.log(df)


def bs_inv(df):
    return 1 / df


def ts_rank_5(x):
    return x.rolling(5).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_rank_10(x):
    return x.rolling(10).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_rank_20(x):
    return x.rolling(20).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_rank_60(x):
    return x.rolling(60).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_rank_120(x):
    return x.rolling(120).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_rank_250(x):
    return x.rolling(250).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_rank_500(x):
    return x.rolling(500).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])


def ts_prod_5(df):  # 效率很慢
    return df.rolling(5).agg(lambda x: x.prod())


def ts_prod_10(df):  # 效率很慢
    return df.rolling(10).agg(lambda x: x.prod())


def ts_prod_20(df):  # 效率很慢
    return df.rolling(20).agg(lambda x: x.prod())


def ts_prod_60(df):  # 效率很慢
    return df.rolling(60).agg(lambda x: x.prod())


def ts_mean_5(df: pd.DataFrame):
    return df.rolling(5).mean()


def ts_mean_10(df: pd.DataFrame):
    return df.rolling(10).mean()


def ts_mean_20(df: pd.DataFrame):
    return df.rolling(20).mean()


def ts_mean_60(df: pd.DataFrame):
    return df.rolling(60).mean()


def ts_mean_120(df: pd.DataFrame):
    return df.rolling(120).mean()


def ts_std_5(df: pd.DataFrame):
    return df.rolling(5).std()


def ts_std_10(df: pd.DataFrame):
    return df.rolling(10).std()


def ts_std_20(df: pd.DataFrame):
    return df.rolling(20).std()


def ts_std_60(df: pd.DataFrame):
    return df.rolling(60).std()


def ts_zscore_5(df: pd.DataFrame):
    return (df - ts_mean_5(df)) / ts_std_5(df)


def ts_zscore_10(df: pd.DataFrame):
    return (df - ts_mean_10(df)) / ts_std_10(df)


def ts_zscore_20(df: pd.DataFrame):
    return (df - ts_mean_20(df)) / ts_std_20(df)


def ts_zscore_60(df: pd.DataFrame):
    return (df - ts_mean_60(df)) / ts_std_60(df)


def ts_delta_1(df):
    return df.diff(1)


def ts_delta_5(df):
    return df.diff(5)


def ts_delta_10(df):
    return df.diff(10)


def ts_delta_20(df):
    return df.diff(20)


def ts_delta_60(df):
    return df.diff(60)


def ts_argmin_5(df):
    df.rolling(5).agg(np.argmin)


def ts_argmin_10(df):
    df.rolling(10).agg(np.argmin)


def ts_argmin_20(df):
    df.rolling(20).agg(np.argmin)


def ts_argmin_60(df):
    df.rolling(60).agg(np.argmin)


def ts_argmax_5(df):
    df.rolling(5).agg(np.argmax)


def ts_argmax_10(df):
    df.rolling(10).agg(np.argmax)


def ts_argmax_20(df):
    df.rolling(20).agg(np.argmax)


def ts_argmax_60(df):
    df.rolling(60).agg(np.argmax)


def ts_min_5(df: pd.DataFrame):
    return df.rolling(5).min()


def ts_min_10(df: pd.DataFrame):
    return df.rolling(10).min()


def ts_min_20(df: pd.DataFrame):
    return df.rolling(20).min()


def ts_min_60(df: pd.DataFrame):
    return df.rolling(60).min()


def ts_max_5(df: pd.DataFrame):
    return df.rolling(5).max()


def ts_max_10(df: pd.DataFrame):
    return df.rolling(10).max()


def ts_max_20(df: pd.DataFrame):
    return df.rolling(20).max()


def ts_max_60(df: pd.DataFrame):
    return df.rolling(60).max()


def ts_sum_5(df: pd.DataFrame):
    return df.rolling(5).sum()


def ts_sum_10(df: pd.DataFrame):
    return df.rolling(10).sum()


def ts_sum_20(df: pd.DataFrame):
    return df.rolling(20).sum()


def ts_sum_60(df: pd.DataFrame):
    return df.rolling(60).sum()


def ts_forward_pct_chg_1(df: pd.DataFrame):
    return df.shift(-1) / df - 1


def ts_forward_pct_chg_5(df: pd.DataFrame):
    return df.shift(-5) / df - 1


def ts_forward_pct_chg_10(df: pd.DataFrame):
    return df.shift(-10) / df - 1


def ts_forward_pct_chg_20(df: pd.DataFrame):
    return df.shift(-20) / df - 1


def ts_forward_pct_chg_60(df: pd.DataFrame):
    return df.shift(-60) / df - 1


def ts_backward_pct_chg_1(df: pd.DataFrame):
    return df.pct_change(1)


def ts_backward_pct_chg_5(df: pd.DataFrame):
    return df.pct_change(5)


def ts_backward_pct_chg_10(df: pd.DataFrame):
    return df.pct_change(10)


def ts_backward_pct_chg_20(df: pd.DataFrame):
    return df.pct_change(20)


def ts_backward_pct_chg_60(df: pd.DataFrame):
    return df.pct_change(60)


def ts_corr_5(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(5).corr(y)


def ts_corr_10(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(10).corr(y)


def ts_corr_20(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(20).corr(y)


def ts_corr_60(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(60).corr(y)


def ts_cov_5(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(5).cov(y)


def ts_cov_10(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(10).cov(y)


def ts_cov_20(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(20).cov(y)


def ts_cov_60(x: pd.DataFrame, y: pd.DataFrame):
    return x.rolling(60).cov(y)


def ts_scale(x: pd.DataFrame):
    return x / np.abs(x).sum()


def rank(x):
    return x.rank(axis=0, pct=True)


def ts_delay_1(x):
    return x.shift(1)


def ts_delay_5(x):
    return x.shift(5)


def ts_delay_10(x):
    return x.shift(10)


def ts_delay_20(x):
    return x.shift(20)


def ts_delay_60(x):
    return x.shift(60)


def cs_orthogonalize(y, x):
    def calc_ortho(_y, _x):
        a = _y.to_numpy()
        b = _x.loc[_y.name].to_numpy()
        c = orthogonalize(a, b)
        return pd.Series(c, index=_y.index, name=_y.name)

    res = y.apply(lambda z: calc_ortho(z, x), axis=1)
    return res


def cs_rank(x):
    return x.rank(axis=1, pct=True)


def cs_rank_ratio(x):
    a = cs_rank(x)
    b = a.div(a.max(axis=1), axis=0)
    return b


def cs_zscore(df: pd.DataFrame):
    def _cs_mean(df: pd.DataFrame):
        return df.mean(axis=1)

    def _cs_std(df: pd.DataFrame):
        return df.std(axis=1)

    return (df.sub(_cs_mean(df), axis=0)).div(_cs_std(df), axis=0)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def rank_sub(X, Y):
    return (rank(X) - rank(Y))


def rank_div(X, Y):
    return (rank(X) / rank(Y))


def cs_winsorize(x):
    res = x.apply(lambda x: winsorize(x), axis=0)
    return res
