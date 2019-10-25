import sys,os,array

from array import array
from glob import glob

from ROOT import TFile, gROOT, kBlack,TH1F

gROOT.SetBatch(True)

#CRSRPath = '/Users/dekumar/MEGA/Fullwork/2017_Plotting/22102019/monoHROOT'
CRSRPath = '/home/deepak/MEGA/Fullwork/2017_Plotting/22102019/monoHROOT'
#SignalPath = '/Users/dekumar/MEGA/Fullwork/2017_Plotting/rootFiles_Signal'
SignalPath = '/home/deepak/MEGA/Fullwork/2017_Plotting/rootFiles_Signal'

CRSRFiles = [CRSRPath+'/'+fl for fl in os.listdir(CRSRPath) if 'Recoil' in fl or 'MET' in fl]
SignalFiles = [SignalPath+'/'+fl for fl in os.listdir(SignalPath) if '.root' in fl]

os.system('rm -rf DataCardRootFiles_test')
os.system('mkdir DataCardRootFiles_test')


def setHistStyle(h_temp,newname):

    #h_temp=h_temp2.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
    h_temp.SetName(newname)
    h_temp.SetTitle(newname)
    h_temp.SetLineWidth(1)
    #h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    #h_temp.SetBinContent(len(bins),0.)
    #h_temp.GetXaxis().SetRangeUser(200,1000)
    h_temp.SetMarkerColor(kBlack);
    h_temp.SetMarkerStyle(2);
    return h_temp


def reBin(h_temp,bins):

    h_temp=h_temp.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
    #h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    #h_temp.SetBinContent(len(bins),0.)
    # h_temp.GetXaxis().SetRangeUser(200,1000)
    #h_temp.SetMarkerColor(kBlack);
    #h_temp.SetMarkerStyle(2);
    return h_temp


CSList = {'ma_150_mA_300':1.606,'ma_150_mA_400':0.987,'ma_150_mA_500':0.5074,'ma_150_mA_600':0.2984,'ma_150_mA_1000':0.0419,'ma_150_mA_1200':0.0106,'ma_150_mA_1600':0.07525}


print ('CSList',CSList)

SRCRhistos=['bkgSum','DIBOSON','ZJets','GJets','QCD','SMH','STop','Top','WJets','DYJets','data_obs']

bins= [200,270,345,480,1000]

f=TFile("DataCardRootFiles_test/AllMETHistos.root","RECREATE")

for infile in CRSRFiles:
    print ('checking code for ',infile)
    fin       =   TFile(infile,"READ")
    rootFile  = infile.split('/')[-1]
    reg       = rootFile.split('_')[2]

    if ('MET' in infile and 'SR' not in infile):continue# or ('Recoil' not in infile): continue
    if 'TopWmu' in infile or 'TopWe' in infile:continue
    print ('running code for ',infile)
    reg = reg.replace('Zmumu','ZMUMU').replace('Zee','ZEE').replace('Wmu','WMU').replace('We','WE').replace('Topmu','TOPMU').replace('Tope','TOPE')

    for hist in SRCRhistos:
        temp   = fin.Get(hist)
        hist=hist.replace('DIBOSON','diboson').replace('ZJets','zjets').replace('GJets','gjets').replace('QCD','qcd').replace('SMH','smh').replace('STop','singlet').replace('Top','tt').replace('WJets','wjets').replace('DYJets','dyjets')
        newName   = 'monoHbb2017_B_'+reg+'_'+str(hist)

        if temp.Integral() == 0.0:
            HISTNAME=newName
            temp = TH1F(newName, newName, 4, array('d',bins))
            # print ('=================',hist)
            # print ('=================',temp.GetXaxis().GetNbins())
            for bin in range(4):
                temp.SetBinContent(bin+1,0.00001)

        myHist = setHistStyle(temp,newName)
        f.cd()
        myHist.Write()


lumi = 41.0*1000

BR = 0.588

for infile in SignalFiles:
    print ('infile',infile)
    fin       =   TFile(infile,"READ")
    rootFile = infile.split('/')[-1]
    ma=rootFile.split('_')[11]
    mA=rootFile.split('_')[9]

    if mA=='1400': continue

    sampStr = 'ma_'+ma+'_mA_'+mA
    CS = CSList[sampStr]
    temp = fin.Get('h_reg_SR_MET')

    if  temp.Integral() == 0.0:
        for bin in range(temp.GetXaxis().GetNbins()):
            temp.SetBinContent(bin,0.00001)

    h_total = fin.Get('h_total_mcweight')
    totalEvents = h_total.Integral()
    temp.Scale((lumi*CS*BR)/(totalEvents))
    samp = 'monoHbb2017_B_SR_ggF_sp_0p35_tb_1p0_mXd_10_mA_'+mA+'_ma_'+ma
    myHist = setHistStyle(temp,samp)
    f.cd()
    myHist.Write()


f.Close()
