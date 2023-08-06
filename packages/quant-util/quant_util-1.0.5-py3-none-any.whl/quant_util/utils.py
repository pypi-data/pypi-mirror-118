import collections
import math

from .trade_date import get_trade_date_list_by_range
import pandas as pd
import hashlib
import re
import numpy as np
from operator import attrgetter
import xlrd
import datetime


def filter_chuangyeban(code_list):
    code_list = [i for i in code_list if not i.startswith("3")]
    return code_list


def filter_kechuangban(code_list):
    code_list = [i for i in code_list if not i.startswith("688")]
    return code_list


def fill_df_date(df, start, end):
    """
    @Author        : 林泽明
    @Time          : 2021-06-09 02:53:00
    @Function      :
    传进来的df是单指标的二维表
    """

    trade_date_list = get_trade_date_list_by_range(start, end)
    trade_date_list = pd.to_datetime(trade_date_list)

    for trade_date in trade_date_list:
        if trade_date not in df.index:
            df.loc[trade_date] = np.nan
    # vardf = pd.DataFrame(index=trade_date_list)
    # res = vardf.merge(df, left_index=True, right_index=True, how='left')
    return df


def fill_df_code(df, code_list, fill_value=np.nan):
    """
    @Author        : 林泽明
    @Time          : 2021-06-09 02:53:00
    @Function      :
    传进来的df是单指标的二维表
    """
    res = df.copy()
    for code in code_list:
        if code not in res.columns:
            res[code] = fill_value
    return res[code_list].copy()


def cvt_code_to_number(code):
    res = re.findall("[0-9]{6}", code)
    if res is None or len(res) == 0:
        return code
    else:
        return res[0]


def cvt_code_to_jq_code(code):
    code = cvt_code_to_number(code)
    mkt = get_eng_mkt_by_code_num(code, is_case=False)
    if mkt == "sh":
        return code + '.XSHG'
    else:
        return code + '.XSHE'


def cvt_code_to_sina_code(code):
    code = cvt_code_to_number(code)
    code = get_eng_mkt_by_code_num(code, is_case=False) + code
    return code


def cvt_code_to_baostock_code(code):
    code = cvt_code_to_number(code)
    code = get_eng_mkt_by_code_num(code, is_case=False) + "." + code
    return code


def get_eng_mkt_by_code_num(code_num, is_case=True, allow_error=False):
    if code_num.startswith("6"):
        if is_case:
            return "SH"
        else:
            return 'sh'
    elif code_num.startswith("0") or code_num.startswith("3"):
        if is_case:
            return "SZ"
        else:
            return 'sz'
    elif allow_error:
        return "unknown"
    else:
        raise Exception('convert code num to english mkt name error >>> ' + code_num)


def cvt_date_to_stamp(date):
    if not date:
        return date

    date = pd.to_datetime(date).date()
    return pd.Timestamp(date).value / 1000000000 - 8 * 3600  # 德国转中国


def cvt_date_to_standard_date(date):
    return pd.to_datetime(date).strftime("%Y-%m-%d")


def cvt_quarter_to_date(yearq):
    """
    @Author        : 林泽明
    @Time          : 2021-05-12 17:01:35
    @Function      :
    满足格式 [xxxx]q[n]
    """
    if 'q' not in yearq or len(yearq) != 6:
        raise Exception("%s not match format [xxxx]q[n]")

    year = int(yearq.split('q')[0])
    q = int(yearq.split('q')[1])

    if q == 1:
        m = 3
        d = 31
    elif q == 2:
        m = 6
        d = 30
    elif q == 3:
        m = 9
        d = 30
    else:
        m = 12
        d = 31

    return datetime.datetime(year, m, d)


def cvt_date_to_quarter(date):
    date = pd.to_datetime(date)
    y = date.year
    m = date.month

    if m <= 3:
        return '%sq%s' % (y, 1)
    if m <= 6:
        return '%sq%s' % (y, 2)
    if m <= 9:
        return '%sq%s' % (y, 3)
    return '%sq%s' % (y, 4)


def get_trade_quarter_list():
    res = []
    for i in range(1990, 2022):
        for j in range(1, 5):
            res.append("%sq%s" % (i, j))
    return res


def get_trade_quarter_by_range(start, end):
    """
    @Author        : 林泽明
    @Time          : 2021-05-12 17:20:18
    @Function      :
    注意这个函数，如果end不是以 3.31 6.30 9.30 12.31结尾，是不会包含最后一个季度地
    """

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    quarter_list = get_trade_quarter_list()
    res = []
    for quarter in quarter_list:
        tar = cvt_quarter_to_date(quarter)
        tar = pd.to_datetime(tar)
        if tar <= end and tar >= start:
            res.append(tar)
    return res


def get_pre_quarter(quarter, n=1):
    """
    @Author        : 林泽明
    @Time          : 2021-05-15 22:30:27
    @Function      :
    如果在apply里面运行 效率好低
    """

    def _get_pre_quarter(cur_quarter):
        date = cvt_quarter_to_date(cur_quarter)
        year = date.year
        month = date.month
        day = date.day

        if month == 6:
            tardate = datetime.datetime(year, 3, 31)
        elif month == 9:
            tardate = datetime.datetime(year, 6, 30)
        elif month == 12:
            tardate = datetime.datetime(year, 9, 30)
        else:
            tardate = datetime.datetime(year - 1, 12, 31)
        return cvt_date_to_quarter(tardate)

    for i in range(n):
        quarter = _get_pre_quarter(quarter)
    return quarter


