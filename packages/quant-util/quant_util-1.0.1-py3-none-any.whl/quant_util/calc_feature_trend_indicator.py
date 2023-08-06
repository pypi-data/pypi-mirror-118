"""
@Author        : 林泽明
@Time          : 2021-06-16 17:22:51
@Function      :

"""
import pandas as pd
from .data_operator import ts_mean_20, ts_std_20, ts_mean_5, ts_mean_10, ts_max_20, ts_min_20, ts_mean_60, ts_mean_120


def MA_LONG_SHORT_ORDER(open_hfq: pd.DataFrame, high_hfq: pd.DataFrame, low_hfq: pd.DataFrame, close_hfq: pd.DataFrame,
                        volume: pd.DataFrame):
    """
    @Author        : 林泽明
    @Time          : 2021-06-16 17:35:44
    @Function      :
    ma多头排列
    """
    ma5 = ts_mean_5(close_hfq)
    ma10 = ts_mean_10(close_hfq)
    ma20 = ts_mean_20(close_hfq)
    ma60 = ts_mean_60(close_hfq)
    ma120 = ts_mean_120(close_hfq)
    res = pd.DataFrame(index=close_hfq.index, columns=close_hfq.columns)
    res[(ma5 > ma10) & (ma10 > ma20) & (ma20 > ma60) & (ma60 > ma120)] = 100
    res[(ma5 < ma10) & (ma10 < ma20) & (ma20 < ma60) & (ma60 < ma120)] = -100
    res = res.fillna(0)
    return ['ma_long_short_order'], [res]
