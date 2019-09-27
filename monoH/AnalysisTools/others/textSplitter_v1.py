from itertools import izip_longest
from glob import glob
import os

cwd = os.getcwd()

n=5

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


dirName='splitted_files'
os.system('rm -rf '+dirName)
os.system('mkdir '+dirName)

def runFile(txtfile,dirName):
    with open(txtfile) as f:
        newtxt=txtfile.split('/')[-1].replace('.txt','')
        for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
            with open(dirName+'/'+newtxt+'_{0}.txt'.format(i), 'w') as fout:
                fout.writelines(g)



path='/afs/cern.ch/work/d/dekumar/public/monoH/2017_Skimmer/V0/ExoPieSlimmer/Files'
files=glob(path+'/*txt')

for infile in files:
    runFile(infile,dirName)
