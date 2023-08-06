import quant_util as qu
import warnings
from tqdm import tqdm
import collections
import math
import gc

warnings.filterwarnings('ignore')


class FeatureDaily:
    def __init__(self, code_list, start, end, save_mem=False):  # 开启save_mem会导致只保留最后20个数值 也就是最近一个月的因子值
        if save_mem:
            self.keep_start = -20
        else:
            self.keep_start = 0

        # 基础operator定义
        self.basic_operators = {
            "add": qu.bs_add,
            "sub": qu.bs_sub,
            "mul": qu.bs_mul,
            "div": qu.bs_div,
            "sqrt": qu.bs_sqrt,
            "abs": qu.bs_abs,
            "log": qu.bs_log,
            "inv": qu.bs_inv,
            "div": qu.bs_div,
            #     "ts_rank":qu.ts_rank,
            "ts_mean": qu.ts_mean,
            "ts_std": qu.ts_std,
            "ts_zscore": qu.ts_zscore,
            "ts_delta": qu.ts_delta,
            #     "ts_argmin":qu.ts_argmin,
            #     "ts_argmax":qu.ts_argmax,
            "ts_min": qu.ts_min,
            "ts_max": qu.ts_max,
            "ts_sum": qu.ts_sum,
            "ts_backward_pct_chg": qu.ts_backward_pct_chg,
            "ts_corr": qu.ts_corr,
            "ts_cov": qu.ts_cov,
            "ts_delay": qu.ts_delay,
            "cs_rank": qu.cs_rank,
            "cs_zscore": qu.cs_zscore,
            "sigmoid": qu.sigmoid,
            #     "cs_winsorize": qu.cs_winsorize,
            "ts_count": qu.ts_count,
            "ts_var": qu.ts_var,
            "ts_kurt": qu.ts_kurt,
            "ts_skew": qu.ts_skew,
            "ts_median": qu.ts_median,
            "cs_orthogonalize": qu.cs_orthogonalize,
        }

        # 开始获取因子
        print("get close", start, end)
        df_close = qu.query_feature_single(code_list, start, end, "daily_hq", "close").fillna(method='ffill')
        print("get open", start, end)
        df_open = qu.query_feature_single(code_list, start, end, "daily_hq", "open").fillna(method='ffill')
        print("get high", start, end)
        df_high = qu.query_feature_single(code_list, start, end, "daily_hq", "high").fillna(method='ffill')
        print("get low", start, end)
        df_low = qu.query_feature_single(code_list, start, end, "daily_hq", "low").fillna(method='ffill')
        print("get up limit", start, end)
        df_up_limit = qu.query_feature_single(code_list, start, end, "stk_limit", "up_limit").fillna(method='ffill')
        print("get df_adj_factor", start, end)
        df_adj_factor = qu.query_feature_single(code_list, start, end, "factor_adj", "adj_factor").fillna(
            method='ffill')
        print("get volume", start, end)
        df_volume = qu.query_feature_single(code_list, start, end, "daily_hq", 'volume').fillna(method='ffill')
        print("get volume ratio", start, end)
        df_volume_ratio = qu.query_feature_single(code_list, start, end, "daily_basic", "volume_ratio").fillna(0)
        print("get pettm", start, end)
        df_pe_ttm = qu.query_feature_single(code_list, start, end, "daily_basic", "pe_ttm").fillna(0)
        print("get free share", start, end)
        df_free_share = qu.query_feature_single(code_list, start, end, "daily_basic", "free_share").fillna(
            method='ffill') * 1e4
        print("get circ mv", start, end)
        df_circ_mv = qu.query_feature_single(code_list, start, end, "daily_basic", "circ_mv").fillna(
            method='ffill') * 1e4
        print("get df_turnover_rate_f", start, end)
        df_turnover_rate_f = qu.query_feature_single(code_list, start, end, "daily_basic", "turnover_rate_f").fillna(0)
        print("get df_limit", start, end)
        df_limit = qu.query_feature_single(code_list, start, end, "limit_list", 'limit')

        print("get df_top_list", start, end)
        df_top_list_pct_change = qu.query_feature_single(code_list, start, end, "top_list", "top_list_pct_change")
        df_top_list_amount = qu.query_feature_single(code_list, start, end, "top_list", "top_list_amount")
        df_top_list_l_sell = qu.query_feature_single(code_list, start, end, "top_list", "top_list_l_sell")
        df_top_list_l_buy = qu.query_feature_single(code_list, start, end, "top_list", "top_list_l_buy")
        df_top_list_l_amount = qu.query_feature_single(code_list, start, end, "top_list", "top_list_l_amount")
        df_top_list_net_amount = qu.query_feature_single(code_list, start, end, "top_list", "top_list_net_amount")
        df_top_list_reason = qu.query_feature_single(code_list, start, end, "top_list", "top_list_reason")
        var = df_top_list_reason.stack().to_frame()
        var['reason_is_zhangfu'] = var[0].apply(lambda x: "涨幅" in x)
        df_reason_is_zhangfu = var[['reason_is_zhangfu']].copy().unstack().fillna(False)
        df_reason_is_zhangfu.columns = df_reason_is_zhangfu.columns.droplevel(0)
        df_reason_is_zhangfu = df_reason_is_zhangfu + 0.0
        var = df_top_list_reason.stack().to_frame()
        var['reason_is_diefu'] = var[0].apply(lambda x: "跌幅" in x)
        df_reason_is_diefu = var[['reason_is_diefu']].copy().unstack().fillna(False)
        df_reason_is_diefu.columns = df_reason_is_diefu.columns.droplevel(0)
        df_reason_is_diefu = df_reason_is_diefu + 0.0

        self.basic_feature = {
            "top_list.top_list_pct_change": df_top_list_pct_change,
            "top_list.top_list_amount": df_top_list_amount,
            "top_list.top_list_l_sell": df_top_list_l_sell,
            "top_list.top_list_l_buy": df_top_list_l_buy,
            "top_list.top_list_l_amount": df_top_list_l_amount,
            "top_list.reason_is_contain_zhangfu": df_reason_is_zhangfu,
            "top_list.reason_is_contain_diefu": df_reason_is_diefu,
            "daily_hq.close": df_close,
            "daily_hq.close_hfq": df_close * df_adj_factor,
            "daily_hq.open_hfq": df_open * df_adj_factor,
            "daily_hq.high_hfq": df_high * df_adj_factor,
            "daily_hq.low_hfq": df_low * df_adj_factor,
            "daily_hq.pct_chg": qu.query_feature_single(code_list, start, end, "daily_hq", 'pct_chg').fillna(0),
            "daily_hq.amount": qu.query_feature_single(code_list, start, end, "daily_hq", 'amount').fillna(0),
            "factor_adj.adj_factor": df_adj_factor,
            "daily_hq.volume": df_volume,
            "daily_basic.volume": df_volume_ratio,
            "daily_basic.pe_ttm": df_pe_ttm,
            "daily_basic.total_mv": df_circ_mv,
            "daily_basic.circ_mv": df_circ_mv,
            "daily_basic.turnover_rate_f": df_turnover_rate_f,
            "daily_basic.turnover_rate": qu.query_feature_single(code_list, start, end, "daily_basic",
                                                                 'turnover_rate').fillna(0),
            "daily_basic.pb": qu.query_feature_single(code_list, start, end, "daily_basic", 'pb').fillna(
                method='ffill'),
            "daily_basic.ps": qu.query_feature_single(code_list, start, end, "daily_basic", 'ps').fillna(
                method='ffill'),
            "daily_basic.ps_ttm": qu.query_feature_single(code_list, start, end, "daily_basic", 'ps_ttm').fillna(
                method='ffill'),
            "daily_basic.dv_ratio": qu.query_feature_single(code_list, start, end, "daily_basic", 'dv_ratio').fillna(
                method='ffill'),
            "daily_basic.dv_ttm": qu.query_feature_single(code_list, start, end, "daily_basic", 'dv_ttm').fillna(
                method='ffill'),
            "daily_basic.total_share": qu.query_feature_single(code_list, start, end, "daily_basic",
                                                               'total_share').fillna(method='ffill'),
            "daily_basic.float_share": qu.query_feature_single(code_list, start, end, "daily_basic",
                                                               'float_share').fillna(method='ffill'),
            "daily_basic.free_share": df_free_share,
            "express.express_revenue": qu.query_feature_single(code_list, start, end, "express",
                                                               'express_revenue').fillna(0),
            "express.express_operate_profit": qu.query_feature_single(code_list, start, end, "express",
                                                                      'express_operate_profit').fillna(0),
            "express.express_total_profit": qu.query_feature_single(code_list, start, end, "express",
                                                                    'express_total_profit').fillna(0),
            "express.express_n_income": qu.query_feature_single(code_list, start, end, "express",
                                                                'express_n_income').fillna(0),
            "express.express_total_assets": qu.query_feature_single(code_list, start, end, "express",
                                                                    'express_total_assets').fillna(0),
            "express.express_total_hldr_eqy_exc_min_int": qu.query_feature_single(code_list, start, end, "express",
                                                                                  'express_total_hldr_eqy_exc_min_int').fillna(
                0),
            "express.express_diluted_eps": qu.query_feature_single(code_list, start, end, "express",
                                                                   'express_diluted_eps').fillna(0),
            "express.express_diluted_roe": qu.query_feature_single(code_list, start, end, "express",
                                                                   'express_diluted_roe').fillna(0),
            "express.express_yoy_net_profit": qu.query_feature_single(code_list, start, end, "express",
                                                                      'express_yoy_net_profit').fillna(0),
            "moneyflow.buy_sm_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'buy_sm_vol').fillna(0),
            "moneyflow.buy_sm_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                               'buy_sm_amount').fillna(0),
            "moneyflow.sell_sm_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'sell_sm_vol').fillna(
                0),
            "moneyflow.sell_sm_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                                'sell_sm_amount').fillna(0),
            "moneyflow.buy_md_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'buy_md_vol').fillna(0),
            "moneyflow.buy_md_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                               'buy_md_amount').fillna(0),
            "moneyflow.sell_md_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'sell_md_vol').fillna(
                0),
            "moneyflow.sell_md_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                                'sell_md_amount').fillna(0),
            "moneyflow.buy_lg_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'buy_lg_vol').fillna(0),
            "moneyflow.buy_lg_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                               'buy_lg_amount').fillna(0),
            "moneyflow.sell_lg_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'sell_lg_vol').fillna(
                0),
            "moneyflow.sell_lg_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                                'sell_lg_amount').fillna(0),
            "moneyflow.buy_elg_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'buy_elg_vol').fillna(
                0),
            "moneyflow.buy_elg_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                                'buy_elg_amount').fillna(0),
            "moneyflow.sell_elg_vol": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                              'sell_elg_vol').fillna(0),
            "moneyflow.sell_elg_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                                 'sell_elg_amount').fillna(0),
            "moneyflow.net_mf_vol": qu.query_feature_single(code_list, start, end, "moneyflow", 'net_mf_vol').fillna(0),
            "moneyflow.net_mf_amount": qu.query_feature_single(code_list, start, end, "moneyflow",
                                                               'net_mf_amount').fillna(0),
        }

        # 开始计算因子
        self.feature_group = {
            "group1": self.calc_feature_1(),
            "gplearn_lv1": self.calc_feature_gplearn_lv1(),
            "gplearn_lv2": self.calc_feature_gplearn_lv2()
        }

    def calc_feature_1(self):
        df_volume_ratio = self.basic_feature['daily_basic.volume']
        df_pe_ttm = self.basic_feature['daily_basic.pe_ttm']
        keep_start = self.keep_start
        df_close_hfq = self.basic_feature['daily_hq.close_hfq']
        df_high_hfq = self.basic_feature['daily_hq.high_hfq']
        df_low_hfq = self.basic_feature['daily_hq.low_hfq']
        # df_open_hfq = self.basic_feature['daily_hq.open_hfq']
        # df_close = self.basic_feature['daily_hq.close']
        # df_high = self.basic_feature['daily_hq.high']
        # df_low = self.basic_feature['daily_hq.low']
        # df_open = self.basic_feature['daily_hq.open']
        # df_volume = self.basic_feature['daily_hq.volume']
        df_circ_mv = self.basic_feature['daily_basic.circ_mv']
        df_turnover_rate_f = self.basic_feature['daily_basic.turnover_rate_f']

        fes = {}
        fes['close'] = self.basic_feature['daily_hq.close']
        fes['free_share'] = self.basic_feature['daily_basic.free_share']
        fes['circ_mv'] = self.basic_feature['daily_basic.circ_mv']
        fes['pe_ttm'] = self.basic_feature['daily_basic.pe_ttm']
        fes['turnover_rate_f'] = self.basic_feature['daily_basic.turnover_rate_f']
        fes['volume'] = self.basic_feature['daily_hq.volume']

        days = [5, 10, 20, 60, 120, 250, 500]

        # # 近期涨停次数
        # print("计算指标-", "近期涨停次数")
        # for day in tqdm(days):
        #     var = qu.cs_rank((df_limit == "U").rolling(day).sum())
        #     feature_name = f'up_limit_times_rank_{day}'
        #     fes[feature_name] = var[keep_start:].copy()
        #     del var
        #     gc.collect()
        #
        # # 近期触板次数
        # print("计算指标-", "近期触板次数")
        # for day in tqdm(days):
        #     var = quant_util.cs_rank(df_is_meet_limit.rolling(day).sum())
        #     feature_name = f'meet_up_limit_times_rank_{day}'
        #     fes[feature_name] = var[keep_start:].copy()
        #     del var
        #     gc.collect()

        # 振幅
        print("计算指标-", "振幅")
        for day in tqdm(days):
            var = qu.cs_rank(((self.basic_feature['daily_hq.close_hfq'] - self.basic_feature['daily_hq.low_hfq']) /
                              self.basic_feature['daily_hq.close_hfq'].shift(1)).rolling(day).mean())
            feature_name = f'amplitude_rank_{day}'
            fes[feature_name] = var[self.keep_start:].copy()
            del var
            gc.collect()

        # 换手率
        print("计算指标-", "换手率")
        for day in tqdm(days):
            var = qu.cs_rank(self.basic_feature['daily_basic.turnover_rate_f'].rolling(day).mean())
            feature_name = f'turnover_rate_f_mean_rank_{day}'
            fes[feature_name] = var[self.keep_start:].copy()
            del var
            gc.collect()

        # 股价在过去的位置水平
        print("计算指标-", "股价在过去的位置水平")
        for day in tqdm(days):
            var = qu.cs_rank(
                (self.basic_feature['daily_hq.close_hfq'] - self.basic_feature['daily_hq.close_hfq'].rolling(
                    day).mean()) / self.basic_feature['daily_hq.close_hfq'].rolling(day).std())
            feature_name = f'close_position_rank_{day}'
            fes[feature_name] = var[self.keep_start:].copy()
            del var
            gc.collect()

        # 空头力道
        print("计算指标-", "空头力道")
        for day in tqdm(days):
            var = qu.cs_rank((self.basic_feature['daily_hq.low_hfq'] - self.basic_feature['daily_hq.close_hfq'].rolling(
                day).mean()) / self.basic_feature['daily_hq.close_hfq'])
            feature_name = f'kong_tou_li_dao_rank_{day}'
            fes[feature_name] = var[self.keep_start:].copy()
            del var
            gc.collect()

        # 布林带
        print("计算指标-", "布林带")
        var = qu.cs_rank(
            qu.BOLL_BAND(self.basic_feature['daily_hq.open_hfq'],
                         self.basic_feature['daily_hq.high_hfq'],
                         self.basic_feature['daily_hq.low_hfq'],
                         self.basic_feature['daily_hq.close_hfq'],
                         self.basic_feature['daily_hq.volume'])[1][2] * -1)
        feature_name = f'boll_band_position_rank'
        fes[feature_name] = var[self.keep_start:].copy()
        del var
        gc.collect()

        # 唐安琪通道
        print("计算指标-", "唐安琪通道")
        var = qu.cs_rank(
            qu.TANGQIAN_BAND(self.basic_feature['daily_hq.open_hfq'],
                             self.basic_feature['daily_hq.high_hfq'],
                             self.basic_feature['daily_hq.low_hfq'],
                             self.basic_feature['daily_hq.close_hfq'],
                             self.basic_feature['daily_hq.volume'])[1][2] * -1)
        feature_name = f'tang_an_qi_band_position_rank'
        fes[feature_name] = var[self.keep_start:].copy()
        del var
        gc.collect()

        # bias
        print("计算指标-", "bias")
        for day in tqdm(days):
            var = qu.cs_rank(
                self.basic_feature['daily_hq.close_hfq'].rolling(day).mean() / self.basic_feature['daily_hq.close_hfq'])
            feature_name = f'bias_rank_{day}'
            fes[feature_name] = var[self.keep_start:].copy()
            del var
            gc.collect()

        # 多头排列
        print("计算指标-", "多头排列")
        var = qu.MA_LONG_SHORT_ORDER(self.basic_feature['daily_hq.open_hfq'],
                                     self.basic_feature['daily_hq.high_hfq'],
                                     self.basic_feature['daily_hq.low_hfq'],
                                     self.basic_feature['daily_hq.close_hfq'],
                                     self.basic_feature['daily_hq.volume'])[1][0] / 100
        feature_name = f'long_order'
        fes[feature_name] = var[self.keep_start:].copy()
        del var
        gc.collect()

        # volume_ratio_mean
        print("计算指标-", "volume_ratio_mean")
        for day in tqdm(days):
            var = qu.cs_rank(df_volume_ratio.rolling(day).mean())
            feature_name = f'volume_ratio_mean_rank_{day}'
            fes[feature_name] = var[self.keep_start:].copy()
            del var
            gc.collect()

        # pe_ttm rank
        print("计算指标-", "df_pe_ttm")
        var = qu.cs_rank(df_pe_ttm)
        feature_name = f'pe_ttm_rank'
        fes[feature_name] = var[keep_start:].copy()
        del var
        gc.collect()

        # 动量
        print("计算指标-", "动量")
        for day in tqdm(days):
            var = qu.cs_rank(df_close_hfq.pct_change(day))
            feature_name = f'momentum_rank_{day}'
            fes[feature_name] = var[keep_start:].copy()
            del var
            gc.collect()

        # cyf
        print("计算指标-", "cyf")
        for day in days:
            var = qu.cs_rank(100 - 100 / (1 + df_turnover_rate_f.rolling(day).mean()))
            feature_name = f'cyf_rank_{day}'
            fes[feature_name] = var[keep_start:].copy()
            del var
            gc.collect()

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
        var = qu.cs_rank(B6)
        feature_name = f'tdx_zhulikongpanxishu_rank'
        fes[feature_name] = var[keep_start:].copy()
        del var
        gc.collect()

        # 市值 rank
        print("计算指标-", "df_circ_mv")
        var = qu.cs_rank(df_circ_mv)
        feature_name = f'circ_mv_rank'
        fes[feature_name] = var[keep_start:].copy()
        del var
        gc.collect()

        # vwap_daily
        # print("计算指标-", "vwap_daily")
        # for day in days:
        #     var = (((df_close + df_high + df_low) / 3 * df_volume).rolling(day).sum() / df_volume.rolling(
        #         day).sum()) / df_up_limit
        #     var = qu.cs_rank(var)
        #     feature_name = f'vwap_to_up_limit_rank_{day}'
        #     fes[feature_name] = var[keep_start:].copy()
        #     del var
        #     gc.collect()
        return fes

    def calc_feature_gplearn_lv1(self):
        need_feature_expressions = ['ts_max(daily_hq.pct_chg,10)',
                                    'ts_std(moneyflow.buy_elg_amount,10)',
                                    'ts_var(moneyflow.buy_elg_amount,10)',
                                    'ts_cov(moneyflow.buy_elg_amount,moneyflow.buy_elg_amount,10)',
                                    'ts_max(moneyflow.buy_elg_amount,10)',
                                    'ts_std(moneyflow.buy_elg_amount,5)',
                                    'ts_var(moneyflow.buy_elg_amount,5)',
                                    'ts_cov(daily_hq.pct_chg,moneyflow.buy_elg_amount,10)',
                                    'ts_max(moneyflow.buy_elg_amount,5)',
                                    'ts_cov(daily_basic.volume,moneyflow.buy_elg_amount,10)',
                                    'ts_max(daily_hq.pct_chg,20)',
                                    'ts_mean(moneyflow.buy_elg_amount,5)',
                                    'ts_sum(moneyflow.buy_elg_amount,5)',
                                    'ts_mean(moneyflow.buy_elg_amount,10)',
                                    'ts_sum(moneyflow.buy_elg_amount,10)',
                                    'div(moneyflow.buy_elg_amount,moneyflow.sell_lg_vol)',
                                    'ts_std(moneyflow.buy_lg_amount,5)',
                                    'div(moneyflow.buy_lg_vol,moneyflow.buy_elg_amount)',
                                    'ts_var(moneyflow.buy_lg_amount,5)',
                                    'cs_rank(moneyflow.buy_elg_amount)',
                                    'abs(moneyflow.buy_elg_amount)', 'sqrt(moneyflow.buy_elg_amount)',
                                    'inv(moneyflow.buy_elg_amount)',
                                    'add(moneyflow.buy_elg_amount,express.express_diluted_eps)',
                                    'add(express.express_diluted_eps,moneyflow.buy_elg_amount)',
                                    'cs_orthogonalize(moneyflow.buy_elg_amount,express.express_n_income)',
                                    'div(daily_hq.volume,moneyflow.buy_elg_amount)',
                                    'sub(moneyflow.buy_elg_amount,daily_basic.turnover_rate)',
                                    'sub(daily_basic.turnover_rate,moneyflow.buy_elg_amount)',
                                    'add(top_list.reason_is_contain_diefu,moneyflow.buy_elg_amount)',
                                    'cs_orthogonalize(moneyflow.buy_elg_amount,express.express_total_hldr_eqy_exc_min_int)',
                                    'ts_cov(moneyflow.buy_elg_amount,moneyflow.sell_lg_amount,10)',
                                    'mul(daily_basic.volume,moneyflow.buy_elg_amount)',
                                    'ts_max(moneyflow.buy_elg_amount,20)',
                                    'div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol)',
                                    'sub(express.express_total_profit,moneyflow.buy_elg_amount)',
                                    'div(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount)',
                                    'div(moneyflow.buy_elg_vol,moneyflow.sell_sm_vol)',
                                    'ts_zscore(daily_hq.close_hfq,120)',
                                    'sub(express.express_revenue,moneyflow.buy_elg_amount)',
                                    'sub(moneyflow.buy_elg_amount,express.express_total_assets)',
                                    'ts_backward_pct_chg(daily_hq.close,10)',
                                    'ts_std(daily_hq.amount,5)', 'cs_zscore(moneyflow.buy_elg_amount)',
                                    'ts_var(daily_hq.amount,5)',
                                    'add(moneyflow.buy_elg_amount,daily_hq.close)',
                                    'mul(daily_hq.close,moneyflow.buy_elg_amount)',
                                    'ts_std(moneyflow.buy_elg_amount,20)',
                                    'ts_var(moneyflow.buy_elg_amount,20)',
                                    'ts_delta(daily_hq.close,10)', 'ts_zscore(daily_hq.close,20)',
                                    'ts_zscore(daily_hq.close_hfq,60)',
                                    'div(moneyflow.buy_lg_amount,moneyflow.buy_sm_amount)',
                                    'div(moneyflow.buy_sm_amount,moneyflow.buy_lg_amount)',
                                    'ts_backward_pct_chg(daily_basic.total_mv,10)',
                                    'mul(moneyflow.buy_elg_amount,daily_basic.turnover_rate_f)',
                                    'mul(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount)',
                                    'ts_zscore(daily_basic.total_mv,20)',
                                    'ts_zscore(daily_basic.circ_mv,20)',
                                    'ts_var(moneyflow.buy_lg_amount,10)',
                                    'div(moneyflow.buy_elg_amount,daily_basic.volume)',
                                    'div(moneyflow.buy_elg_vol,moneyflow.sell_md_vol)',
                                    'add(moneyflow.buy_elg_amount,daily_hq.high_hfq)',
                                    'add(daily_hq.low_hfq,moneyflow.buy_elg_amount)',
                                    'add(moneyflow.buy_elg_amount,daily_hq.open_hfq)',
                                    'ts_delta(daily_hq.close_hfq,10)', 'ts_zscore(daily_hq.close,120)',
                                    'mul(daily_basic.turnover_rate,moneyflow.buy_elg_amount)',
                                    'add(daily_basic.pb,moneyflow.buy_elg_amount)',
                                    'div(moneyflow.buy_md_vol,moneyflow.buy_elg_vol)',
                                    'ts_std(moneyflow.sell_elg_amount,5)',
                                    'ts_std(moneyflow.sell_md_amount,5)',
                                    'ts_var(moneyflow.sell_md_amount,5)',
                                    'ts_var(moneyflow.sell_elg_amount,5)',
                                    'mul(moneyflow.sell_elg_amount,moneyflow.buy_elg_amount)',
                                    'ts_max(moneyflow.buy_lg_amount,5)',
                                    'ts_cov(moneyflow.buy_elg_amount,daily_hq.amount,5)',
                                    'div(daily_basic.turnover_rate,moneyflow.buy_elg_amount)',
                                    'ts_zscore(daily_hq.close_hfq,250)',
                                    'div(daily_basic.total_share,moneyflow.buy_elg_amount)',
                                    'add(moneyflow.buy_elg_amount,daily_basic.ps)',
                                    'ts_zscore(daily_hq.close,60)', 'ts_mean(daily_hq.pct_chg,20)',
                                    'ts_zscore(daily_basic.circ_mv,60)',
                                    'ts_zscore(daily_basic.total_mv,60)',
                                    'ts_zscore(daily_basic.circ_mv,120)',
                                    'ts_var(moneyflow.sell_elg_amount,10)',
                                    'div(moneyflow.buy_elg_amount,daily_basic.float_share)',
                                    'mul(moneyflow.buy_elg_amount,daily_basic.pb)',
                                    'ts_backward_pct_chg(daily_basic.pb,10)',
                                    'ts_zscore(daily_hq.high_hfq,20)',
                                    'ts_backward_pct_chg(daily_basic.ps,10)',
                                    'ts_max(moneyflow.sell_elg_amount,10)',
                                    'add(daily_hq.pct_chg,daily_hq.close)',
                                    'cs_orthogonalize(moneyflow.buy_lg_amount,moneyflow.net_mf_vol)',
                                    'ts_max(moneyflow.buy_lg_amount,10)',
                                    'ts_zscore(daily_basic.ps,20)',
                                    'ts_std(moneyflow.sell_lg_amount,10)',
                                    'ts_var(moneyflow.sell_lg_amount,10)',
                                    'ts_std(daily_hq.amount,10)', 'ts_var(daily_hq.amount,10)',
                                    'ts_delta(daily_basic.pb,10)', 'ts_zscore(daily_hq.high_hfq,60)',
                                    'ts_std(moneyflow.buy_md_amount,5)',
                                    'ts_var(moneyflow.buy_md_amount,5)',
                                    'ts_backward_pct_chg(daily_hq.high_hfq,10)',
                                    'ts_zscore(daily_basic.circ_mv,250)',
                                    'ts_zscore(daily_basic.total_mv,250)',
                                    'div(moneyflow.buy_md_vol,moneyflow.sell_elg_amount)',
                                    'ts_delta(daily_basic.total_mv,10)',
                                    'ts_zscore(daily_basic.pb,20)', 'ts_mean(daily_hq.pct_chg,5)',
                                    'ts_sum(daily_hq.pct_chg,5)', 'ts_max(moneyflow.sell_lg_amount,5)',
                                    'div(moneyflow.buy_md_vol,daily_hq.amount)',
                                    'ts_cov(daily_basic.turnover_rate,moneyflow.buy_elg_amount,5)',
                                    'div(moneyflow.sell_sm_vol,daily_hq.amount)',
                                    'div(daily_hq.amount,moneyflow.sell_sm_vol)',
                                    'mul(daily_basic.total_mv,moneyflow.buy_elg_amount)',
                                    'add(moneyflow.sell_elg_amount,moneyflow.buy_lg_amount)',
                                    'ts_max(daily_hq.amount,5)',
                                    'mul(moneyflow.buy_elg_amount,daily_basic.ps_ttm)',
                                    'ts_max(moneyflow.buy_elg_vol,10)',
                                    'cs_rank(moneyflow.buy_lg_amount)',
                                    'ts_zscore(daily_hq.close,250)',
                                    'mul(moneyflow.buy_elg_amount,moneyflow.buy_lg_vol)',
                                    'mul(moneyflow.buy_lg_vol,moneyflow.buy_elg_amount)',
                                    'cs_zscore(moneyflow.buy_lg_amount)',
                                    'ts_backward_pct_chg(daily_basic.ps_ttm,10)',
                                    'add(moneyflow.buy_elg_vol,moneyflow.buy_lg_amount)',
                                    'mul(moneyflow.sell_elg_amount,moneyflow.buy_elg_vol)',
                                    'ts_var(moneyflow.sell_md_amount,10)',
                                    'mul(moneyflow.buy_elg_amount,moneyflow.sell_elg_vol)',
                                    'ts_cov(moneyflow.sell_lg_amount,moneyflow.buy_elg_vol,10)',
                                    'div(moneyflow.sell_elg_amount,moneyflow.sell_sm_vol)',
                                    'sub(moneyflow.buy_elg_amount,daily_basic.ps)',
                                    'ts_max(moneyflow.sell_lg_amount,10)',
                                    'add(express.express_total_hldr_eqy_exc_min_int,moneyflow.buy_lg_amount)',
                                    'ts_std(moneyflow.buy_elg_vol,10)',
                                    'ts_zscore(daily_basic.ps_ttm,20)',
                                    'ts_delta(daily_hq.close_hfq,20)',
                                    'add(daily_hq.pct_chg,moneyflow.buy_lg_amount)',
                                    'ts_mean(moneyflow.sell_elg_amount,5)',
                                    'abs(moneyflow.buy_lg_amount)', 'log(moneyflow.buy_lg_amount)',
                                    'sqrt(moneyflow.buy_lg_amount)',
                                    'sub(express.express_diluted_eps,moneyflow.buy_lg_amount)',
                                    'ts_delta(daily_hq.close,5)',
                                    'sub(moneyflow.buy_lg_amount,daily_basic.turnover_rate)',
                                    'sub(moneyflow.buy_lg_amount,daily_hq.pct_chg)',
                                    'mul(moneyflow.sell_elg_amount,daily_basic.volume)',
                                    'mul(daily_basic.volume,moneyflow.sell_elg_amount)',
                                    'ts_sum(moneyflow.sell_elg_amount,5)',
                                    'mul(moneyflow.sell_elg_amount,moneyflow.buy_lg_amount)',
                                    'ts_skew(daily_hq.pct_chg,10)',
                                    'cs_orthogonalize(moneyflow.buy_lg_amount,express.express_diluted_eps)',
                                    'ts_backward_pct_chg(daily_hq.close,20)',
                                    'cs_orthogonalize(moneyflow.buy_elg_amount,daily_hq.low_hfq)',
                                    'ts_zscore(daily_basic.ps,60)',
                                    'div(moneyflow.sell_elg_amount,moneyflow.sell_md_vol)',
                                    'ts_backward_pct_chg(daily_hq.close_hfq,5)',
                                    'cs_orthogonalize(moneyflow.buy_lg_amount,express.express_total_profit)',
                                    'cs_orthogonalize(moneyflow.buy_lg_amount,express.express_revenue)',
                                    'add(moneyflow.sell_sm_amount,moneyflow.buy_elg_amount)',
                                    'sub(moneyflow.buy_lg_amount,daily_basic.pe_ttm)',
                                    'cs_orthogonalize(moneyflow.buy_elg_amount,daily_basic.free_share)',
                                    'ts_cov(moneyflow.sell_lg_amount,daily_basic.turnover_rate_f,10)',
                                    'add(moneyflow.sell_lg_amount,moneyflow.sell_elg_amount)',
                                    'sub(moneyflow.buy_lg_amount,express.express_n_income)',
                                    'ts_max(daily_hq.amount,10)',
                                    'sub(moneyflow.buy_lg_amount,top_list.reason_is_contain_zhangfu)',
                                    'ts_cov(moneyflow.buy_elg_amount,moneyflow.sell_elg_vol,5)',
                                    'ts_delta(daily_hq.close,20)', 'ts_zscore(daily_basic.pb,60)',
                                    'mul(daily_hq.close,moneyflow.sell_lg_amount)',
                                    'ts_std(moneyflow.sell_sm_amount,5)',
                                    'mul(moneyflow.sell_lg_amount,daily_basic.volume)',
                                    'mul(daily_basic.volume,moneyflow.sell_lg_amount)',
                                    'ts_var(moneyflow.sell_sm_amount,5)',
                                    'ts_zscore(daily_hq.low_hfq,120)',
                                    'add(moneyflow.buy_elg_vol,moneyflow.buy_elg_amount)',
                                    'ts_max(moneyflow.buy_elg_vol,5)',
                                    'div(moneyflow.sell_md_amount,moneyflow.buy_sm_amount)',
                                    'div(moneyflow.buy_sm_amount,moneyflow.sell_md_amount)',
                                    'sub(moneyflow.buy_sm_vol,moneyflow.buy_lg_vol)',
                                    'sub(express.express_revenue,moneyflow.buy_lg_amount)',
                                    'mul(moneyflow.buy_elg_vol,moneyflow.sell_sm_amount)',
                                    'ts_max(moneyflow.sell_md_amount,5)',
                                    'mul(moneyflow.sell_lg_amount,moneyflow.sell_elg_amount)',
                                    'mul(moneyflow.sell_elg_amount,moneyflow.sell_lg_amount)',
                                    'ts_delta(daily_basic.ps,10)',
                                    'div(moneyflow.buy_sm_vol,moneyflow.sell_elg_vol)',
                                    'add(moneyflow.buy_elg_vol,moneyflow.sell_elg_amount)',
                                    'mul(daily_hq.amount,moneyflow.sell_elg_amount)',
                                    'mul(moneyflow.sell_elg_amount,daily_hq.amount)',
                                    'ts_zscore(daily_basic.pb,120)',
                                    'mul(moneyflow.buy_elg_amount,moneyflow.buy_md_vol)',
                                    'ts_var(moneyflow.buy_elg_vol,5)',
                                    'div(moneyflow.buy_lg_amount,moneyflow.buy_md_amount)',
                                    'ts_mean(moneyflow.buy_lg_amount,5)',
                                    'ts_sum(moneyflow.buy_lg_amount,5)',
                                    'ts_delta(moneyflow.buy_elg_amount,250)',
                                    'ts_mean(moneyflow.buy_elg_amount,20)',
                                    'cs_rank(moneyflow.sell_lg_amount)',
                                    'ts_sum(moneyflow.buy_elg_amount,20)',
                                    'cs_zscore(daily_hq.amount)',
                                    'cs_zscore(moneyflow.sell_lg_amount)',
                                    'ts_backward_pct_chg(daily_basic.total_mv,5)',
                                    'ts_backward_pct_chg(daily_basic.circ_mv,5)',
                                    'add(moneyflow.sell_elg_amount,express.express_diluted_roe)',
                                    'add(express.express_diluted_roe,moneyflow.sell_elg_amount)',
                                    'inv(moneyflow.sell_elg_amount)', 'abs(moneyflow.sell_elg_amount)',
                                    'sqrt(moneyflow.sell_elg_amount)',
                                    'mul(moneyflow.sell_elg_amount,moneyflow.sell_elg_amount)',
                                    'log(moneyflow.sell_elg_amount)',
                                    'cs_rank(moneyflow.sell_elg_amount)',
                                    'ts_zscore(daily_basic.ps,120)',
                                    'add(moneyflow.sell_elg_amount,express.express_total_profit)',
                                    'add(express.express_operate_profit,moneyflow.sell_elg_amount)',
                                    'add(express.express_n_income,moneyflow.sell_elg_amount)',
                                    'ts_std(moneyflow.buy_md_amount,10)',
                                    'cs_orthogonalize(moneyflow.sell_elg_amount,express.express_diluted_roe)',
                                    'cs_rank(moneyflow.buy_elg_vol)',
                                    'mul(moneyflow.sell_sm_amount,moneyflow.sell_elg_amount)',
                                    'mul(moneyflow.sell_elg_amount,moneyflow.sell_sm_amount)',
                                    'cs_orthogonalize(moneyflow.sell_elg_amount,express.express_operate_profit)',
                                    'ts_sum(moneyflow.sell_elg_amount,10)',
                                    'add(express.express_yoy_net_profit,moneyflow.sell_lg_amount)',
                                    'mul(daily_basic.volume,daily_hq.amount)',
                                    'mul(daily_hq.amount,daily_basic.volume)',
                                    'add(moneyflow.buy_elg_vol,moneyflow.sell_sm_amount)',
                                    'add(moneyflow.sell_lg_amount,daily_basic.turnover_rate_f)',
                                    'ts_cov(daily_hq.amount,moneyflow.buy_elg_vol,5)',
                                    'add(express.express_diluted_roe,moneyflow.sell_lg_amount)',
                                    'add(express.express_diluted_eps,moneyflow.sell_lg_amount)',
                                    'add(moneyflow.sell_lg_amount,express.express_diluted_eps)',
                                    'log(moneyflow.sell_lg_amount)', 'inv(moneyflow.sell_lg_amount)',
                                    'sqrt(moneyflow.sell_lg_amount)', 'abs(moneyflow.sell_lg_amount)',
                                    'sub(express.express_diluted_eps,moneyflow.sell_lg_amount)',
                                    'sub(moneyflow.sell_lg_amount,express.express_diluted_roe)',
                                    'sub(moneyflow.sell_lg_amount,daily_basic.turnover_rate_f)',
                                    'sub(daily_basic.turnover_rate_f,moneyflow.sell_lg_amount)',
                                    'sub(moneyflow.sell_lg_amount,daily_basic.turnover_rate)',
                                    'sub(daily_basic.volume,moneyflow.sell_lg_amount)',
                                    'add(express.express_revenue,moneyflow.buy_elg_vol)',
                                    'mul(daily_basic.volume,moneyflow.buy_elg_vol)',
                                    'sub(moneyflow.buy_elg_vol,express.express_diluted_roe)',
                                    'sqrt(moneyflow.buy_elg_vol)', 'inv(moneyflow.buy_elg_vol)',
                                    'abs(moneyflow.buy_elg_vol)',
                                    'cs_orthogonalize(moneyflow.sell_elg_amount,express.express_total_hldr_eqy_exc_min_int)',
                                    'cs_orthogonalize(moneyflow.sell_lg_amount,express.express_diluted_roe)',
                                    'cs_rank(daily_hq.amount)',
                                    'mul(daily_hq.amount,moneyflow.sell_lg_amount)',
                                    'mul(moneyflow.sell_lg_amount,daily_hq.amount)',
                                    'sub(daily_basic.turnover_rate_f,moneyflow.buy_elg_vol)',
                                    'add(daily_basic.pe_ttm,moneyflow.sell_lg_amount)',
                                    'add(moneyflow.sell_lg_amount,daily_basic.pe_ttm)',
                                    'ts_backward_pct_chg(daily_basic.total_mv,20)',
                                    'ts_backward_pct_chg(daily_basic.circ_mv,20)',
                                    'ts_zscore(daily_hq.close_hfq,500)',
                                    'sub(moneyflow.sell_elg_amount,top_list.reason_is_contain_diefu)',
                                    'ts_backward_pct_chg(daily_basic.ps,5)',
                                    'add(moneyflow.sell_md_amount,moneyflow.sell_elg_amount)',
                                    'sub(top_list.reason_is_contain_zhangfu,moneyflow.sell_elg_amount)',
                                    'ts_zscore(daily_hq.low_hfq,250)',
                                    'add(express.express_total_profit,moneyflow.buy_elg_vol)',
                                    'add(moneyflow.buy_elg_vol,express.express_operate_profit)',
                                    'mul(daily_basic.turnover_rate,moneyflow.buy_elg_vol)',
                                    'mul(moneyflow.buy_elg_vol,daily_basic.turnover_rate)',
                                    'mul(daily_basic.turnover_rate_f,moneyflow.sell_elg_amount)',
                                    'sub(express.express_revenue,moneyflow.sell_elg_amount)',
                                    'sub(express.express_total_assets,moneyflow.sell_elg_amount)',
                                    'add(daily_hq.pct_chg,moneyflow.buy_elg_vol)',
                                    'ts_delta(daily_hq.high_hfq,20)',
                                    'add(daily_hq.amount,express.express_total_profit)',
                                    'add(daily_hq.amount,express.express_operate_profit)',
                                    'ts_zscore(daily_hq.low_hfq,20)',
                                    'sub(moneyflow.buy_md_amount,moneyflow.buy_sm_amount)',
                                    'ts_std(moneyflow.net_mf_amount,5)',
                                    'sub(moneyflow.sell_md_vol,daily_hq.amount)',
                                    'sub(daily_hq.amount,moneyflow.sell_md_vol)',
                                    'sub(daily_hq.amount,moneyflow.sell_lg_vol)',
                                    'sub(daily_hq.amount,moneyflow.sell_elg_vol)',
                                    'add(moneyflow.buy_elg_amount,daily_hq.amount)',
                                    'add(moneyflow.sell_elg_amount,daily_hq.amount)',
                                    'sub(daily_hq.amount,moneyflow.buy_md_amount)',
                                    'sub(daily_basic.pe_ttm,daily_hq.amount)',
                                    'add(moneyflow.net_mf_amount,daily_hq.amount)',
                                    'add(daily_hq.amount,moneyflow.net_mf_vol)',
                                    'add(moneyflow.net_mf_vol,daily_hq.amount)',
                                    'sub(daily_hq.amount,daily_basic.turnover_rate)',
                                    'sub(express.express_diluted_roe,daily_hq.amount)',
                                    'log(daily_hq.amount)', 'inv(daily_hq.amount)',
                                    'add(daily_hq.amount,daily_basic.turnover_rate_f)',
                                    'sub(express.express_diluted_eps,daily_hq.amount)']

        fes = {}
        for expression in need_feature_expressions:
            var = qu.process_expression(expression, "self.basic_feature", "self.basic_operators")
            print(expression, "-->", var)
            vardf = eval(var)
            fes[expression] = vardf[self.keep_start:].copy()
            del vardf

        return fes

    def calc_feature_gplearn_lv2(self):
        need_feature_expressions = ['log(ts_cov(daily_hq.pct_chg,moneyflow.buy_elg_amount,10))',
                                    'ts_max(cs_rank(daily_hq.pct_chg),10)',
                                    'sqrt(ts_max(daily_hq.pct_chg,10))',
                                    'inv(ts_max(daily_hq.pct_chg,10))',
                                    'abs(ts_max(daily_hq.pct_chg,10))',
                                    'abs(ts_cov(daily_hq.pct_chg,moneyflow.buy_elg_amount,10))',
                                    'ts_max(cs_orthogonalize(daily_hq.pct_chg,factor_adj.adj_factor),10)',
                                    'ts_std(mul(daily_basic.volume,moneyflow.buy_elg_amount),10)',
                                    'ts_std(ts_std(moneyflow.buy_elg_amount,5),5)',
                                    'ts_std(cs_zscore(moneyflow.buy_elg_amount),10)',
                                    'sqrt(ts_cov(daily_basic.volume,moneyflow.buy_elg_amount,10))',
                                    'ts_max(cs_orthogonalize(daily_hq.pct_chg,daily_basic.dv_ratio),10)',
                                    'ts_max(ts_zscore(daily_hq.pct_chg,250),10)',
                                    'cs_rank(ts_std(moneyflow.buy_elg_amount,10))',
                                    'cs_rank(ts_var(moneyflow.buy_elg_amount,10))',
                                    'abs(ts_var(moneyflow.buy_elg_amount,10))',
                                    'log(ts_var(moneyflow.buy_elg_amount,5))',
                                    'log(ts_cov(moneyflow.buy_elg_amount,moneyflow.buy_elg_amount,10))',
                                    'ts_var(add(express.express_diluted_eps,moneyflow.buy_elg_amount),10)',
                                    'inv(ts_max(moneyflow.buy_elg_amount,10))',
                                    'ts_max(add(top_list.reason_is_contain_diefu,moneyflow.buy_elg_amount),10)',
                                    'sqrt(ts_var(moneyflow.buy_elg_amount,10))',
                                    'add(ts_var(moneyflow.buy_elg_amount,5),ts_max(moneyflow.sell_lg_amount,10))',
                                    'abs(ts_cov(daily_basic.volume,moneyflow.buy_elg_amount,10))',
                                    'sub(ts_var(moneyflow.buy_elg_amount,10),express.express_total_assets)',
                                    'abs(ts_var(moneyflow.buy_elg_amount,5))',
                                    'log(ts_std(moneyflow.buy_elg_amount,5))',
                                    'inv(ts_std(moneyflow.buy_elg_amount,5))',
                                    'abs(ts_std(moneyflow.buy_elg_amount,5))',
                                    'ts_var(add(top_list.reason_is_contain_diefu,moneyflow.buy_elg_amount),5)',
                                    'ts_corr(add(moneyflow.buy_elg_amount,moneyflow.buy_md_vol),moneyflow.buy_md_vol,20)',
                                    'ts_max(cs_rank(moneyflow.buy_elg_amount),5)',
                                    'cs_rank(ts_max(moneyflow.buy_elg_amount,5))',
                                    'sub(ts_max(moneyflow.buy_elg_amount,5),express.express_diluted_eps)',
                                    'inv(ts_max(moneyflow.buy_elg_amount,5))',
                                    'cs_rank(ts_cov(daily_hq.pct_chg,moneyflow.buy_elg_amount,10))',
                                    'cs_zscore(ts_std(moneyflow.buy_elg_amount,5))',
                                    'ts_std(div(moneyflow.buy_elg_vol,moneyflow.sell_md_vol),10)',
                                    'ts_var(mul(daily_hq.close,moneyflow.buy_elg_amount),5)',
                                    'ts_min(sub(express.express_total_profit,moneyflow.buy_elg_amount),5)',
                                    'cs_zscore(ts_backward_pct_chg(daily_hq.close,10))',
                                    'ts_var(div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol),5)',
                                    'mul(ts_count(daily_basic.pb,60),ts_cov(daily_basic.volume,moneyflow.buy_elg_amount,10))',
                                    'ts_max(ts_cov(moneyflow.buy_elg_amount,daily_hq.amount,5),5)',
                                    'cs_rank(ts_cov(daily_basic.volume,moneyflow.buy_elg_amount,10))',
                                    'ts_sum(div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol),10)',
                                    'sqrt(ts_cov(daily_basic.turnover_rate,moneyflow.buy_elg_amount,5))',
                                    'log(ts_cov(daily_basic.turnover_rate,moneyflow.buy_elg_amount,5))',
                                    'inv(ts_max(daily_hq.pct_chg,20))',
                                    'log(ts_max(daily_hq.pct_chg,20))',
                                    'sigmoid(ts_max(daily_hq.pct_chg,20))',
                                    'ts_max(sub(daily_hq.pct_chg,daily_basic.dv_ttm),10)',
                                    'add(ts_var(moneyflow.buy_elg_amount,10),ts_zscore(daily_hq.open_hfq,250))',
                                    'ts_std(add(moneyflow.buy_elg_amount,daily_hq.open_hfq),10)',
                                    'ts_std(add(daily_hq.low_hfq,moneyflow.buy_elg_amount),10)',
                                    'ts_var(cs_orthogonalize(moneyflow.buy_elg_amount,daily_basic.total_mv),5)',
                                    'cs_rank(ts_backward_pct_chg(daily_basic.total_mv,10))',
                                    'ts_max(add(daily_basic.pb,moneyflow.buy_elg_amount),10)',
                                    'ts_min(sub(moneyflow.buy_sm_amount,moneyflow.buy_lg_amount),10)',
                                    'ts_zscore(cs_rank(daily_basic.ps),20)',
                                    'mul(ts_var(moneyflow.buy_elg_amount,10),daily_hq.low_hfq)',
                                    'cs_rank(ts_mean(daily_hq.pct_chg,20))',
                                    'sub(ts_min(daily_hq.open_hfq,10),daily_hq.close_hfq)',
                                    'cs_zscore(ts_mean(daily_hq.pct_chg,20))',
                                    'abs(ts_cov(moneyflow.buy_elg_amount,daily_hq.amount,5))',
                                    'cs_rank(ts_mean(moneyflow.buy_elg_amount,5))',
                                    'cs_rank(ts_max(daily_hq.pct_chg,20))',
                                    'mul(ts_max(daily_hq.amount,10),ts_max(moneyflow.buy_elg_amount,10))',
                                    'cs_zscore(ts_zscore(daily_basic.total_mv,60))',
                                    'cs_zscore(ts_zscore(daily_basic.circ_mv,60))',
                                    'cs_rank(ts_sum(moneyflow.buy_elg_amount,5))',
                                    'add(ts_std(moneyflow.buy_elg_amount,5),daily_hq.low_hfq)',
                                    'cs_rank(ts_zscore(daily_basic.total_mv,60))',
                                    'ts_var(cs_orthogonalize(moneyflow.buy_elg_amount,moneyflow.sell_lg_amount),5)',
                                    'log(ts_mean(moneyflow.buy_elg_amount,5))',
                                    'abs(ts_mean(moneyflow.buy_elg_amount,5))',
                                    'sqrt(ts_mean(moneyflow.buy_elg_amount,5))',
                                    'div(cs_orthogonalize(moneyflow.buy_sm_vol,moneyflow.buy_lg_amount),moneyflow.buy_md_amount)',
                                    'ts_var(mul(moneyflow.sell_elg_amount,moneyflow.buy_elg_amount),5)',
                                    'inv(ts_var(moneyflow.buy_elg_amount,10))',
                                    'ts_var(div(moneyflow.buy_elg_amount,daily_basic.float_share),10)',
                                    'ts_std(cs_orthogonalize(factor_adj.adj_factor,moneyflow.buy_elg_amount),5)',
                                    'div(mul(daily_basic.total_mv,moneyflow.buy_elg_amount),moneyflow.sell_sm_vol)',
                                    'div(sub(daily_hq.volume,express.express_n_income),ts_var(moneyflow.buy_elg_amount,10))',
                                    'ts_max(cs_zscore(daily_hq.pct_chg),20)',
                                    'ts_zscore(ts_max(moneyflow.buy_elg_vol,10),500)',
                                    'ts_sum(sub(daily_hq.pct_chg,top_list.reason_is_contain_zhangfu),10)',
                                    'mul(div(moneyflow.sell_md_amount,moneyflow.sell_md_vol),ts_max(moneyflow.buy_elg_vol,5))',
                                    'cs_rank(ts_backward_pct_chg(daily_basic.ps,10))',
                                    'ts_zscore(ts_std(moneyflow.buy_elg_vol,10),500)',
                                    'ts_mean(cs_orthogonalize(daily_hq.pct_chg,moneyflow.sell_elg_vol),10)',
                                    'div(ts_std(moneyflow.buy_elg_amount,5),add(moneyflow.buy_elg_amount,moneyflow.sell_lg_vol))',
                                    'mul(ts_max(moneyflow.buy_elg_vol,5),daily_hq.close)',
                                    'cs_orthogonalize(ts_max(moneyflow.buy_elg_amount,10),sub(express.express_revenue,daily_basic.pb))',
                                    'ts_backward_pct_chg(cs_rank(daily_hq.close),10)',
                                    'ts_std(div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol),20)',
                                    'ts_max(cs_orthogonalize(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol),20)',
                                    'ts_max(mul(daily_basic.volume,daily_hq.pct_chg),20)',
                                    'cs_rank(ts_sum(moneyflow.buy_elg_amount,10))',
                                    'ts_max(cs_orthogonalize(daily_hq.pct_chg,moneyflow.buy_elg_vol),20)',
                                    'log(ts_var(moneyflow.buy_lg_amount,5))',
                                    'sqrt(ts_var(moneyflow.buy_lg_amount,5))',
                                    'abs(ts_cov(daily_basic.turnover_rate,moneyflow.buy_elg_amount,5))',
                                    'ts_var(mul(moneyflow.buy_elg_amount,daily_basic.pb),5)',
                                    'cs_zscore(ts_backward_pct_chg(daily_basic.ps,10))',
                                    'add(ts_count(daily_basic.total_mv,120),moneyflow.buy_elg_amount)',
                                    'ts_mean(cs_orthogonalize(daily_hq.pct_chg,daily_basic.dv_ratio),10)',
                                    'mul(cs_orthogonalize(moneyflow.sell_md_amount,daily_basic.float_share),div(moneyflow.buy_elg_amount,moneyflow.sell_lg_vol))',
                                    'ts_mean(cs_orthogonalize(daily_hq.pct_chg,daily_basic.total_mv),10)',
                                    'cs_rank(ts_backward_pct_chg(daily_hq.close,20))',
                                    'cs_rank(ts_backward_pct_chg(daily_basic.pb,10))',
                                    'ts_sum(ts_max(daily_hq.pct_chg,10),5)',
                                    'inv(ts_mean(moneyflow.buy_elg_amount,10))',
                                    'ts_var(mul(daily_basic.turnover_rate,moneyflow.buy_elg_amount),5)',
                                    'ts_std(sqrt(daily_hq.amount),5)',
                                    'sigmoid(div(moneyflow.buy_elg_amount,moneyflow.sell_lg_vol))',
                                    'abs(div(moneyflow.buy_elg_amount,moneyflow.sell_lg_vol))',
                                    'log(ts_sum(moneyflow.buy_elg_amount,10))',
                                    'ts_mean(add(top_list.reason_is_contain_diefu,moneyflow.buy_elg_amount),10)',
                                    'ts_var(cs_orthogonalize(moneyflow.buy_lg_amount,moneyflow.buy_elg_vol),5)',
                                    'ts_std(add(daily_hq.pct_chg,moneyflow.buy_lg_amount),5)',
                                    'div(add(moneyflow.buy_elg_vol,moneyflow.sell_elg_amount),moneyflow.sell_sm_vol)',
                                    'ts_mean(sub(daily_basic.turnover_rate,moneyflow.buy_elg_amount),10)',
                                    'log(ts_std(moneyflow.buy_lg_amount,5))',
                                    'abs(ts_std(moneyflow.buy_lg_amount,5))',
                                    'cs_rank(ts_backward_pct_chg(daily_hq.high_hfq,10))',
                                    'inv(div(moneyflow.buy_lg_vol,moneyflow.buy_elg_amount))',
                                    'cs_rank(ts_mean(daily_hq.pct_chg,5))',
                                    'sub(ts_std(moneyflow.buy_lg_amount,5),ts_count(daily_hq.close_hfq,10))',
                                    'ts_mean(mul(moneyflow.sell_elg_amount,moneyflow.buy_elg_amount),5)',
                                    'ts_var(cs_zscore(daily_hq.amount),5)',
                                    'div(add(moneyflow.buy_elg_vol,moneyflow.buy_lg_amount),add(top_list.reason_is_contain_zhangfu,daily_hq.volume))',
                                    'cs_orthogonalize(ts_min(daily_basic.total_mv,20),sub(daily_basic.circ_mv,moneyflow.sell_lg_vol))',
                                    'mul(ts_sum(moneyflow.buy_elg_amount,5),moneyflow.buy_elg_amount)',
                                    'cs_zscore(sqrt(moneyflow.buy_elg_amount))',
                                    'cs_rank(abs(moneyflow.buy_elg_amount))',
                                    'sqrt(cs_rank(moneyflow.buy_elg_amount))',
                                    'inv(cs_rank(moneyflow.buy_elg_amount))',
                                    'cs_rank(sqrt(moneyflow.buy_elg_amount))',
                                    'cs_rank(cs_zscore(moneyflow.buy_elg_amount))',
                                    'ts_max(abs(daily_hq.pct_chg),10)',
                                    'mul(ts_max(moneyflow.sell_elg_amount,10),div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol))',
                                    'cs_rank(ts_zscore(daily_hq.close,120))',
                                    'abs(cs_orthogonalize(moneyflow.buy_elg_amount,express.express_n_income))',
                                    'abs(ts_cov(moneyflow.buy_elg_amount,daily_hq.close_hfq,5))',
                                    'add(abs(express.express_operate_profit),moneyflow.buy_elg_amount)',
                                    'div(ts_delta(daily_hq.close_hfq,10),daily_hq.close_hfq)',
                                    'log(abs(moneyflow.buy_elg_amount))',
                                    'div(inv(moneyflow.buy_elg_amount),moneyflow.buy_elg_amount)',
                                    'log(sqrt(moneyflow.buy_elg_amount))',
                                    'inv(abs(moneyflow.buy_elg_amount))',
                                    'inv(inv(moneyflow.buy_elg_amount))',
                                    'sqrt(inv(moneyflow.buy_elg_amount))',
                                    'sigmoid(inv(moneyflow.buy_elg_amount))',
                                    'sub(ts_min(moneyflow.buy_elg_amount,20),moneyflow.buy_elg_amount)',
                                    'cs_rank(cs_orthogonalize(moneyflow.buy_elg_amount,express.express_n_income))',
                                    'cs_rank(ts_max(moneyflow.buy_elg_amount,20))',
                                    'log(sub(moneyflow.buy_elg_amount,express.express_total_assets))',
                                    'sub(cs_zscore(daily_basic.turnover_rate_f),moneyflow.buy_elg_amount)',
                                    'ts_std(ts_cov(moneyflow.buy_elg_amount,daily_hq.close_hfq,5),10)',
                                    'ts_std(ts_delta(moneyflow.buy_elg_amount,500),10)',
                                    'cs_orthogonalize(sqrt(moneyflow.buy_elg_amount),express.express_diluted_roe)',
                                    'add(ts_zscore(moneyflow.sell_sm_amount,60),div(daily_hq.volume,moneyflow.buy_elg_amount))',
                                    'ts_backward_pct_chg(add(daily_hq.close_hfq,daily_hq.close),10)',
                                    'ts_var(mul(daily_basic.total_mv,moneyflow.buy_elg_amount),10)',
                                    'cs_zscore(ts_mean(daily_hq.pct_chg,5))',
                                    'add(div(daily_hq.volume,moneyflow.buy_elg_amount),ts_var(daily_basic.volume,10))',
                                    'abs(div(daily_hq.volume,moneyflow.buy_elg_amount))',
                                    'inv(div(daily_hq.volume,moneyflow.buy_elg_amount))',
                                    'add(div(daily_hq.volume,moneyflow.buy_elg_amount),daily_basic.turnover_rate_f)',
                                    'div(mul(factor_adj.adj_factor,moneyflow.sell_sm_vol),moneyflow.buy_elg_amount)',
                                    'mul(ts_var(daily_basic.turnover_rate_f,5),ts_mean(moneyflow.buy_elg_amount,5))',
                                    'div(cs_rank(moneyflow.buy_md_amount),moneyflow.buy_elg_amount)',
                                    'mul(div(daily_basic.total_mv,moneyflow.sell_sm_vol),add(moneyflow.net_mf_amount,daily_hq.amount))',
                                    'sub(ts_delta(top_list.reason_is_contain_zhangfu,10),moneyflow.buy_elg_amount)',
                                    'inv(add(top_list.reason_is_contain_diefu,moneyflow.buy_elg_amount))',
                                    'cs_rank(div(moneyflow.buy_lg_vol,moneyflow.buy_elg_amount))',
                                    'cs_rank(ts_zscore(daily_hq.high_hfq,20))',
                                    'sqrt(ts_max(moneyflow.buy_elg_amount,20))',
                                    'sigmoid(div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol))',
                                    'sqrt(div(moneyflow.buy_elg_vol,moneyflow.buy_sm_vol))',
                                    'ts_max(ts_delta(daily_hq.close_hfq,5),5)',
                                    'ts_var(ts_delta(moneyflow.buy_elg_amount,10),10)',
                                    'ts_min(sub(daily_basic.turnover_rate,moneyflow.buy_elg_amount),20)',
                                    'ts_std(add(moneyflow.sell_lg_amount,daily_basic.turnover_rate_f),5)',
                                    'sqrt(div(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount))',
                                    'sigmoid(div(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount))',
                                    'div(ts_median(moneyflow.buy_sm_vol,500),moneyflow.buy_elg_amount)',
                                    'cs_zscore(ts_std(moneyflow.buy_lg_amount,5))',
                                    'sub(sigmoid(moneyflow.buy_sm_vol),sub(express.express_revenue,moneyflow.buy_elg_amount))',
                                    'ts_var(add(moneyflow.sell_lg_amount,daily_basic.pe_ttm),5)',
                                    'abs(div(moneyflow.buy_elg_vol,moneyflow.sell_sm_vol))',
                                    'ts_max(cs_orthogonalize(moneyflow.buy_elg_amount,express.express_n_income),20)',
                                    'sigmoid(ts_zscore(daily_hq.close_hfq,120))',
                                    'cs_orthogonalize(ts_var(moneyflow.sell_sm_vol,500),moneyflow.buy_elg_vol)',
                                    'cs_rank(ts_var(moneyflow.buy_elg_amount,20))',
                                    'add(mul(daily_hq.close,moneyflow.buy_elg_amount),express.express_yoy_net_profit)',
                                    'sigmoid(ts_backward_pct_chg(daily_hq.close,10))',
                                    'sqrt(ts_std(daily_hq.amount,5))',
                                    'inv(ts_std(daily_hq.amount,5))',
                                    'cs_zscore(abs(moneyflow.buy_elg_amount))',
                                    'cs_zscore(cs_zscore(moneyflow.buy_elg_amount))',
                                    'sigmoid(cs_zscore(moneyflow.buy_elg_amount))',
                                    'cs_zscore(add(express.express_diluted_eps,moneyflow.buy_elg_amount))',
                                    'cs_zscore(add(moneyflow.buy_elg_amount,express.express_diluted_eps))',
                                    'add(ts_var(daily_hq.amount,5),mul(moneyflow.buy_elg_vol,moneyflow.sell_sm_amount))',
                                    'cs_zscore(sub(moneyflow.buy_elg_amount,daily_basic.turnover_rate))',
                                    'cs_zscore(sub(daily_basic.turnover_rate,moneyflow.buy_elg_amount))',
                                    'sqrt(add(moneyflow.buy_elg_amount,daily_hq.close))',
                                    'log(add(moneyflow.buy_elg_amount,daily_hq.close))',
                                    'ts_mean(ts_sum(moneyflow.buy_elg_amount,5),5)',
                                    'cs_rank(div(moneyflow.buy_lg_amount,moneyflow.buy_sm_amount))',
                                    'log(ts_var(moneyflow.buy_elg_amount,20))',
                                    'ts_var(cs_orthogonalize(daily_hq.amount,express.express_total_assets),5)',
                                    'add(mul(daily_hq.close,moneyflow.buy_elg_amount),ts_count(daily_basic.pb,10))',
                                    'add(ts_std(moneyflow.buy_elg_amount,5),ts_var(daily_hq.high_hfq,500))',
                                    'ts_std(ts_cov(daily_hq.amount,moneyflow.buy_elg_vol,5),5)',
                                    'ts_std(sub(moneyflow.sell_lg_amount,top_list.reason_is_contain_diefu),5)',
                                    'ts_var(cs_orthogonalize(moneyflow.buy_elg_amount,daily_basic.free_share),5)',
                                    'cs_orthogonalize(ts_std(daily_hq.amount,5),express.express_operate_profit)',
                                    'ts_max(ts_delta(moneyflow.buy_lg_amount,10),10)',
                                    'ts_delta(cs_rank(daily_basic.total_mv),20)',
                                    'abs(ts_var(moneyflow.buy_elg_amount,20))',
                                    'ts_max(mul(daily_basic.volume,daily_hq.amount),5)',
                                    'ts_std(mul(daily_basic.total_mv,moneyflow.buy_elg_amount),5)',
                                    'sqrt(ts_std(moneyflow.buy_elg_amount,20))',
                                    'ts_std(abs(moneyflow.buy_elg_amount),20)',
                                    'add(sigmoid(moneyflow.buy_elg_vol),ts_zscore(daily_hq.close,60))',
                                    'cs_orthogonalize(ts_zscore(daily_basic.circ_mv,120),ts_median(daily_basic.volume,250))',
                                    'ts_backward_pct_chg(sub(daily_hq.close_hfq,express.express_total_assets),10)',
                                    'cs_rank(ts_backward_pct_chg(daily_basic.total_mv,5))',
                                    'add(ts_delta(daily_hq.pct_chg,60),ts_var(moneyflow.buy_elg_amount,20))',
                                    'ts_std(cs_orthogonalize(moneyflow.buy_elg_amount,express.express_n_income),20)',
                                    'ts_max(mul(daily_hq.pct_chg,daily_basic.turnover_rate_f),10)',
                                    'ts_zscore(cs_zscore(daily_basic.circ_mv),20)',
                                    'sub(ts_count(daily_hq.close_hfq,10),ts_delta(daily_hq.close,10))',
                                    'ts_max(div(moneyflow.buy_lg_amount,moneyflow.buy_md_amount),5)',
                                    'ts_delta(abs(daily_hq.close),10)',
                                    'ts_max(ts_mean(moneyflow.buy_elg_amount,5),10)',
                                    'sub(mul(moneyflow.buy_sm_amount,express.express_diluted_roe),add(moneyflow.buy_elg_amount,daily_hq.close))',
                                    'ts_mean(sub(daily_hq.pct_chg,express.express_total_assets),10)',
                                    'cs_zscore(ts_backward_pct_chg(daily_basic.circ_mv,5))',
                                    'cs_zscore(ts_backward_pct_chg(daily_basic.total_mv,5))',
                                    'div(sqrt(daily_basic.turnover_rate_f),mul(moneyflow.buy_elg_amount,daily_basic.turnover_rate_f))',
                                    'ts_var(add(express.express_yoy_net_profit,moneyflow.sell_lg_amount),5)',
                                    'ts_mean(div(moneyflow.buy_elg_vol,moneyflow.sell_sm_vol),10)',
                                    'add(mul(moneyflow.buy_elg_amount,daily_basic.turnover_rate_f),moneyflow.sell_elg_amount)',
                                    'div(inv(moneyflow.sell_md_amount),moneyflow.buy_elg_amount)',
                                    'add(add(express.express_total_hldr_eqy_exc_min_int,moneyflow.buy_lg_amount),ts_mean(moneyflow.buy_elg_amount,10))',
                                    'ts_std(add(moneyflow.buy_md_amount,moneyflow.buy_lg_amount),5)',
                                    'ts_std(sqrt(moneyflow.sell_md_amount),5)',
                                    'abs(div(moneyflow.buy_sm_amount,moneyflow.buy_lg_amount))',
                                    'sqrt(div(moneyflow.buy_lg_amount,moneyflow.buy_sm_amount))',
                                    'sqrt(div(moneyflow.buy_sm_amount,moneyflow.buy_lg_amount))',
                                    'inv(div(moneyflow.buy_sm_amount,moneyflow.buy_lg_amount))',
                                    'sigmoid(div(moneyflow.buy_sm_amount,moneyflow.buy_lg_amount))',
                                    'add(ts_zscore(daily_basic.pb,500),moneyflow.buy_elg_amount)',
                                    'ts_backward_pct_chg(add(daily_basic.dv_ttm,daily_basic.circ_mv),10)',
                                    'sigmoid(ts_backward_pct_chg(daily_basic.total_mv,10))',
                                    'add(cs_orthogonalize(moneyflow.buy_elg_amount,express.express_total_hldr_eqy_exc_min_int),ts_backward_pct_chg(daily_basic.ps_ttm,10))',
                                    'ts_backward_pct_chg(sub(moneyflow.sell_elg_amount,daily_basic.circ_mv),10)',
                                    'ts_backward_pct_chg(sub(daily_basic.circ_mv,moneyflow.buy_md_amount),10)',
                                    'ts_std(add(moneyflow.buy_elg_amount,moneyflow.buy_sm_amount),5)',
                                    'ts_var(ts_std(moneyflow.sell_elg_amount,5),5)',
                                    'cs_rank(mul(daily_hq.close,moneyflow.buy_elg_amount))',
                                    'sub(ts_zscore(daily_hq.close,20),top_list.reason_is_contain_diefu)',
                                    'div(mul(daily_hq.amount,moneyflow.sell_lg_amount),moneyflow.sell_sm_vol)',
                                    'cs_zscore(ts_max(moneyflow.buy_elg_amount,20))',
                                    'ts_var(ts_var(moneyflow.sell_elg_amount,5),5)',
                                    'cs_rank(mul(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount))',
                                    'sqrt(ts_cov(daily_hq.amount,moneyflow.buy_elg_vol,5))',
                                    'log(ts_cov(daily_hq.amount,moneyflow.buy_elg_vol,5))',
                                    'ts_zscore(mul(daily_hq.close_hfq,daily_basic.total_share),60)',
                                    'sub(sub(daily_basic.volume,daily_hq.high_hfq),add(daily_hq.low_hfq,moneyflow.buy_elg_amount))',
                                    'ts_std(div(moneyflow.sell_md_amount,moneyflow.buy_sm_amount),5)',
                                    'cs_rank(add(moneyflow.buy_elg_amount,daily_hq.high_hfq))',
                                    'ts_zscore(sub(daily_hq.volume,daily_basic.total_mv),20)',
                                    'inv(mul(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount))',
                                    'log(mul(moneyflow.buy_elg_amount,moneyflow.sell_sm_amount))',
                                    'add(ts_cov(moneyflow.buy_elg_amount,top_list.reason_is_contain_diefu,250),moneyflow.buy_elg_amount)',
                                    'ts_std(add(daily_hq.pct_chg,moneyflow.buy_lg_amount),10)',
                                    'ts_var(add(daily_hq.pct_chg,moneyflow.buy_lg_amount),10)',
                                    'cs_rank(add(moneyflow.buy_elg_amount,daily_hq.open_hfq))',
                                    'sigmoid(ts_zscore(daily_basic.total_mv,20))',
                                    'sigmoid(ts_zscore(daily_basic.circ_mv,20))',
                                    'cs_orthogonalize(add(moneyflow.buy_elg_amount,daily_hq.high_hfq),mul(moneyflow.sell_elg_vol,daily_basic.ps_ttm))',
                                    'ts_var(sub(moneyflow.buy_lg_amount,daily_basic.turnover_rate),10)',
                                    'cs_orthogonalize(mul(moneyflow.buy_elg_amount,daily_basic.turnover_rate_f),express.express_operate_profit)',
                                    'log(ts_var(moneyflow.sell_elg_amount,5))',
                                    'sqrt(ts_var(moneyflow.sell_elg_amount,5))',
                                    'mul(inv(daily_basic.volume),abs(moneyflow.buy_elg_amount))',
                                    'inv(div(moneyflow.buy_elg_amount,daily_basic.volume))',
                                    'ts_mean(add(daily_hq.low_hfq,moneyflow.buy_elg_amount),5)',
                                    'ts_mean(cs_orthogonalize(daily_hq.pct_chg,moneyflow.buy_elg_vol),10)',
                                    'ts_sum(sqrt(moneyflow.buy_elg_amount),5)',
                                    'ts_zscore(log(daily_basic.total_mv),20)',
                                    'cs_rank(div(moneyflow.buy_elg_amount,daily_basic.volume))',
                                    'div(add(express.express_revenue,moneyflow.buy_elg_vol),moneyflow.sell_md_vol)',
                                    'inv(div(moneyflow.buy_elg_vol,moneyflow.sell_md_vol))',
                                    'cs_rank(ts_backward_pct_chg(daily_basic.ps,5))']

        fes = {}
        for expression in need_feature_expressions:
            var = qu.process_expression(expression, "self.basic_feature", "self.basic_operators")
            print(expression, "-->", var)
            vardf = eval(var)
            fes[expression] = vardf[self.keep_start:].copy()
            del vardf

        return fes

    def get_feature(self, date, code, group='all'):
        res = {}

        if group == 'all':
            for gname in self.feature_group:
                features = self.feature_group[gname]
                for key in features.keys():
                    res[key] = features[key].loc[
                        date, code]  # 1.7 ms ± 66.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
        else:
            features = self.feature_group[group]
            for key in features.keys():
                res[key] = features[key].loc[
                    date, code]  # 1.7 ms ± 66.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

        # fill nan
        for key, value in res.items():
            if math.isnan(value):
                res[key] = 0.0

        res_sorted = collections.OrderedDict(sorted(res.items()))
        return res_sorted
