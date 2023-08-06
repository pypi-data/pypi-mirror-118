import quant_util
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
from tqdm import tqdm
import collections
import math


class FeatureDaily1:
    def __init__(self, code_list, end):
        start = (pd.to_datetime(end) - pd.Timedelta(days=365 * 2 + 100)).strftime('%Y-%m-%d')

        # 正在获取
        print("get close", start, end)
        df_close = quant_util.query_feature_single(code_list, start, end, "daily_hq", "close").fillna(method='ffill')
        print(df_close.tail(5)[code_list[:5]])

        print("get open", start, end)
        df_open = quant_util.query_feature_single(code_list, start, end, "daily_hq", "open").fillna(method='ffill')
        print(df_open.tail(5)[code_list[:5]])

        print("get high", start, end)
        df_high = quant_util.query_feature_single(code_list, start, end, "daily_hq", "high").fillna(method='ffill')
        print(df_high.tail(5)[code_list[:5]])

        print("get low", start, end)
        df_low = quant_util.query_feature_single(code_list, start, end, "daily_hq", "low").fillna(method='ffill')
        print(df_low.tail(5)[code_list[:5]])

        print("get up limit", start, end)
        df_up_limit = quant_util.query_feature_single(code_list, start, end, "stk_limit", "up_limit").fillna(
            method='ffill')
        print(df_up_limit.tail(5)[code_list[:5]])

        print("get df_adj_factor", start, end)
        df_adj_factor = quant_util.query_feature_single(code_list, start, end, "factor_adj", "adj_factor").fillna(
            method='ffill')
        print(df_adj_factor.tail(5)[code_list[:5]])

        print("get volume", start, end)
        df_volume = quant_util.query_feature_single(code_list, start, end, "daily_hq", 'volume').fillna(method='ffill')
        print(df_volume.tail(5)[code_list[:5]])

        print("get volume ratio", start, end)
        df_volume_ratio = quant_util.query_feature_single(code_list, start, end, "daily_basic", "volume_ratio").fillna(
            0)
        print(df_volume_ratio.tail(5)[code_list[:5]])

        print("get pettm", start, end)
        df_pe_ttm = quant_util.query_feature_single(code_list, start, end, "daily_basic", "pe_ttm").fillna(0)
        print(df_pe_ttm.tail(5)[code_list[:5]])

        print("get free share", start, end)
        df_free_share = quant_util.query_feature_single(code_list, start, end, "daily_basic", "free_share").fillna(
            method='ffill') * 1e4
        print(df_free_share.tail(5)[code_list[:5]])

        print("get circ mv", start, end)
        df_circ_mv = quant_util.query_feature_single(code_list, start, end, "daily_basic", "circ_mv").fillna(
            method='ffill') * 1e4
        print(df_circ_mv.tail(5)[code_list[:5]])

        print("get df_turnover_rate_f", start, end)
        df_turnover_rate_f = quant_util.query_feature_single(code_list, start, end, "daily_basic",
                                                             "turnover_rate_f").fillna(0)
        print(df_turnover_rate_f.tail(5)[code_list[:5]])

        print("get df_limit", start, end)
        df_limit = quant_util.query_feature_single(code_list, start, end, "limit_list", 'limit')
        print(df_limit.tail(5)[code_list[:5]])

        print("正在计算相关指标")
        df_close_hfq = df_close * df_adj_factor
        df_open_hfq = df_open * df_adj_factor
        df_high_hfq = df_high * df_adj_factor
        df_low_hfq = df_low * df_adj_factor
        df_is_meet_limit = df_limit == "U"

        fes = {}
        fes['close'] = df_close
        fes['free_share'] = df_free_share
        fes['circ_mv'] = df_circ_mv
        fes['pe_ttm'] = df_pe_ttm
        fes['turnover_rate_f'] = df_turnover_rate_f
        fes['volume'] = df_volume

        days = [5, 10, 20, 60, 120, 250, 500]
        # 收盘价排名
        print("计算指标-", "close_rank")
        feature_name = "close_rank"
        var = quant_util.cs_rank(df_close)
        fes['cs_rank(close)'] = var

        # 近期涨停次数
        print("计算指标-", "近期涨停次数")
        for day in tqdm(days):
            var = quant_util.cs_rank((df_limit == "U").rolling(day).sum())
            feature_name = f'up_limit_times_rank_{day}'
            fes[feature_name] = var

        # 近期触板次数
        print("计算指标-", "近期触板次数")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_is_meet_limit.rolling(day).sum())
            feature_name = f'meet_up_limit_times_rank_{day}'
            fes[feature_name] = var

        # 振幅
        print("计算指标-", "振幅")
        for day in tqdm(days):
            var = quant_util.cs_rank(((df_high_hfq - df_low_hfq) / df_close_hfq.shift(1)).rolling(day).mean())
            feature_name = f'amplitude_rank_{day}'
            fes[feature_name] = var

        # 换手率
        print("计算指标-", "换手率")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_turnover_rate_f.rolling(day).mean())
            feature_name = f'turnover_rate_f_mean_rank_{day}'
            fes[feature_name] = var

        # 股价在过去的位置水平
        print("计算指标-", "股价在过去的位置水平")
        for day in tqdm(days):
            var = quant_util.cs_rank(
                (df_close_hfq - df_close_hfq.rolling(day).mean()) / df_close_hfq.rolling(day).std())
            feature_name = f'close_position_rank_{day}'
            fes[feature_name] = var

        # 量价corr
        print("计算指标-", "量价corr")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_close_hfq.rolling(day).corr(df_volume))
            feature_name = f'close_volume_corr_rank_{day}'
            fes[feature_name] = var

        # high low corr
        print("计算指标-", "high low corr")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_high_hfq.rolling(day).corr(df_low_hfq))
            feature_name = f'high_low_corr_rank_{day}'
            fes[feature_name] = var

        # 空头力道
        print("计算指标-", "空头力道")
        for day in tqdm(days):
            var = quant_util.cs_rank((df_low_hfq - df_close_hfq.rolling(day).mean()) / df_close_hfq)
            feature_name = f'kong_tou_li_dao_rank_{day}'
            fes[feature_name] = var

        # 布林带
        print("计算指标-", "布林带")
        var = quant_util.cs_rank(
            quant_util.BOLL_BAND(df_open_hfq, df_high_hfq, df_low_hfq, df_close_hfq, df_volume)[1][2] * -1)
        feature_name = f'boll_band_position_rank'
        fes[feature_name] = var

        # 唐安琪通道
        print("计算指标-", "唐安琪通道")
        var = quant_util.cs_rank(
            quant_util.TANGQIAN_BAND(df_open_hfq, df_high_hfq, df_low_hfq, df_close_hfq, df_volume)[1][2] * -1)
        feature_name = f'tang_an_qi_band_position_rank'
        fes[feature_name] = var
        # In[ ]:

        # bias
        print("计算指标-", "bias")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_close_hfq.rolling(day).mean() / df_close_hfq)
            feature_name = f'bias_rank_{day}'
            fes[feature_name] = var

        # 多头排列
        print("计算指标-", "多头排列")
        var = quant_util.MA_LONG_SHORT_ORDER(df_open_hfq, df_high_hfq, df_low_hfq, df_close_hfq, df_volume)[1][0] / 100
        feature_name = f'long_order'
        fes[feature_name] = var

        # volume_ratio_mean
        print("计算指标-", "volume_ratio_mean")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_volume_ratio.rolling(day).mean())
            feature_name = f'volume_ratio_mean_rank_{day}'
            fes[feature_name] = var

        # pe_ttm rank
        print("计算指标-", "df_pe_ttm")
        var = quant_util.cs_rank(df_pe_ttm)
        feature_name = f'pe_ttm_rank'
        fes[feature_name] = var

        # 动量
        print("计算指标-", "动量")
        for day in tqdm(days):
            var = quant_util.cs_rank(df_close_hfq.pct_change(day))
            feature_name = f'momentum_rank_{day}'
            fes[feature_name] = var

        # cyf
        print("计算指标-", "cyf")
        for day in days:
            var = quant_util.cs_rank(100 - 100 / (1 + df_turnover_rate_f.rolling(day).mean()))
            feature_name = f'cyf_rank_{day}'
            fes[feature_name] = var

        # 主力控盘系数
        print("计算指标-", "主力控盘系数")
        B1 = (df_high_hfq.rolling(35).max() - df_close_hfq) / (
                df_high_hfq.rolling(35).max() - df_low_hfq.rolling(35).min()) * 100 - 35
        B2 = B1.rolling(35).mean() + 100
        B3 = (df_close_hfq - df_low_hfq.rolling(35).min()) / (
                df_high_hfq.rolling(35).max() - df_low_hfq.rolling(35).min()) * 100
        B4 = B3.rolling(3).mean()
        B5 = B4.rolling(3).mean() + 100
        B6 = B5 - B2
        var = quant_util.cs_rank(B6)
        feature_name = f'tdx_zhulikongpanxishu_rank'
        fes[feature_name] = var

        # 市值 rank
        print("计算指标-", "df_circ_mv")
        var = quant_util.cs_rank(df_circ_mv)
        feature_name = f'circ_mv_rank'
        fes[feature_name] = var

        # vwap_daily
        print("计算指标-", "vwap_daily")
        for day in days:
            var = (((df_close + df_high + df_low) / 3 * df_volume).rolling(day).sum() / df_volume.rolling(
                day).sum()) / df_up_limit
            var = quant_util.cs_rank(var)
            feature_name = f'vwap_to_up_limit_rank_{day}'
            fes[feature_name] = var

        self.features = fes

    def get_feature(self, date, code):
        res = {}
        for key in self.features.keys():
            res[key] = self.features[key].loc[
                date, code]  # 1.7 ms ± 66.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

        # fill nan
        for key, value in res.items():
            if math.isnan(value):
                res[key] = 0.0

        res_sorted = collections.OrderedDict(sorted(res.items()))
        return res_sorted