from itertools import chain, islice


def create_dict(arr1, arr2):
    if len(arr1) != len(arr2):
        return {}
    else:
        res = {}
        for index in range(len(arr1)):
            res[arr1[index]] = arr2[index]
    return res


def get_chunk(lst, n, i):
    """
    @Author        : 林泽明
    @Time          : 2021-05-13 18:44:15
    @Function      :
    传进来一个list , 分成n份， 取第i份 i从1开始
    """

    def chunks(lst, n):
        res = []
        size = int(len(lst) / n) + 1
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), size):
            res.append(lst[i:i + size])
        return res

    # 修改分成几份 选择第几份
    code_list = chunks(lst, n)
    code_list = code_list[i - 1]
    return code_list


def chunks_record(iterable, size=10000):
    """
    @Author        : 林泽明
    @Time          : 2021-05-14 10:41:12
    @Function      :
    用于插入分层
    """

    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


def xl_datetime_to_float(_datetime, datemode=0):
    attrs = ('year', 'month', 'day', 'hour', 'minute', 'second')
    d_tuple = attrgetter(*attrs)(_datetime)
    res = xlrd.xldate.xldate_from_datetime_tuple(d_tuple, datemode)
    return res


def df_col_astype_ignore_nan(df, col, cvt_fun):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 22:51
    @Function      :

    """

    def _fun(x):
        if x != np.nan:
            try:
                var1 = cvt_fun(x)
            except:
                raise Exception("convert data type error")
            return var1
        else:
            return np.nan

    df[col] = df[col].apply(lambda x: _fun(x))
    return df


def drop_na_by_col(df, col_name):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 22:51
    @Function      :
    drop一列，可以用这个函数，多列用fropna 里面的 subset
    """

    return df[df[col_name].notna()]


def rename_col_endswith_1(df):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 22:52
    @Function      :
    去掉因为列名重复自动添加的.1后缀
    """

    df.columns = [i.strip('.1').strip() for i in df.columns]
    return df


def split_df_by_col_index(df, split_index):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 22:52
    @Function      :
    根据column的index来拆分df 分成两半
    """

    return (df.iloc[:, :split_index], df.iloc[:, split_index:])


def get_today_pd():
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 22:52
    @Function      :
    获取今天的日期， 不带时间，datetime64类型
    """

    return pd.to_datetime('today').normalize()


def get_now_pd():
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 23:14
    @Function      :
    获取现在的时间，datetime64类型
    """

    return pd.to_datetime(datetime.datetime.now())


def fill_columns(df, columns, default=np.nan):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 22:55
    @Function      :
    给定一些列名，如果df里面不包含某些列名则自动填充，默认填充nan
    """
    if df is None:
        df = pd.DataFrame()
    for col in columns:
        if col not in df.columns:
            df[col] = default
    return df


def standard_column_names(df, cvt_col_map):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 23:34
    @Function      :
    用于标准化列名
    """
    df.rename(columns=cvt_col_map, inplace=True)
    return df


def cvt_column_names(df, cvt_col_map):
    """
    @Author        : 林泽明
    @Time          : 2021-03-06 23:34
    @Function      :
    和standard_column_names功能一样，为了兼容之前的名字
    """
    return standard_column_names(df, cvt_col_map)


def get_df_list_min_date(df_list, bench="pay_date"):
    """
    @Author        : 林泽明
    @Time          : 2021-03-08 9:40
    @Function      :
    传入一个df_list 里面每个df需要包含bench列，然后找到多个df中最小的日期
    """

    min_date = datetime.datetime(2050, 1, 1)
    for df in df_list:
        min_date = min(min_date, df[df[bench].notna()][bench].min())

    if min_date == datetime.datetime(2050, 1, 1):
        return None
    return min_date


def drop_col_endswith_drop(df, end="_drop"):
    columns = list(df.columns)
    for col in columns:
        if col.endswith(end) and col in df.columns:
            del df[col]
    return df


def cvt_pd_to_records(data):
    if 'datetime' in data.columns:
        data.datetime = data.datetime.apply(str)
    if 'date' in data.columns:
        data.date = data.date.apply(str)
    return data.to_dict('records')


def get_last_trade_date(count=7):
    # 获取最近n天的交易日 - 网页最新交易日中间所有交易日
    start = "1990-01-01"
    end = datetime.datetime.now()
    trade_date_list = get_trade_date_list_by_range(start, end)
    return trade_date_list[-count:]


def get_md5_value(str):
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(str.encode('utf-8'))  # 得到MD5消息摘要
    my_md5_Digest = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return my_md5_Digest


def fill_dict_nan(dict_, nan_value=0.0):
    for key, value in dict_.items():
        if math.isnan(value):
            dict_[key] = nan_value
    return dict_


def sort_dict_by_key(dict_in):
    res_sorted = collections.OrderedDict(sorted(dict_in.items()))
    return res_sorted


def process_expression(expression, feature_dict_name="feature_0_s", funcs_dict_name='func'):
    """
    表达式处理，返回可以直接eval的格式
    """
    params = re.findall('([a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)', expression)
    var = re.sub('([a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)', "###param###", expression)
    for p in params:
        var = var.replace("###param###", f"{feature_dict_name}['{p}']", 1)

    fun_names = re.findall('([a-zA-Z0-9_]*)\(', var)
    var2 = re.sub('[a-zA-Z0-9_]*\(', "###function###(", var)
    for fname in fun_names:
        var2 = var2.replace("###function###", f"{funcs_dict_name}['{fname}']", 1)

    return var2
