#!/usr/bin/env python
import ROOT as ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend,TH2D
import os, datetime, glob
import random
import sys, optparse
import array
import math
import getpass
import socket
import json
from array import array

path='/home/deepak/MEGA/Fullwork/2017_monoHbb/kFactorFiles'

dirName = 'WeightFiles'
os.system('rm -rf '+dirName)
os.system('mkdir  '+dirName)

rootFiles = [file for file in glob.glob(path+'/*.root') if 'merged_kfactors' in file]

def runFile(infile,histName):
    f = TFile.Open(infile,'READ')
    Hist = f.Get(histName)
    Nbins = Hist.GetXaxis().GetNbins()
    OutFileName = infile.split('/')[-1].replace('.root','.txt')
    fout = open(dirName+'/'+OutFileName,'w')
    fout.write('lowPt'+'      '+'highpT'+'       '+'weight'+'     '+'weight_up'+'          '+'weight_down'+'         '+'stats_error'+'\n' )
    for i in range(1,Nbins+1):
        lowPt  = Hist.GetXaxis().GetBinLowEdge(i)
        highPt = Hist.GetXaxis().GetBinUpEdge(i)
        weight = Hist.GetBinContent(i)
        weight_err  = Hist.GetBinError(i)
        weight_up   = weight + weight*0.5  # 50% uncertainty
        weight_down = weight - weight*0.5

        fout.write(str(lowPt)+'    ' + str(highPt)+'    '+str(weight)+'    '+str(weight_up)+'     '+str(weight_down)+'       '+str(weight_err)+'\n')

    fout.close()

for infile in rootFiles:
    runFile(infile,'kfactor_monojet_ewk')
