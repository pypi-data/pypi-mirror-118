import akshare as ak


def get_all_code_list():
    df = ak.stock_zh_a_spot_em()
    code_list = list(df['代码'])
    return code_list

if __name__ == '__main__':
    print(get_all_code_list())