"""
@Author        : 林泽明
@Time          : 2021-06-16 17:22:51
@Function      :

"""
import pandas as pd
from .data_operator import ts_mean, ts_max, ts_min


def BOLL_BAND(open_hfq: pd.DataFrame, high_hfq: pd.DataFrame, low_hfq: pd.DataFrame, close_hfq: pd.DataFrame,
              volume: pd.DataFrame):
    boll_up = ts_mean(close_hfq, 20) + 2 * ts_mean(close_hfq, 20)
    boll_down = ts_mean(close_hfq, 20) - 2 * ts_mean(close_hfq, 20)
    boll_pos = (close_hfq - boll_down) / (boll_up - boll_down)
    return ["boll_up", "boll_down", "boll_pos"], [boll_up, boll_down, boll_pos]


def TANGQIAN_BAND(open_hfq: pd.DataFrame, high_hfq: pd.DataFrame, low_hfq: pd.DataFrame, close_hfq: pd.DataFrame,
                  volume: pd.DataFrame):
    tqa_up = ts_max(high_hfq, 20)
    tqa_down = ts_min(low_hfq, 20)
    tqa_pos = (close_hfq - tqa_down) / (tqa_up - tqa_down)
    return ['tangqian_up', 'tangqian_down', 'tangqian_pos'], [tqa_up, tqa_down, tqa_pos]
