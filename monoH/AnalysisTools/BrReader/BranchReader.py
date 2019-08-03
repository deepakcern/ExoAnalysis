#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math
import AllQuantList
import Selections
ROOT.gROOT.SetBatch(True)
from bbMETQuantities import *

n2ddtcalFile=TFile('scalefactors/h3_n2ddt.root')
trans_h2ddt=n2ddtcalFile.Get("h2ddt")

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-i", "--inputfile",  dest="inputfile")
parser.add_option("-o", "--outputfile", dest="outputfile")
parser.add_option("-D", "--outputdir", dest="outputdir")
parser.add_option("-a", "--analyze", action="store_true",  dest="analyze")
parser.add_option("-F", "--farmout", action="store_true",  dest="farmout")


(options, args) = parser.parse_args()

if options.farmout==None:
    isfarmout = False
else:
    isfarmout = options.farmout


inputfilename = options.inputfile
outputdir = options.outputdir

pathlist = inputfilename.split("/")
sizeoflist = len(pathlist)
#print ('sizeoflist = ',sizeoflist)
rootfile='tmphist'
rootfile = pathlist[sizeoflist-1]
textfile = rootfile+".txt"

print "rootfile", rootfile

if outputdir!='.': os.system('mkdir -p '+outputdir)

if options.outputfile is None or options.outputfile==rootfile:
    if not isfarmout:
        outputfilename = "/Output_"+rootfile
    else:
        outputfilename = "/Output_"+rootfile.split('.')[0]+".root"
else:
    outputfilename = "/"+options.outputfile

outfilename = outputdir + outputfilename


print ("Input:",options.inputfile, "; Output:", outfilename)

skimmedTree = TChain("outTree")


def WhichSample(filename):
    samplename = 'all'
    if filename.find('WJets')>-1:
        samplename = 'WJETS'
    elif filename.find('ZJets')>-1 or filename.find('DYJets')>-1:
        samplename = 'ZJETS'
    elif filename.find('TT')>-1:
        samplename  = 'TT'
    else:
        samplename = 'all'
    return samplename


h_t = TH1F('h_t','h_t',2,0,2)
h_t_weight = TH1F('h_t_weight','h_t_weight',2,0,2)


samplename = 'all'
if isfarmout:
    infile = open(inputfilename)
    failcount=0
    for ifile in infile:
        try:
            f_tmp = TFile.Open(ifile.rstrip(),'READ')
            if f_tmp.IsZombie():
                failcount += 1
                continue
            skimmedTree.Add(ifile.rstrip())
            h_tmp = f_tmp.Get('h_total')
            h_tmp_weight = f_tmp.Get('h_total_mcweight')
            h_t.Add(h_tmp)
            h_t_weight.Add(h_tmp_weight)
        except:
            failcount += 1
    if failcount>0: print ("Could not read %d files. Skipping them." %failcount)

if not isfarmout:
    skimmedTree.Add(inputfilename)
    f_tmp = TFile.Open(inputfilename,'READ')
    h_tmp = f_tmp.Get('h_total')
    h_tmp_weight = f_tmp.Get('h_total_mcweight')
    h_t.Add(h_tmp)
    h_t_weight.Add(h_tmp_weight)


try:
    samplepath = str(f_tmp.Get('samplepath').GetTitle())
    if not isfarmout: print ("Original source file: " + samplepath)
except:
    samplepath='TT'
    print ("WARNING: Looks like the input was skimmed with an older version of SkimTree. Using " + samplepath + " as sample path. Gen pT Reweighting may NOT work.")

samplename = WhichSample(samplepath)
print ("Dataset classified as: " + samplename)


