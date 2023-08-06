import pandas as pd
import numpy as np
from quant_util import fill_dict_nan, sort_dict_by_key


class FeatureHf1:
    def __init__(self):
        pass

    def calc_hf_feature(self, df):
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

    def calc_hf_feature_2(self, df):
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

    def get_feature(self, df_filter):
        fe1 = self.calc_hf_feature(df_filter)
        fe2 = self.calc_hf_feature_2(df_filter)
        fe = {**fe1, **fe2}
        fe = fill_dict_nan(fe)
        return sort_dict_by_key(fe)
