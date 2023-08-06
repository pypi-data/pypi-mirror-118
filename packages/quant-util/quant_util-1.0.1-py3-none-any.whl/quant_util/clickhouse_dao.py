import pandas as pd
from pandahouse import read_clickhouse

from .config_file import pandahouse_connection_dict
from .utils import fill_df_date, fill_df_code


def query_feature_single(code_list, start, end, table_name, feature, verbose=False):
    sqls = []
    if code_list is None or len(code_list) == 0:
        pass
    else:
        var = "','".join(code_list)
        code_filter_sql = f"`code` in ['{var}'] "
        sqls.append(code_filter_sql)
    if start is not None:
        sqls.append(f"`date` >= '{start}'")
    if end is not None:
        sqls.append(f"`date` <= '{end}'")

    filter_sql = ' and '.join(sqls)
    sql = f"""SELECT `date`,`code`,`{feature}` FROM quant.{table_name} where {filter_sql}"""
    if verbose:
        print(sql)

    df = read_clickhouse(sql, connection=pandahouse_connection_dict)
    res = df.set_index(['date', 'code']).unstack().sort_index()
    res = fill_df_date(res, start, end).sort_index()
    res.columns = res.columns.droplevel(0)
    res = fill_df_code(res, code_list)[code_list]
    return res


def get_a_feature(date, code, table_name, feature_name, verbose=False):
    date = pd.to_datetime(date).strftime("%Y-%m-%d")
    sql = f"""SELECT `date`,`code`,`{feature_name}` FROM quant.{table_name} where `date` == '{date}' and `code` = '{code}'"""
    if verbose:
        print(sql)

    df = read_clickhouse(sql, connection=pandahouse_connection_dict)
    if df is None or len(df) == 0:
        return None
    else:
        return df[feature_name][0]