def Analyze():
    NEntries = skimmedTree.GetEntries()
    npass = 0
    allquantities = MonoHbbQuantities(outfilename)
    allquantities.defineHisto()
    CSVLWP=0.54
    for ievent in range(NEntries):
        skimmedTree.GetEntry(ievent)

        try:
            run                        = skimmedTree.__getattr__('st_runId')
            lumi                       = skimmedTree.__getattr__('st_lumiSection')
            event                      = skimmedTree.__getattr__('st_eventId')
            if ievent%100==0: print "Processed "+str(ievent)+" of "+str(NEntries)+" events."

            pfMet                      = skimmedTree.__getattr__('st_pfMetCorrPt')
            pfMetPhi                   = skimmedTree.__getattr__('st_pfMetCorrPhi')

            nTHINJets                  = skimmedTree.__getattr__('st_THINnJet')
            thinjetP4                  = skimmedTree.__getattr__('st_THINjetP4')
            thinJetCSV                 = skimmedTree.__getattr__('st_THINjetCISVV2')
            THINjetHadronFlavor        = skimmedTree.__getattr__('st_THINjetHadronFlavor')
            thinjetNhadEF              = skimmedTree.__getattr__('st_THINjetNHadEF')
            thinjetChadEF              = skimmedTree.__getattr__('st_THINjetCHadEF')
            thinjetNPV                 = skimmedTree.__getattr__('st_THINjetNPV')

            CA15njets                 = skimmedTree.__getattr__('st_CA15njets')
            CA15jetP4                 = skimmedTree.__getattr__('st_CA15jetP4')
            CA15SDmass                = skimmedTree.__getattr__('st_CA15SDmass_corr')
            CA15Puppi_doublebtag      = skimmedTree.__getattr__('st_CA15Puppi_doublebtag')
            CA15N2b1                  = skimmedTree.__getattr__('st_CA15N2b1')
            CA15PassIDTight           = skimmedTree.__getattr__('st_CA15PassIDTight')

            nPho                       = skimmedTree.__getattr__('st_nPho')
            phoP4                      = skimmedTree.__getattr__('st_phoP4')
            phoIsPassTight             = skimmedTree.__getattr__('st_phoIsPassTight')

            nEle                       = skimmedTree.__getattr__('st_nEle')
            eleP4                      = skimmedTree.__getattr__('st_eleP4')
            eleIsPassTight             = skimmedTree.__getattr__('st_eleIsPassTight')

            nMu                        = skimmedTree.__getattr__('st_nMu')
            muP4                       = skimmedTree.__getattr__('st_muP4')
            MuIso                      = skimmedTree.__getattr__('st_muIso')
            isTightMuon                = skimmedTree.__getattr__('st_isTightMuon')

            nTau                       = skimmedTree.__getattr__('st_HPSTau_n')
            isData                     = skimmedTree.__getattr__('st_isData')
            mcWeight                   = skimmedTree.__getattr__('mcweight')
            pu_nTrueInt                = int(skimmedTree.__getattr__('st_pu_nTrueInt'))
            pu_nPUVert                 = int(skimmedTree.__getattr__('st_pu_nPUVert'))

            nGenPar                    = skimmedTree.__getattr__('st_nGenPar')
            genParId                   = skimmedTree.__getattr__('st_genParId')
            genMomParId                = skimmedTree.__getattr__('st_genMomParId')
            genParSt                   = skimmedTree.__getattr__('st_genParSt')
            genParP4                   = skimmedTree.__getattr__('st_genParP4')

            WenuRecoil                 = skimmedTree.__getattr__('WenuRecoil')
            Wenumass                   = skimmedTree.__getattr__('Wenumass')
            WenuPhi                    = skimmedTree.__getattr__('WenuPhi')
            WmunuRecoil                = skimmedTree.__getattr__('WmunuRecoil')
            Wmunumass                  = skimmedTree.__getattr__('Wmunumass')
            WmunuPhi                   = skimmedTree.__getattr__('WmunuPhi')
            ZeeRecoil                  = skimmedTree.__getattr__('ZeeRecoil')
            ZeeMass                    = skimmedTree.__getattr__('ZeeMass')
            ZeePhi                     = skimmedTree.__getattr__('ZeePhi')
            ZmumuRecoil                = skimmedTree.__getattr__('ZmumuRecoil')
            ZmumuMass                  = skimmedTree.__getattr__('ZmumuMass')
            ZmumuPhi                   = skimmedTree.__getattr__('ZmumuPhi')


            HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v      = skimmedTree.__getattr__('st_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v')
            HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v    = skimmedTree.__getattr__('st_HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v')
            HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v    = skimmedTree.__getattr__('st_HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v')
            HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v    = skimmedTree.__getattr__('st_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v')
            HLT_PFMET170_                              = skimmedTree.__getattr__('st_HLT_PFMET170_')
            HLT_Ele105_CaloIdVT_GsfTrkIdT_v            = skimmedTree.__getattr__('st_HLT_Ele105_CaloIdVT_GsfTrkIdT_v')
            HLT_Ele27_WPTight_Gsf                      = skimmedTree.__getattr__('st_HLT_Ele27_WPTight_Gsf')

        except Exception as e:
            print (e)
            print ("Corrupt file detected! Skipping 1 event.")
            continue


        if isData:
            trigstatus = HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v or HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v or HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v or HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v or HLT_PFMET170_
            EleCRtrigstatus = (HLT_Ele105_CaloIdVT_GsfTrkIdT_v or HLT_Ele27_WPTight_Gsf)
        if not isData:
            trigstatus=True
            EleCRtrigstatus=True

        #==================================================== selections =================

        Selca15jetsP4=[]; SelN2DDT=[]; corrSD=[]; FatJDB=[]

        mybJetsP4=[];mybjets=[];myJetHadronFlavor=[]

        myJetP4=[]
        for i in range(CA15njets):
            if (bool(CA15PassIDTight[i])==False):continue
            fjet        =  CA15jetP4[i]
            corr_SDMass = CA15SDmass[i]
            N2          = CA15N2b1[i]
            fjdb        = CA15Puppi_doublebtag[i]
            if fjet.Pt() > 200. and abs(fjet.Eta()) < 2.4 and corr_SDMass > 100. and corr_SDMass < 150. and fjdb > 0.75:

                rh_8   = math.log((corr_SDMass*corr_SDMass)/(fjet.Pt()*fjet.Pt()))
                jpt_8  = fjet.Pt()
                cur_rho_index = trans_h2ddt.GetXaxis().FindBin(rh_8);
                cur_pt_index  = trans_h2ddt.GetYaxis().FindBin(jpt_8);
                if rh_8 > trans_h2ddt.GetXaxis().GetBinUpEdge( trans_h2ddt.GetXaxis().GetNbins() ): cur_rho_index = trans_h2ddt.GetXaxis().GetNbins();
                if rh_8 < trans_h2ddt.GetXaxis().GetBinLowEdge( 1 ): cur_rho_index = 1;
                if jpt_8 > trans_h2ddt.GetYaxis().GetBinUpEdge( trans_h2ddt.GetYaxis().GetNbins() ): cur_pt_index = trans_h2ddt.GetYaxis().GetNbins();
                if jpt_8 < trans_h2ddt.GetYaxis().GetBinLowEdge( 1 ): cur_pt_index = 1;

                n2ddt_ = N2 - trans_h2ddt.GetBinContent(cur_rho_index,cur_pt_index);

                Selca15jetsP4.append(fjet)
                SelN2DDT.append(n2ddt_)
                corrSD.append(corr_SDMass)
                FatJDB.append(CA15Puppi_doublebtag[i])


        for nb in range(nTHINJets):
            if isMatch(Selca15jetsP4, thinjetP4[nb],1.5):continue
            myJetP4.append(thinjetP4[nb])
            myJetHadronFlavor.append(THINjetHadronFlavor[nb])

            if thinJetCSV[nb] > CSVLWP and abs(thinjetP4[nb].Eta())<2.4:
                mybjets.append(nb)
                mybJetsP4.append(thinjetP4[nb])

        myJetNPV=thinjetNPV
        nBjets=len(mybjets)
        nJets=len(myJetP4)
        if not nJets <2:continue

        nFatJet=len(Selca15jetsP4)
        if nFatJet!=1: continue
        N2DDT = SelN2DDT[0]
        Fatjet1_pT=Selca15jetsP4[0].Pt()
        Fatjet1_eta=Selca15jetsP4[0].Eta()
        CA15SD=corrSD[0]

        dPhi_jet_MET_Cond = True; dPhi_jet_Zeerecoil_Cond = True ; dPhi_jet_Zmumurecoil_Cond = True ; dPhi_jet_Werecoil_Cond = True ; dPhi_jet_Wmurecoil_Cond = True
        if nJets ==1:
            j1 = myJetP4[0]
            min_dPhi_jet_MET = DeltaPhi(j1.Phi(),pfMetPhi)
            dPhi_jet_MET_Cond          = DeltaPhi(j1.Phi(),pfMetPhi) > 0.4
            dPhi_jet_Zeerecoil_Cond    = DeltaPhi(ZeePhi,j1.Phi()) > 0.4
            dPhi_jet_Zmumurecoil_Cond  = DeltaPhi(ZmumuPhi,j1.Phi()) > 0.4
            dPhi_jet_Werecoil_Cond     = DeltaPhi(WenuPhi,j1.Phi()) > 0.4
            dPhi_jet_Wmurecoil_Cond    = DeltaPhi(WmunuPhi,j1.Phi()) > 0.4


        #=================================== end of selections==================================

        allquantlist=AllQuantList.getAll()
        for quant in allquantlist:
            exec("allquantities."+quant+" = None")

        preselquantlist=AllQuantList.getPresel()
        for quant in preselquantlist:
            exec("allquantities."+quant+" = None")


        regquants=AllQuantList.getRegionQuants()
        for quant in regquants:
            exec("allquantities."+quant+" = None")

        #=================================get cut dictionary =================================
        writeSR=False
        cuts=Selections.getSel(nEle,nMu,nTau,nBjets,nPho,nFatJet,isTightMuon,MuIso,eleIsPassTight,pfMet,nJets,dPhi_jet_MET_Cond,dPhi_jet_Wmurecoil_Cond,dPhi_jet_Werecoil_Cond,dPhi_jet_Zeerecoil_Cond,dPhi_jet_Zmumurecoil_Cond,ZeeMass,ZmumuMass,N2DDT,WenuRecoil,WmunuRecoil,ZeeRecoil,ZmumuRecoil)

        if cuts['signal']:
            allquantities.ca15jet_pT_sr2             = Fatjet1_pT
            allquantities.met_sr2                    = pfMet
            allquantities.ca15jet_eta_sr2            = Fatjet1_eta
            allquantities.ca15jet_SD_sr2             = CA15SD
            writeSR=True
        if cuts['te']:
            allquantities.reg_1e2bT_Wmass            = Wenumass
            allquantities.reg_1e2bT_hadrecoil        = WenuRecoil
            allquantities.reg_1e2bT_MET              = pfMet
            allquantities.reg_1e2bT_ca15jet_pT       = Fatjet1_pT
            allquantities.reg_1e2bT_ca15jet_eta      = Fatjet1_eta
            allquantities.reg_1e2bT_ca15jet_SD       = CA15SD
            allquantities.reg_1e2bT_lep1_pT          = eleP4[0].Pt()
            allquantities.reg_1e2bT_lep1_eta         = eleP4[0].Eta()
            allquantities.reg_1e2bT_njet             = nJets
        if cuts['tm']:
            allquantities.reg_1mu2bT_Wmass           = Wmunumass
            allquantities.reg_1mu2bT_hadrecoil       = WmunuRecoil
            allquantities.reg_1mu2bT_MET             = pfMet
            allquantities.reg_1mu2bT_ca15jet_pT      = Fatjet1_pT
            allquantities.reg_1mu2bT_ca15jet_eta     = Fatjet1_eta
            allquantities.reg_1mu2bT_ca15jet_SD      = CA15SD
            allquantities.reg_1mu2bT_lep1_pT         = muP4[0].Pt()
            allquantities.reg_1mu2bT_lep1_eta        = muP4[0].Eta()
            allquantities.reg_1mu2bT_njet            = nJets
        if cuts['wen']:
            allquantities.reg_1e2bW_hadrecoil        = WenuRecoil
            allquantities.reg_1e2bW_MET              = pfMet
            allquantities.reg_1e2bW_ca15jet_pT       = Fatjet1_pT
            allquantities.reg_1e2bW_ca15jet_eta      = Fatjet1_eta
            allquantities.reg_1e2bW_ca15jet_SD       = CA15SD
            allquantities.reg_1e2bW_lep1_pT          = eleP4[0].Pt()
            allquantities.reg_1e2bW_lep1_eta         = eleP4[0].Eta()
            allquantities.reg_1e2bW_njet             = nJets
        if cuts['wmn']:
            allquantities.reg_1mu2bW_hadrecoil       = WmunuRecoil
            allquantities.reg_1mu2bW_MET             = pfMet
            allquantities.reg_1mu2bW_ca15jet_pT      = Fatjet1_pT
            allquantities.reg_1mu2bW_ca15jet_eta     = Fatjet1_eta
            allquantities.reg_1mu2bW_ca15jet_SD      = CA15SD
            allquantities.reg_1mu2bW_lep1_pT         = muP4[0].Pt()
            allquantities.reg_1mu2bW_lep1_eta        = muP4[0].Eta()
            allquantities.reg_1mu2bW_njet            = nJets



        if writeSR:
            npass +=1


        allweights = 1.0
        allquantities.weight          = allweights
        allquantities.FillRegionHisto()
        allquantities.FillHisto()

    print "passed events",npass




def isMatch(P4Coll, objP4, cut):
    match=False
    for ojb in range(len(P4Coll)):
        if DeltaR(P4Coll[ojb],objP4) < cut: match=True
        break
    return match

def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;

def DeltaPhi(phi1,phi2):
   phi = Phi_mpi_pi(phi1-phi2)

   return abs(phi)

def DeltaR(P4_1,P4_2):
    return math.sqrt(  (  P4_1.Eta()-P4_2.Eta() )**2  + (  DeltaPhi(P4_1.Phi(),P4_2.Phi()) )**2 )



if __name__ == "__main__":
    ## analyze the tree and make histograms and all the 2D plots and Efficiency plots.
    if options.analyze:
        print "now calling analyzedataset"
        Analyze()
