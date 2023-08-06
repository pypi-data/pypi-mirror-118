import pandas as pd
import numpy as np
from quant_util import fill_dict_nan, sort_dict_by_key


def log_return(series):
    var = np.log(series)
    var = np.diff(var)
    return np.concatenate(([np.nan], var))


def realized_volatility(series):
    return np.sqrt(np.nansum(series ** 2))


def count_unique(series):
    return len(np.unique(series))


class FeatureHf:
    def __init__(self):
        pass

    def calc_hf_feature_jingjia(self, df):
        time_np = df['server_datetime'].to_numpy()
        price_np = df['close'].to_numpy()
        last_close = df['pre_close'][-1]
        last_time = time_np[-1]
        last_time = pd.to_datetime(last_time)
        sec = last_time.hour * 3600 + last_time.minute * 60 + last_time.second - 34200
        if sec >= 12600:
            sec = sec - 5400
        elif sec < 0:
            sec = 0
        first_meet_up_limit_time_seconds_close_0 = sec / 14400
        first_meet_up_limit_time_seconds_close_7200 = abs((sec - 7200) / 14400)
        first_meet_up_limit_time_seconds_close_14400 = abs((sec - 14400) / 14400)

        # 竞价信息
        date = last_time.date()
        kaipanshijian = pd.to_datetime(date.strftime('%Y-%m-%d') + " 09:30:00.000")
        mask = np.where(time_np < kaipanshijian)[0]
        if len(mask) == 0:
            kaipanjia = df['close'][0]
        else:
            kaipanjia = price_np[mask[-1]]
        kaipanyijia = kaipanjia / last_close

        fe = {
            "first_meet_up_limit_time_seconds_close_0": first_meet_up_limit_time_seconds_close_0,
            "first_meet_up_limit_time_seconds_close_7200": first_meet_up_limit_time_seconds_close_7200,
            "first_meet_up_limit_time_seconds_close_14400": first_meet_up_limit_time_seconds_close_14400,
            "kaipanyijia": kaipanyijia
        }
        return fe

    def calc_hf_feature_dadan(self, df):
        fe = {}

        price_np = df['close'].to_numpy()
        price_diff = np.diff(price_np, n=1)
        mask_zhang = np.where(price_diff > 0)[0] + 1
        mask_die = np.where(price_diff < 0)[0] + 1
        cur_vol_np = df['cur_vol'].to_numpy()
        cur_amount_np = price_np * cur_vol_np * 100

        fe['zhang_vol_sum'] = cur_vol_np[mask_zhang].sum() * 100  # need
        fe['die_vol_sum'] = cur_vol_np[mask_die].sum() * 100  # need

        time_np = df['server_datetime'].to_numpy()
        last_time = time_np[-1]
        last_time = pd.to_datetime(last_time)

        for timedelta in [150, 300, 450, 600]:
            timedelta_mask = np.where(time_np > (last_time - pd.Timedelta(seconds=timedelta)))[0]
            fe[f'min_price_before_{timedelta}s_div_realtime_price'] = price_np[timedelta_mask].min() / price_np[-1]
            fe[f'start_price_before_{timedelta}s_div_realtime_price'] = price_np[timedelta_mask[0]] / price_np[-1]

            mask_zhang_timedelta = np.intersect1d(mask_zhang, timedelta_mask)
            mask_die_timedelta = np.intersect1d(mask_die, timedelta_mask)
            fe[f'zhang_vol_sum_before_{timedelta}s'] = cur_vol_np[mask_zhang_timedelta].sum() * 100
            fe[f'die_vol_sum_before_{timedelta}s'] = cur_vol_np[mask_die_timedelta].sum() * 100
            fe[f'zhang_vol_std_before_{timedelta}s'] = cur_vol_np[mask_zhang_timedelta].std() * 100
            fe[f'die_vol_std_before_{timedelta}s'] = cur_vol_np[mask_die_timedelta].std() * 100
            fe[f'zhang_vol_mean_before_{timedelta}s'] = cur_vol_np[mask_zhang_timedelta].mean() * 100
            fe[f'die_vol_mean_before_{timedelta}s'] = cur_vol_np[mask_die_timedelta].mean() * 100

            for dadan in [10e4, 30e4, 50e4, 100e4]:
                mask_dadan = np.where(cur_amount_np > dadan)[0]
                var1 = np.intersect1d(mask_zhang_timedelta, mask_dadan)
                var2 = np.intersect1d(mask_die_timedelta, mask_dadan)
                fe[f'zhang_dadan_sum_{dadan}_before_{timedelta}s'] = cur_amount_np[var1].sum()
                fe[f'die_dadan_sum_{dadan}_before_{timedelta}s'] = cur_amount_np[var2].sum()
                fe[f'zhang_dadan_std_{dadan}_before_{timedelta}s'] = cur_amount_np[var1].std()
                fe[f'die_dadan_std_{dadan}_before_{timedelta}s'] = cur_amount_np[var2].std()
                fe[f'zhang_dadan_mean_{dadan}_before_{timedelta}s'] = cur_amount_np[var1].mean()
                fe[f'die_dadan_mean_{dadan}_before_{timedelta}s'] = cur_amount_np[var2].mean()

            for dadan_vol in [100, 500, 1000, 3000, 5000]:
                mask_dadan = np.where(cur_vol_np > dadan_vol)[0]
                var1 = np.intersect1d(mask_zhang_timedelta, mask_dadan)
                var2 = np.intersect1d(mask_die_timedelta, mask_dadan)
                fe[f'zhang_dadan_vol_sum_{dadan_vol}_before_{timedelta}s'] = cur_vol_np[var1].sum()
                fe[f'die_dadan_vol_sum_{dadan_vol}_before_{timedelta}s'] = cur_vol_np[var2].sum()
                fe[f'zhang_dadan_vol_std_{dadan_vol}_before_{timedelta}s'] = cur_vol_np[var1].std()
                fe[f'die_dadan_vol_std_{dadan_vol}_before_{timedelta}s'] = cur_vol_np[var2].std()
                fe[f'zhang_dadan_vol_mean_{dadan_vol}_before_{timedelta}s'] = cur_vol_np[var1].mean()
                fe[f'die_dadan_vol_mean_{dadan_vol}_before_{timedelta}s'] = cur_vol_np[var2].mean()
        return fe

    def calc_hf_feature_wap(self, df):
        fe = {}
        # get pre_close
        code = df.index.get_level_values(1)[0]
        d_time = pd.to_datetime(df['server_datetime'][-1])
        fe['code'] = code
        fe['date'] = d_time.date()

        time_np = pd.to_datetime(df['server_datetime']).to_numpy()
        price = df['close'].to_numpy()
        price_mean = price.mean()
        volume = df['cur_vol'].to_numpy() * 100
        price_mul_volume = price * volume

        price_mul_volume_cumsum = price_mul_volume.cumsum()
        volume_cumsum = volume.cumsum()
        wap = price_mul_volume_cumsum / volume_cumsum
        delta_price_wap = price - wap
        delta_price_wap_div_price_mean = delta_price_wap / price_mean
        price_div_wap = price / wap
        price_log_return = log_return(price)

        # Dict for aggregations
        create_feature_dict = {
            'delta_price_wap': ["np.nansum", "np.nanmean", "np.nanstd"],
            'delta_price_wap_div_price_mean': ["np.nansum", "np.nanmean", "np.nanstd"],
            'price_div_wap': ["np.nansum", "np.nanmean", "np.nanstd"],
            'price_log_return': ["realized_volatility"],
            'time_np': ["count_unique"],
            'volume': ["np.nansum", "realized_volatility", "np.nanmean", "np.nanstd", "np.max", "np.min"],
            'price_mul_volume': ["np.nansum", "realized_volatility", "np.nanmean", "np.nanstd", "np.max", "np.min"],

        }

        feature_name_var_map = {
            'delta_price_wap': delta_price_wap,
            'delta_price_wap_div_price_mean': delta_price_wap_div_price_mean,
            'price_div_wap': delta_price_wap_div_price_mean,
            "price_log_return": price_log_return,
            "time_np": time_np,
            "volume": volume,
            "price_mul_volume": price_mul_volume,
        }

        npfun_name_fun_map = {
            'np.nansum': np.nansum,
            'np.nanmean': np.nanmean,
            'np.nanstd': np.nanstd,
            "realized_volatility": realized_volatility,
            "count_unique": count_unique,
            "np.max": np.max,
            "np.min": np.min,

        }

        for timedelta in [150, 300, 450, 600]:
            start_datetime = d_time - pd.Timedelta(seconds=timedelta)
            time_mask = np.where(time_np > start_datetime)[0]

            # 特殊的 corr
            fe[f'correlation_price_vol_{timedelta}'] = np.corrcoef(price[time_mask], volume[time_mask])[0][1]
            for feature in create_feature_dict:
                for fun_name in create_feature_dict[feature]:
                    fe[f'{feature}_{fun_name}_{timedelta}'] = npfun_name_fun_map[fun_name](
                        feature_name_var_map[feature][time_mask])
        return fe

    def calc_hf_feature_askbid12(self, df):
        fe = {}
        # get pre_close
        code = df.index.get_level_values(1)[0]
        d_time = pd.to_datetime(df['server_datetime'][-1])
        fe['code'] = code
        fe['date'] = d_time.date()

        time_np = pd.to_datetime(df['server_datetime']).to_numpy()
        bid_price1 = df['bid_price_1'].to_numpy()
        bid_price2 = df['bid_price_2'].to_numpy()
        ask_price1 = df['ask_price_1'].to_numpy()
        ask_price2 = df['ask_price_2'].to_numpy()
        bid_size1 = df['bid_vol_1'].to_numpy()
        bid_size2 = df['bid_vol_2'].to_numpy()
        ask_size1 = df['ask_vol_1'].to_numpy()
        ask_size2 = df['ask_vol_2'].to_numpy()
        # Calculate Wap
        wap1 = (bid_price1 * ask_size1 + ask_price1 * bid_size1) / (bid_size1 + ask_size1)
        wap2 = (bid_price2 * ask_size2 + ask_price2 * bid_size2) / (bid_size2 + ask_size2)
        log_return1 = log_return(wap1)
        log_return2 = log_return(wap2)
        wap_balance = wap1 - wap2
        price_spread = (ask_price1 - bid_price1) / ((ask_price1 + bid_price1) / 2)
        bid_spread = bid_price1 - bid_price2
        ask_spread = ask_price1 - ask_price2
        total_volume = (ask_size1 + ask_size2) + (bid_size1 + bid_size2)
        volume_imbalance = abs((ask_size1 + ask_size2) - (bid_size1 + bid_size2))

        # Dict for aggregations
        #     create_feature_dict = {
        #         'wap1': [np.sum, np.mean, np.std],
        #         'wap2': [np.sum, np.mean, np.std],
        #         'log_return1': [np.sum, realized_volatility, np.mean, np.std],
        #         'log_return2': [np.sum, realized_volatility, np.mean, np.std],
        #         'wap_balance': [np.sum, np.mean, np.std],
        #         'price_spread':[np.sum, np.mean, np.std],
        #         'bid_spread':[np.sum, np.mean, np.std],
        #         'ask_spread':[np.sum, np.mean, np.std],
        #         'total_volume':[np.sum, np.mean, np.std],
        #         'volume_imbalance':[np.sum, np.mean, np.std]
        #     }

        for timedelta in [150, 300, 450, 600]:
            start_datetime = d_time - pd.Timedelta(seconds=timedelta)
            time_mask = np.where(time_np > start_datetime)[0]

            for fe_basic_name, var in [
                ('wap1', wap1),
                ('wap2', wap2),
                ("log_return1", log_return1),
                ("log_return2", log_return2),
                ('wap_balance', wap_balance),
                ('price_spread', price_spread),
                ('bid_spread', bid_spread),
                ('ask_spread', ask_spread),
                ('total_volume', total_volume),
                ('volume_imbalance', volume_imbalance),
            ]:
                fe[f'{fe_basic_name}_sum_{timedelta}'] = np.nansum(var[time_mask])
                fe[f'{fe_basic_name}_mean_{timedelta}'] = np.nanmean(var[time_mask])
                fe[f'{fe_basic_name}_std_{timedelta}'] = np.nanstd(var[time_mask])

            fe[f'log_return1_realized_volatility_{timedelta}'] = realized_volatility(log_return1[time_mask])
            fe[f'log_return2_realized_volatility_{timedelta}'] = realized_volatility(log_return2[time_mask])

        start_datetime = d_time - pd.Timedelta(seconds=600)
        time_mask = np.where(time_np > start_datetime)[0]
        fe[f'tick_count_{timedelta}'] = len(time_mask)
        return fe

    def calc_hf_feature_soir(self, df):
        fe = {}
        # get pre_close
        code = df.index.get_level_values(1)[0]
        d_time = pd.to_datetime(df['server_datetime'][-1])
        fe['code'] = code
        fe['date'] = d_time.date()

        time_np = pd.to_datetime(df['server_datetime']).to_numpy()
        bid_price_1 = df['bid_price_1'].to_numpy()
        ask_price_1 = df['ask_price_1'].to_numpy()
        bid_vol_1 = df['bid_vol_1'].to_numpy()
        ask_vol_1 = df['ask_vol_1'].to_numpy()
        ask_vol_2 = df['ask_vol_2'].to_numpy()
        bid_price_2 = df['bid_price_2'].to_numpy()
        bid_vol_2 = df['bid_vol_2'].to_numpy()
        ask_price_2 = df['ask_price_2'].to_numpy()
        bid_price_3 = df['bid_price_3'].to_numpy()
        ask_price_3 = df['ask_price_3'].to_numpy()
        bid_vol_3 = df['bid_vol_3'].to_numpy()
        ask_vol_3 = df['ask_vol_3'].to_numpy()
        bid_price_4 = df['bid_price_4'].to_numpy()
        ask_price_4 = df['ask_price_4'].to_numpy()
        bid_vol_4 = df['bid_vol_4'].to_numpy()
        ask_vol_4 = df['ask_vol_4'].to_numpy()
        bid_price_5 = df['bid_price_5'].to_numpy()
        ask_price_5 = df['ask_price_5'].to_numpy()
        bid_vol_5 = df['bid_vol_5'].to_numpy()
        ask_vol_5 = df['ask_vol_5'].to_numpy()

        # Calculate Wap
        soir1 = (bid_vol_1 - ask_vol_1) / (bid_vol_1 - ask_vol_1)
        soir2 = (bid_vol_2 - ask_vol_2) / (bid_vol_2 - ask_vol_2)
        soir3 = (bid_vol_3 - ask_vol_3) / (bid_vol_3 - ask_vol_3)
        soir4 = (bid_vol_4 - ask_vol_4) / (bid_vol_4 - ask_vol_4)
        soir5 = (bid_vol_5 - ask_vol_5) / (bid_vol_5 - ask_vol_5)
        soir_sum = soir1 * 5 + soir2 * 4 + soir3 * 3 + soir4 * 2 + soir5 * 1

        # mpc
        avg_pri = (bid_price_1 + ask_price_1) / 2
        pri_diff = np.diff(avg_pri)
        pri_diff = np.concatenate(([np.nan], pri_diff))
        mpc1 = pri_diff / avg_pri

        # Dict for aggregations
        create_feature_dict = {
            'soir1': ["np.nansum", "np.nanmean", "np.nanstd"],
            'soir2': ["np.nansum", "np.nanmean", "np.nanstd"],
            'soir3': ["np.nansum", "np.nanmean", "np.nanstd"],
            'soir4': ["np.nansum", "np.nanmean", "np.nanstd"],
            'soir5': ["np.nansum", "np.nanmean", "np.nanstd"],
            'soir_sum': ["np.nansum", "np.nanmean", "np.nanstd"],
            'mpc1': ["np.nansum", "np.nanmean", "np.nanstd"],
        }

        feature_name_var_map = {
            'soir1': soir1,
            'soir2': soir2,
            'soir3': soir3,
            'soir4': soir4,
            'soir5': soir5,
            'soir_sum': soir_sum,
            'mpc1': mpc1,
        }

        npfun_name_fun_map = {
            'np.nansum': np.nansum,
            'np.nanmean': np.nanmean,
            'np.nanstd': np.nanstd,
        }

        for timedelta in [150, 300, 450, 600]:
            start_datetime = d_time - pd.Timedelta(seconds=timedelta)
            time_mask = np.where(time_np > start_datetime)[0]
            for feature in create_feature_dict:
                for fun_name in create_feature_dict[feature]:
                    fe[f'{feature}_{fun_name}_{timedelta}'] = npfun_name_fun_map[fun_name](
                        feature_name_var_map[feature][time_mask])
        return fe

    def get_feature(self, df_filter):
        fe1 = self.calc_hf_feature_soir(df_filter)
        fe2 = self.calc_hf_feature_wap(df_filter)
        fe3 = self.calc_hf_feature_askbid12(df_filter)
        fe4 = self.calc_hf_feature_dadan(df_filter)
        fe5 = self.calc_hf_feature_jingjia(df_filter)
        fe = {**fe1, **fe2, **fe3, **fe4, **fe5}
        fe = fill_dict_nan(fe)
        return sort_dict_by_key(fe)
