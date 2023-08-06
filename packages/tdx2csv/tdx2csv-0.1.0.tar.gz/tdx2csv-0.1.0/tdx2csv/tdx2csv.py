import pandas as pd


def txt2csv(infile, output=None):
    """
    通达信导出文件转换为 Pandas 可用的 csv 文件
    :param infile: 通达信导出的 txt 文件路径
    :param output: 转换后的目标 csv 文件路径
    """
    names = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']
    df = pd.read_csv(infile, names=names, header=2, skipfooter=1, index_col='date')
    bool(output) and df.to_csv(output)

    return df
