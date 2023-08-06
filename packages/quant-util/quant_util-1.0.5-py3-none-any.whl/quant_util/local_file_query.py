import pandas as pd
import os
from quant_util import get_eng_mkt_by_code_num


def query_wudang(date_="2021-03-25", code="000001"):
    root_dir = r'E:\wudang_data'
    date = pd.to_datetime(date_)
    var1 = date.strftime("%Y%m%d")
    var2 = date.strftime("%Y-%m-%d")

    if date.year == 2019:
        year = date.year
        month = date.month
        # day = date.day
        mkt = get_eng_mkt_by_code_num(code, is_case=False)
        file_path = os.path.join(root_dir, str(year), str(month), f"fenbi-data-push.{var1}",
                                 f"{var2} {mkt}{code} fenbi.csv")
        df = pd.read_csv(file_path, skiprows=1, encoding='gbk')
    elif date.year == 2020:
        year = date.year
        month = date.month
        # day = date.day
        mkt = get_eng_mkt_by_code_num(code, is_case=False)
        file_path = os.path.join(root_dir, str(year), str(month).zfill(2), f"fenbi-data-push.{var1}",
                                 f"{var2} {mkt}{code} fenbi.csv")
        df = pd.read_csv(file_path, skiprows=1, encoding='gbk')
    elif date.year == 2021:
        year = date.year
        month = date.month
        # day = date.day
        mkt = get_eng_mkt_by_code_num(code, is_case=False)
        file_path = os.path.join(root_dir, str(year), str(month).zfill(2), f"fenbi-data-push.{var1}",
                                 f"{var2} {mkt}{code} fenbi.csv")
        df = pd.read_csv(file_path, skiprows=1, encoding='gbk')
    else:
        raise Exception("not supported year")

    df['date'] = pd.to_datetime(date)
    df['时间'] = pd.to_datetime(df['时间'])
    df['datetime'] = df['时间']
    df['code'] = code
    df['hour'] = df['datetime'].apply(lambda x: x.hour)
    df['minute'] = df['datetime'].apply(lambda x: x.minute)
    df['second'] = df['datetime'].apply(lambda x: x.second)
    df.set_index(['datetime', 'code'], inplace=True)
    return df


if __name__ == '__main__':
    query_wudang("2020-03-05", "600094")
