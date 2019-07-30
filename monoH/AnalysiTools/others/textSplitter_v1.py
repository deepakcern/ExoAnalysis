from itertools import izip_longest
from glob import glob
import os

cwd = os.getcwd()

n=3000

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


dirName='splitted_bkg_files'

with open('Files/bkg_2016.txt') as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
        with open('Files'+'/'+'bkg_2016_{0}.txt'.format(i), 'w') as fout:
            fout.writelines(g)


