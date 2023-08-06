import akshare as ak


def get_all_code_list(is_filter_st=False):
    df = ak.stock_zh_a_spot_em()

    def is_st_(x):
        if 'ST' in x.upper():
            return True
        else:
            return False

    if is_filter_st:
        df['is_st'] = df['名称'].apply(is_st_)
        df = df[df['is_st'] == False]
    code_list = list(df['代码'])
    return code_list


if __name__ == '__main__':
    print(len(get_all_code_list(is_filter_st=True)))
