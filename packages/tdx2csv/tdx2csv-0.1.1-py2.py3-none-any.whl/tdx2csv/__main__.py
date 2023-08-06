"""Console script for tdx2csv."""
import sys
from glob import glob1
from pathlib import Path

import click
from tqdm import tqdm

from .tdx2csv import txt2csv


@click.command(help=u'通达信数据转换程序.')
@click.option('-i', '--infile', required=True, type=click.Path(), help='历史数据下载目录, 默认当前目录下 input')
@click.option('-o', '--output', type=click.Path(), help='转换后输出目录, 默认当前目录下 output')
def main(infile, output):
    [txt2csv(Path(infile, txt), Path(output, txt.replace('.txt', '.csv'))) for txt in tqdm(glob1(infile, '*.txt'))]
    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
