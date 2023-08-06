"""
@Author        : 林泽明
@Time          : 2021-06-16 17:22:51
@Function      :

"""
import pandas as pd
from .data_operator import ts_mean


def MA_LONG_SHORT_ORDER(open_hfq: pd.DataFrame, high_hfq: pd.DataFrame, low_hfq: pd.DataFrame, close_hfq: pd.DataFrame,
                        volume: pd.DataFrame):
    """
    @Author        : 林泽明
    @Time          : 2021-06-16 17:35:44
    @Function      :
    ma多头排列
    """
    ma5 = ts_mean(close_hfq, 5)
    ma10 = ts_mean(close_hfq, 10)
    ma20 = ts_mean(close_hfq, 20)
    ma60 = ts_mean(close_hfq, 60)
    ma120 = ts_mean(close_hfq, 120)
    res = pd.DataFrame(index=close_hfq.index, columns=close_hfq.columns)
    res[(ma5 > ma10) & (ma10 > ma20) & (ma20 > ma60) & (ma60 > ma120)] = 100
    res[(ma5 < ma10) & (ma10 < ma20) & (ma20 < ma60) & (ma60 < ma120)] = -100
    res = res.fillna(0)
    return ['ma_long_short_order'], [res]
