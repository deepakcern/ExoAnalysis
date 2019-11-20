import sys,os,array
import json

from array import array
from glob import glob

from ROOT import TFile, gROOT, kBlack,TH1F


f= TFile.Open('/Users/dekumar/MEGA/Fullwork/2017_Plotting/19112019/monoHROOT/h_reg_WenuCR_resolved_cutFlow.root','READ')


DIBOSON=f.Get('DIBOSON')
ZJets = f.Get('ZJets')
GJets = f.Get('GJets')
QCD = f.Get('QCD')
SMH = f.Get('SMH')
STop = f.Get('STop')
Top = f.Get('Top')
WJets = f.Get('WJets')
DYJets = f.Get('DYJets')

histos=[DIBOSON,ZJets,GJets,QCD,SMH,STop,Top,WJets,DYJets]
Names=['DIBOSON','ZJets','GJets','QCD','SMH','STop','Top','WJets','DYJets']
Label=['Total','preselection','trigger','requreLep','vetoLep','nJets','MET','Recoil','nBjets','Mbb','aditionalJets','orthogonal']
BinSum=[ 0 for i in range(len(Label))]
WjetBin=[0 for i in range(len(Label))]

fout = open('BinContent.txt','w')
for hist in range(len(histos)):
    bins={}
    for bin in range(histos[hist].GetXaxis().GetNbins()):
        bins[Label[bin]]=histos[hist].GetBinContent(bin+1)
        BinSum[bin]+=histos[hist].GetBinContent(bin+1)
        if Names[hist]=='WJets':WjetBin[bin]+=histos[hist].GetBinContent(bin+1)


    fout.write("==================Contribution from : "+str(Names[hist])+"========================\n")
    fout.write(json.dumps(bins))
    fout.write("\n")
    fout.write("\n")
    fout.write("\n")
    # print ("==================Contribution from : ",Names[hist],"========================+\n")
    # print ("")
    # print (bins)
    # print ("")
    # print ("====================================================================+\n")

print (BinSum)
print (WjetBin)

fout.close()
fraction=[]
frac_dic={}
fout2=open('BinFraction.txt','w')
for i in range(len(histos)):
    fraction.append(WjetBin[i]/BinSum[i])
    frac_dic[Label[i]]=WjetBin[i]/BinSum[i]

fout2.write(json.dumps(frac_dic))
fout2.close()
