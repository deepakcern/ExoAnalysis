import os
import numpy as np
import pandas as pd 
from glob import glob
import sys, optparse,argparse

usage = "python"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-2017", "--path17",  dest="path17",default=".")
parser.add_argument("-2018", "--path18",  dest="path18",default=".")
parser.add_argument("-D", "--outputdir", dest="outputdir",default=".")

args = parser.parse_args()

path2017 = args.path17
path2018 = args.path18
outputdir = args.outputdir



def getFiles_2017_2018(path2017,path2018):
    files2017 = [txtfile for txtfile in glob(path2017+'/*txt') if ('Recoil' in txtfile or 'SR_MET' in txtfile) and not ('up' in txtfile or 'down' in txtfile)]
    files2018 = [txtfile for txtfile in glob(path2018+'/*txt') if ('Recoil' in txtfile or 'SR_MET' in txtfile) and not ('up' in txtfile or 'down' in txtfile)]
    return files2017,files2018


def dfTolatex(df,filename):
    df.to_csv(filename+'.tex',header=None, index=None, sep=' ', mode='w')

def getdf(infile_2017,infile_2018):
    headerlist2017 = ["process","and1","2017","and2"]
    headerlist2018 = ["process","and3","2018","and4"]
    df2017 = pd.read_csv(infile_2017,names=headerlist2017)
    df2018 = pd.read_csv(infile_2018,names=headerlist2018)
    df2018.drop("process",axis='columns', inplace=True)
    df = df2017.join(df2018)
    df["hline"]="\hline" #ADD hline FOR LATEX
    return df


def run(infile_2017,infile_2018,outputName):
    df = getdf(infile_2017,infile_2018)
    dfTolatex(df,outputName)


if __name__ == '__main__':

    files2017, files2018 = getFiles_2017_2018(path2017,path2018)
    if len(files2017)!=len(files2018):
        print ('files are not equal for 2017 and 2018')
        sys.exit()

    for infile1, infile2 in zip(files2017, files2018):
        if str(infile1.split('/')[-1])!=str(infile2.split('/')[-1]):
            continue
        else:
            outputfile=outputdir+'/'+'2017_2018_'+infile1.split('/')[-1].replace('.txt','.tex').replace('log','')
            run(infile1, infile2,outputfile)
            print ('written output to file:  ',outputfile)

