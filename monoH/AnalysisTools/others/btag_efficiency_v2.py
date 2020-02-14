#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, AddressOf, gROOT, TNamed
import ROOT as ROOT
import os,traceback
import sys, optparse,argparse
from array import array
import math
import numpy as numpy
import pandas
from root_pandas import read_root
from pandas import  DataFrame, concat
from pandas import Series
import time
import glob

## for parallel threads in interactive running
from multiprocessing import Process
import multiprocessing as mp


isCondor = False

## user packages
## in local dir
sys.path.append('configs')
import  triggers as trig
import variables as branches
import filters as filters
import genPtProducer as GenPtProd

## from commonutils
if isCondor:sys.path.append('ExoPieUtils/commonutils/')
else:sys.path.append('../ExoPieUtils/commonutils/')
import MathUtils as mathutil
from MathUtils import *
import BooleanUtils as boolutil


## from analysisutils
if isCondor:sys.path.append('ExoPieUtils/analysisutils/')
else:sys.path.append('../ExoPieUtils/analysisutils/')
import analysis_utils as anautil

######################################################################################################
## All import are done before this
######################################################################################################


runInteractive = False
runOn2016 = False
runOn2017 = False

## ----- start if clock

start = time.clock()


## ----- command line argument
usage = "analyzer for bb+DM (debugging) "
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-i", "--inputfile",  dest="inputfile",default="myfiles.txt")
parser.add_argument("-inDir", "--inputDir",  dest="inputDir",default=".")
parser.add_argument("-runOnTXT", "--runOnTXT",action="store_true", dest="runOnTXT")
parser.add_argument("-o", "--outputfile", dest="outputfile", default="out.root")
parser.add_argument("-D", "--outputdir", dest="outputdir")
parser.add_argument("-F", "--farmout", action="store_true",  dest="farmout")
parser.add_argument("-y", "--year", dest="year", default="Year")

#parser.add_argument("runOnTXT", "--runOnTXT",dest="runOnTXT")
#parser.set_defaults(runOnTXT=False)
## add argument for debug, default to be false

args = parser.parse_args()

if args.farmout==None:
    isfarmout = False
else:
    isfarmout = args.farmout

if args.inputDir and isfarmout:
    dirName=args.inputDir

if args.year=='2016':
    runOn2016=True
elif args.year=='2017':
    runOn2017=True
else:
    print('Please provide on which year you want to run?')

runOnTxt=False
if args.runOnTXT:
    runOnTxt = True

if isfarmout:
    infile  = args.inputfile

else: print "No file is provided for farmout"


outputdir = '.'
if args.outputdir:
    outputdir = str(args.outputdir)

infilename = "ExoPieElementTuples.root"

debug_ = False
#please provide the latest recommended working points from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation
if runOn2016:
    LWP = 0.2217
    MWP = 0.6321
    TWP = 0.8953
if runOn2017:
    LWP = 0.1522
    MWP = 0.4941
    TWP = 0.8001

def whichsample(filename):
    sample = -999
    if "TTT" in filename:
        sample = 6
    elif "WJetsToLNu_HT" in filename:
        sample = 24
    elif "ZJetsToNuNu_HT" in filename:
        sample = 23
    return sample

def TextToList(textfile):
    return([iline.rstrip()    for iline in open(textfile)])

## the input file list and key is caught in one variable as a python list,
#### first element is the list of rootfiles
#### second element is the key, user to name output.root

def runbbdm(txtfile):
    infile_=[]
    outfilename=""
    prefix="Skimmed_"
    ikey_ = ""

    if not runInteractive:
        print "running for ", txtfile
        infile_  = TextToList(txtfile)
        outfile = txtfile.split('/')[-1].replace('.txt','.root')
        #key_=txtfile[1]


        outfilename= outfile#prefix+key_+".root"
        print "outfilename", outfilename

    if runInteractive:
	infile_=TextToList(txtfile)
        #print "running code for ",infile_
        prefix_ = '' 
        if outputdir!='.': prefix_ = outputdir+'/'
        #print "prefix_", prefix_
        outfilename = prefix_+txtfile.split('/')[-1].replace('.txt','.root')#"SkimmedTree.root"
        print 'outfilename',  outfilename

    samplename = whichsample(outfilename)

    bins_pT     = [20.0,50.0,80.0,120.0,200.0,300.0,400.0,500.0,700.0,1000.0]
    bins_eta    = [-2.5,-1.5,-0.5,0.0,0.5,1.5,2.5]

    h_btag_num_pass_mwp    =  TH2D("h_btag_num_pass_mwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_btag_num_fail_mwp    =  TH2D("h_btag_num_fail_mwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_btag_den             =  TH2D("h_btag_den","",6,array('d',bins_eta),9,array('d',bins_pT))

    h_ctag_num_pass_mwp    =  TH2D("h_ctag_num_pass_mwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_ctag_num_fail_mwp    =  TH2D("h_ctag_num_fail_mwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_ctag_den             =  TH2D("h_ctag_den","",6,array('d',bins_eta),9,array('d',bins_pT))

    h_lighttag_num_pass_mwp=  TH2D("h_lighttag_num_pass_mwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_lighttag_num_fail_mwp=  TH2D("h_lighttag_num_fail_mwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_lighttag_den         =  TH2D("h_lighttag_den","",6,array('d',bins_eta),9,array('d',bins_pT))



    h_btag_num_pass_lwp    = TH2D("h_btag_num_pass_lwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_btag_num_fail_lwp    = TH2D("h_btag_num_fail_lwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_btag_den             = TH2D("h_btag_den","",6,array('d',bins_eta),9,array('d',bins_pT))

    h_ctag_num_pass_lwp    = TH2D("h_ctag_num_pass_lwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_ctag_num_fail_lwp    = TH2D("h_ctag_num_fail_lwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_ctag_den             = TH2D("h_ctag_den","",6,array('d',bins_eta),9,array('d',bins_pT))

    h_lighttag_num_pass_lwp= TH2D("h_lighttag_num_pass_lwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_lighttag_num_fail_lwp= TH2D("h_lighttag_num_fail_lwp","",6,array('d',bins_eta),9,array('d',bins_pT))
    h_lighttag_den         = TH2D("h_lighttag_den","",6,array('d',bins_eta),9,array('d',bins_pT))


    passfilename = open("configs/outfilename.txt","w")

    passfilename.write(outfilename)
    passfilename.close()

    ## this will give some warning, but that is safe,
    from  outputTree  import *

    ## following can be moved to outputtree.py if we manage to change the name of output root file.
    outfilenameis = outfilename
    outfile = TFile(outfilenameis,'RECREATE')

    ## following can be moved to outputtree.py if we manage to change the name of output root file.

    if runOn2016:
        jetvariables = branches.allvars2016
    elif runOn2017:
        jetvariables = branches.allvars2017

    filename = infile_

    ieve = 0;icount = 0
    #print "running on", filename
    for df in read_root(filename, 'tree/treeMaker', columns=jetvariables, chunksize=125000):
        if runOn2016:
            var_zip = zip(df.runId,df.lumiSection,df.eventId,df.isData,df.mcWeight,\
                       df.pu_nTrueInt,df.pu_nPUVert,\
                       df.hlt_trigName,df.hlt_trigResult,df.hlt_filterName,df.hlt_filterResult,\
                       df.pfMetCorrPt,df.pfMetCorrPhi,df.pfMetCorrUnc,\
                       df.nEle,df.elePx,df.elePy,df.elePz,df.eleEnergy,df.eleIsPassVeto, df.eleIsPassLoose,df.eleIsPassTight,\
                       df.eleCharge,df.nPho,df.phoPx,df.phoPy,df.phoPz,df.phoEnergy,df.phoIsPassLoose,df.phoIsPassTight,\
                       df.nMu,df.muPx,df.muPy,df.muPz,df.muEnergy,df.isLooseMuon,df.isTightMuon,df.PFIsoLoose, df.PFIsoMedium, df.PFIsoTight, df.PFIsoVeryTight, df.muCharge,\
                       df.HPSTau_n,df.HPSTau_Px,df.HPSTau_Py,df.HPSTau_Pz,df.HPSTau_Energy,df.disc_decayModeFinding,df.disc_byLooseIsolationMVArun2017v2DBoldDMwLT2017,df.disc_byMediumIsolationMVArun2017v2DBoldDMwLT2017,df.disc_byTightIsolationMVArun2017v2DBoldDMwLT2017,\
                       df.disc_againstMuonLoose3,df.disc_againstMuonTight3,df.disc_againstElectronLooseMVA6,df.disc_againstElectronMediumMVA6,df.disc_againstElectronTightMVA6,\
                       df.nGenPar,df.genParId,df.genMomParId,df.genParSt,df.genParPx,df.genParPy,df.genParPz,df.genParE,\
                       df.THINnJet,df.THINjetPx,df.THINjetPy,df.THINjetPz,df.THINjetEnergy,\
                       df.THINjetPassIDLoose,df.THINjetDeepCSV_b,df.THINjetHadronFlavor,df.THINjetNHadEF,df.THINjetCHadEF,\
                       df.THINjetCEmEF,df.THINjetCorrUncUp,df.THINjetNPV, \
                       df.FATnJet, df.FATjetPx, df.FATjetPy, df.FATjetPz, df.FATjetEnergy, df.FATjetPassIDLoose,\
                       df.FATjet_DoubleSV, df.FATjet_probQCDb, df.FATjet_probHbb, df.FATjet_probQCDc, df.FATjet_probHcc, df.FATjet_probHbbc,\
                       df.FATjet_prob_bbvsLight, df.FATjet_prob_ccvsLight, df.FATjet_prob_TvsQCD, df.FATjet_prob_WvsQCD, df.FATjet_prob_ZHbbvsQCD,\
                       df.FATjetSDmass, df.FATN2_Beta1_, df.FATN2_Beta2_, df.FATjetCHSPRmassL2L3Corr, df.FATjetCHSSDmassL2L3Corr)
        elif runOn2017:
            var_zip = zip(df.runId,df.lumiSection,df.eventId,df.isData,df.mcWeight,\
                       df.pu_nTrueInt,df.pu_nPUVert,\
                       df.hlt_trigName,df.hlt_trigResult,df.hlt_filterName,df.hlt_filterResult,\
                       df.pfMetCorrPt,df.pfMetCorrPhi,df.pfMetCorrUnc,\
                       df.nEle,df.elePx,df.elePy,df.elePz,df.eleEnergy,df.eleIsPassVeto, df.eleIsPassLoose,df.eleIsPassTight,\
                       df.eleCharge,df.nPho,df.phoPx,df.phoPy,df.phoPz,df.phoEnergy,df.phoIsPassLoose,df.phoIsPassTight,\
                       df.nMu,df.muPx,df.muPy,df.muPz,df.muEnergy,df.isLooseMuon,df.isTightMuon,df.PFIsoLoose, df.PFIsoMedium, df.PFIsoTight, df.PFIsoVeryTight, df.muCharge,\
                       df.HPSTau_n,df.HPSTau_Px,df.HPSTau_Py,df.HPSTau_Pz,df.HPSTau_Energy,df.disc_decayModeFinding,df.disc_byLooseIsolationMVArun2017v2DBoldDMwLT2017,df.disc_byMediumIsolationMVArun2017v2DBoldDMwLT2017,df.disc_byTightIsolationMVArun2017v2DBoldDMwLT2017,\
                       df.disc_againstMuonLoose3,df.disc_againstMuonTight3,df.disc_againstElectronLooseMVA6,df.disc_againstElectronMediumMVA6,df.disc_againstElectronTightMVA6,\
                       df.nGenPar,df.genParId,df.genMomParId,df.genParSt,df.genParPx,df.genParPy,df.genParPz,df.genParE,\
                       df.THINnJet,df.THINjetPx,df.THINjetPy,df.THINjetPz,df.THINjetEnergy,\
                       df.THINjetPassIDTight,df.THINjetDeepCSV_b,df.THINjetHadronFlavor,df.THINjetNHadEF,df.THINjetCHadEF,\
                       df.THINjetCEmEF,df.THINjetCorrUncUp,df.THINjetNPV, \
                       df.FATnJet, df.FATjetPx, df.FATjetPy, df.FATjetPz, df.FATjetEnergy, df.FATjetPassIDTight,\
                       df.FATjet_DoubleSV, df.FATjet_probQCDb, df.FATjet_probHbb, df.FATjet_probQCDc, df.FATjet_probHcc, df.FATjet_probHbbc,\
                       df.FATjet_prob_bbvsLight, df.FATjet_prob_ccvsLight, df.FATjet_prob_TvsQCD, df.FATjet_prob_WvsQCD, df.FATjet_prob_ZHbbvsQCD,\
                       df.FATjetSDmass, df.FATN2_Beta1_, df.FATN2_Beta2_, df.FATjetCHSPRmassL2L3Corr, df.FATjetCHSSDmassL2L3Corr)
        for run,lumi,event,isData,mcWeight_,\
                pu_nTrueInt_,pu_nPUVert_,\
                trigName_,trigResult_,filterName,filterResult,\
                met_,metphi_,metUnc_,\
                nele_,elepx_,elepy_,elepz_,elee_,elevetoid_, elelooseid_,eletightid_,\
                eleCharge_, npho_,phopx_,phopy_,phopz_,phoe_,pholooseid_,photightID_,\
                nmu_,mupx_,mupy_,mupz_,mue_,mulooseid_,mutightid_,muisoloose, muisomedium, muisotight, muisovtight, muCharge_,\
                nTau_,tau_px_,tau_py_,tau_pz_,tau_e_,tau_dm_,tau_isLoose_,tau_isoMedium_,tau_isoTight_,\
                Taudisc_againstLooseMuon,Taudisc_againstTightMuon,Taudisc_againstLooseElectron,Taudisc_againstMediumElectron,Taudisc_againstTightElectron,\
                nGenPar_,genParId_,genMomParId_,genParSt_,genpx_,genpy_,genpz_,gene_,\
                nak4jet_,ak4px_,ak4py_,ak4pz_,ak4e_,\
                ak4PassID_,ak4deepcsv_,ak4flavor_,ak4NHEF_,ak4CHEF_,\
                ak4CEmEF_,ak4JEC_, ak4NPV_,\
                fatnJet, fatjetPx, fatjetPy, fatjetPz, fatjetEnergy,fatjetPassID,\
                fatjet_DoubleSV, fatjet_probQCDb, fatjet_probHbb, fatjet_probQCDc, fatjet_probHcc, fatjet_probHbbc,\
                fatjet_prob_bbvsLight, fatjet_prob_ccvsLight, fatjet_prob_TvsQCD, fatjet_prob_WvsQCD, fatjet_prob_ZHbbvsQCD,\
                fatjetSDmass, fatN2_Beta1_, fatN2_Beta2_, fatjetCHSPRmassL2L3Corr, fatjetCHSSDmassL2L3Corr\
                in var_zip:


            if ieve%1000==0: print "Processed",ieve,"Events"
            ieve = ieve + 1
            # -------------------------------------------------
            # MC Weights
            # -------------------------------------------------
            mcweight[0] = 0.0
            if isData==1:   mcweight[0] =  1.0
            if not isData :
                if mcWeight_<0:  mcweight[0] = -1.0
                if mcWeight_>0:  mcweight[0] =  1.0
            #h_total.Fill(1.);
            #h_total_mcweight.Fill(1.,mcweight[0]);

            # -------------------------------------------------
            ## Trigger selection
            # -------------------------------------------------

            eletrigdecision=False
            mudecision=False
            metdecision=False
            phodecision=False

            eletrigstatus = [( anautil.CheckFilter(trigName_, trigResult_, trig.Electrontrigger2017[itrig] ) ) for itrig in range(len(trig.Electrontrigger2017))]
            mutrigstatus  = [( anautil.CheckFilter(trigName_, trigResult_, trig.Muontrigger2017[itrig]     ) ) for itrig in range(len(trig.Muontrigger2017))    ]
            mettrigstatus = [( anautil.CheckFilter(trigName_, trigResult_, trig.METtrigger2017[itrig]       ) ) for itrig in range(len(trig.METtrigger2017))     ]
            photrigstatus = [( anautil.CheckFilter(trigName_, trigResult_, trig.Photontrigger2017[itrig]   ) ) for itrig in range(len(trig.Photontrigger2017))  ]

            eletrigdecision = boolutil.logical_OR(eletrigstatus)
            mutrigdecision  = boolutil.logical_OR(mutrigstatus)
            mettrigdecision = boolutil.logical_OR(mettrigstatus)
            photrigdecision = boolutil.logical_OR(photrigstatus)

            if not isData:
                eletrigdecision = True
                mutrigdecision = True
                mettrigdecision = True
                photrigdecision = True


            # ------------------------------------------------------
            ## Filter selection
            # ------------------------------------------------------
            filterdecision=False
            filterstatus = [False for ifilter in range(len(filters.filters2017)) ]
            filterstatus = [anautil.CheckFilter(filterName, filterResult, filters.filters2017[ifilter]) for ifilter in range(len(filters.filters2017)) ]


            if not isData:     filterdecision = True
            if isData:         filterdecision  = boolutil.logical_AND(filterstatus)

            if filterdecision == False: continue



            # ------------------------------------------------------
            ## PFMET Selection
            # --------------------------------------------------------
            pfmetstatus = ( met_ > 200. )

            '''
            *******   *      *   ******
            *     *   *      *  *      *
            *******   ********  *      *
            *         *      *  *      *
            *         *      *   ******
            '''

            phopt = [getPt(phopx_[ip], phopy_[ip]) for ip in range(npho_)]
            phoeta = [getEta(phopx_[ip], phopy_[ip], phopz_[ip]) for ip in range(npho_)]

            pho_pt15_eta2p5_looseID = [ (phopt[ip] > 15.0) and (abs(phoeta[ip]) < 2.5) and (pholooseid_[ip])               for ip in range(npho_)]
            pass_pho_index = boolutil.WhereIsTrue(pho_pt15_eta2p5_looseID)

            '''
            ****   *      ****
            *      *      *
            ***    *      ***
            *      *      *
            ****   ****   ****
            '''
            elept = [getPt(elepx_[ie], elepy_[ie]) for ie in range(nele_)]
            eleeta = [getEta(elepx_[ie], elepy_[ie], elepz_[ie]) for ie in range(nele_)]
            elephi = [getPhi(elepx_[ie], elepy_[ie]) for ie in range(nele_)]

            ele_pt10_eta2p5_vetoID   = [(elept[ie] > 10.0) and (elevetoid_[ie])  and (((abs(eleeta[ie]) > 1.566 or abs(eleeta[ie]) < 1.4442) and (abs(eleeta[ie]) < 2.5))) for ie in range(nele_)]
            ele_pt10_eta2p5_looseID  = [(elept[ie] > 10.0) and (elelooseid_[ie]) and (((abs(eleeta[ie]) > 1.566 or abs(eleeta[ie]) < 1.4442) and (abs(eleeta[ie]) < 2.5))) for ie in range(nele_)]
            ele_pt40_eta2p5_tightID  = [(elept[ie] > 40.0) and (eletightid_[ie]) and (((abs(eleeta[ie]) > 1.566 or abs(eleeta[ie]) < 1.4442) and (abs(eleeta[ie]) < 2.5))) for ie in range(nele_)]

            pass_ele_veto_index      = boolutil.WhereIsTrue(ele_pt10_eta2p5_vetoID)
            pass_ele_loose_index    = boolutil.WhereIsTrue(ele_pt10_eta2p5_looseID)
            pass_ele_tight_index     = boolutil.WhereIsTrue(ele_pt40_eta2p5_tightID)

            '''
            **     *  *     *
            * *  * *  *     *
            *  *   *  *     *
            *      *  *     *
            *      *   *****
            '''
            mupt = [getPt(mupx_[imu], mupy_[imu]) for imu in range(nmu_)]
            mueta = [getEta(mupx_[imu], mupy_[imu], mupz_[imu]) for imu in range(nmu_)]
            muphi = [getPhi(mupx_[imu], mupy_[imu]) for imu in range(nmu_)]

            mu_pt10_eta2p4_looseID_looseISO  = [ ( (mupt[imu] > 10.0) and (abs(mueta[imu]) < 2.4 ) and (mulooseid_[imu])  and (muisoloose[imu]) )  for imu in range(nmu_) ]
            mu_pt30_eta2p4_tightID_tightISO  = [ ( (mupt[imu] > 30.0) and (abs(mueta[imu]) < 2.4 ) and (mutightid_[imu])  and (muisotight[imu]) )  for imu in range(nmu_) ]

            pass_mu_loose_index = boolutil.WhereIsTrue(mu_pt10_eta2p4_looseID_looseISO)
            pass_mu_tight_index     = boolutil.WhereIsTrue(mu_pt30_eta2p4_tightID_tightISO)


            '''
            *******   *****   *******
               *      *          *
               *      ****       *
               *      *          *
            ***       *****      *
            '''
            ak4pt = [getPt(ak4px_[ij], ak4py_[ij]) for ij in range(nak4jet_)]
            ak4eta = [getEta(ak4px_[ij], ak4py_[ij], ak4pz_[ij]) for ij in range(nak4jet_)]
            ak4phi = [getPhi(ak4px_[ij], ak4py_[ij]) for ij in range(nak4jet_)]

            ak4_pt30_eta4p5_IDT  = [ ( (ak4pt[ij] > 30.0) and (abs(ak4eta[ij]) < 4.5) and (ak4PassID_[ij] ) ) for ij in range(nak4jet_)]

            ##--- jet cleaning
            jetCleanAgainstEle = []
            jetCleanAgainstMu = []
            pass_jet_index_cleaned = []


            if len(ak4_pt30_eta4p5_IDT) > 0:
                DRCut = 0.4
                jetCleanAgainstEle = anautil.jetcleaning(ak4_pt30_eta4p5_IDT, ele_pt10_eta2p5_vetoID, ak4eta, eleeta, ak4phi, elephi, DRCut)
                jetCleanAgainstMu  = anautil.jetcleaning(ak4_pt30_eta4p5_IDT, mu_pt10_eta2p4_looseID_looseISO, ak4eta, mueta, ak4phi, muphi, DRCut)
                jetCleaned = boolutil.logical_AND_List3(ak4_pt30_eta4p5_IDT,jetCleanAgainstEle, jetCleanAgainstMu)
                pass_jet_index_cleaned = boolutil.WhereIsTrue(jetCleaned)
                if debug_:print "pass_jet_index_cleaned = ", pass_jet_index_cleaned,"nJets= ",len(ak4px_)



            ## Fill variables for the CRs.
            ## Fill variables for the CRs.
            WmunuRecoilPt = -9999.0
            WenuRecoilPt  = -9999.0
            ZmumuRecoilPt = -9999.0
            ZeeRecoilPt   = -9999.0
            

            # ------------------
            # Z CR
            # ------------------
            ## for dielectron
            if len(pass_ele_loose_index)==2 and (len(pass_ele_tight_index)==1 or len(pass_ele_tight_index)==2):
                iele1=pass_ele_loose_index[0]
                iele2=pass_ele_loose_index[1]
                if eleCharge_[iele1]*eleCharge_[iele2]<0:
                    ee_mass = InvMass(elepx_[iele1],elepy_[iele1],elepz_[iele1],elee_[iele1],elepx_[iele2],elepy_[iele2],elepz_[iele2],elee_[iele2])
                    zeeRecoilPx = -( met_*math.cos(metphi_) + elepx_[iele1] + elepx_[iele2])
                    zeeRecoilPy = -( met_*math.sin(metphi_) + elepy_[iele1] + elepy_[iele2])
                    ZeeRecoilPt =  math.sqrt(zeeRecoilPx**2  +  zeeRecoilPy**2)
            ## for dimu
            if len(pass_mu_loose_index) ==2 and (len(pass_mu_tight_index)==1 or len(pass_mu_tight_index)==2):
                imu1=pass_mu_loose_index[0]
                imu2=pass_mu_loose_index[1]
                if muCharge_[imu1]*muCharge_[imu2]<0:
                    mumu_mass = InvMass(mupx_[imu1],mupy_[imu1],mupz_[imu1],mue_[imu1],mupx_[imu2],mupy_[imu2],mupz_[imu2],mue_[imu2] )
                    zmumuRecoilPx = -( met_*math.cos(metphi_) + mupx_[imu1] + mupx_[imu2])
                    zmumuRecoilPy = -( met_*math.sin(metphi_) + mupy_[imu1] + mupy_[imu2])
                    ZmumuRecoilPt =  math.sqrt(zmumuRecoilPx**2  +  zmumuRecoilPy**2)


            # ------------------
            # W CR
            # ------------------
            ## for Single electron
            if len(pass_ele_tight_index) == 1 and len(pass_ele_loose_index)==1:
               ele1 = pass_ele_loose_index[0]
               #e_mass = MT(elept[ele1],met_, DeltaPhi(elephi[ele1],metphi_)) #transverse mass defined as sqrt{2pT*MET*(1-cos(dphi)}
               WenuRecoilPx = -( met_*math.cos(metphi_) + elepx_[ele1])
               WenuRecoilPy = -( met_*math.sin(metphi_) + elepy_[ele1])
               WenuRecoilPt = math.sqrt(WenuRecoilPx**2  +  WenuRecoilPy**2)



            ## for Single muon
            if len(pass_mu_loose_index) == 1 and len(pass_mu_tight_index)==1:
               mu1 = pass_mu_loose_index[0]
               #mu_mass = MT(mupt[mu1],met_, DeltaPhi(muphi[mu1],metphi_)) #transverse mass defined as sqrt{2pT*MET*(1-cos(dphi)}
               WmunuRecoilPx = -( met_*math.cos(metphi_) + mupx_[mu1])
               WmunuRecoilPy = -( met_*math.sin(metphi_) + mupy_[mu1])
               WmunuRecoilPt = math.sqrt(WmunuRecoilPx**2  +  WmunuRecoilPy**2)



            RecoilCond = False

            if (WmunuRecoilPt > 200.0 or WenuRecoilPt > 200.0 or ZmumuRecoilPt > 200.0 or ZeeRecoilPt > 200.0 ): RecoilCond=True

            if not RecoilCond: continue

            for ithinjet in pass_jet_index_cleaned:

                #==================== for flavor 5 ==================================

                if ak4flavor_[ithinjet]==5:
                    h_btag_den.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                    if ak4deepcsv_[ithinjet] > LWP:
                        h_btag_num_pass_lwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])
                    else:
                        h_btag_num_fail_lwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                    if ak4deepcsv_[ithinjet] > MWP:
                        h_btag_num_pass_mwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])
                    else:
                        h_btag_num_fail_mwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                #==================== for flavor 4 ==================================

                if ak4flavor_[ithinjet]==4:
                    h_ctag_den.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                    if ak4deepcsv_[ithinjet] > LWP:
                        h_ctag_num_pass_lwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                    else:
                        h_ctag_num_fail_lwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                    if ak4deepcsv_[ithinjet] > MWP:
                        h_ctag_num_pass_mwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                    else:
                        h_ctag_num_fail_mwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])

                #==================== for light flavor  ==================================

                if ak4flavor_[ithinjet]!=4 and ak4flavor_[ithinjet]!=5:
                    h_lighttag_den.Fill(ak4eta[ithinjet],ak4pt[ithinjet])
                    

                    if ak4deepcsv_[ithinjet] > LWP:
                        h_lighttag_num_pass_lwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])
                    else:
                        h_lighttag_num_fail_lwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])


                    if ak4deepcsv_[ithinjet] > MWP:
                        h_lighttag_num_pass_mwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])
                    else:
                        h_lighttag_num_fail_mwp.Fill(ak4eta[ithinjet],ak4pt[ithinjet])




    outfile.cd()
    h_btag_num_pass_mwp.Write()
    h_btag_num_fail_mwp.Write()
    h_btag_num_pass_lwp.Write()
    h_btag_num_fail_lwp.Write()
    h_btag_den.Write()
    h_ctag_num_pass_mwp.Write()
    h_ctag_num_fail_mwp.Write()
    h_ctag_num_pass_lwp.Write()
    h_ctag_num_fail_lwp.Write()

    h_ctag_den.Write()

    h_lighttag_num_pass_mwp.Write()
    h_lighttag_num_fail_mwp.Write()

    h_lighttag_num_pass_lwp.Write()
    h_lighttag_num_fail_lwp.Write()

    h_lighttag_den.Write()


    outfile.Write()
    print "output written to ", outfilename
    end = time.clock()
    print "%.4gs" % (end-start)

#files=["/eos/cms//store/group/phys_exotica/bbMET/ExoPieElementTuples/MC_2017miniaodV2_V1/WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8/DYJetsToLL_M_50_HT_400to600_TuneCP5_13TeV_30K/190825_203128/0000/ExoPieElementTuples_1.root", "/eos/cms//store/group/phys_exotica/bbMET/ExoPieElementTuples/MC_2017miniaodV2_V1/WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8/DYJetsToLL_M_50_HT_400to600_TuneCP5_13TeV_30K/190825_203128/0000/ExoPieElementTuples_2.root"]

if __name__ == '__main__':
    if not runInteractive:
        txtFile=infile

        runbbdm(txtFile)

    if runInteractive and runOnTxt:
	filesPath = dirName+'/*txt'
	files     = glob.glob(filesPath)
        n = 8 #submit n txt files at a time, make equal to cores
        final = [files[i * n:(i + 1) * n] for i in range((len(files) + n - 1) // n )]
        print 'final', final
        for i in range(len(final)):
            print 'first set', final[i]

            try:
                pool = mp.Pool(8)
                pool.map(runbbdm,final[i])
                pool.close()
                pool.join()
	    except Exception as e:
		print e
		print "Corrupt file inside input txt file is detected! Skipping this txt file:  ", final[i]
		continue

    if runInteractive and not runOnTxt:
        ''' following part is for interactive running. This is still under testing because output file name can't be changed at this moment '''
        inputpath= "/eos/cms/store/group/phys_exotica/bbMET/ExoPieElementTuples/MC_2017miniaodV2_V1/"

        os.system('rm dirlist.txt')
        os.system("ls -1 "+inputpath+" > dirlist.txt")

        allkeys=[idir.rstrip() for idir in open('dirlist.txt')]
        alldirs=[inputpath+"/"+idir.rstrip() for idir in open('dirlist.txt')]

        pool = mp.Pool(6)
        allsample=[]
        for ikey in allkeys:
            dirpath=inputpath+"/"+ikey
            txtfile=ikey+".txt"
            os.system ("find "+dirpath+"  -name \"*.root\" | grep -v \"failed\"  > "+txtfile)
            fileList=TextToList(txtfile)
            ## this is the list, first element is txt file with all the files and second element is the ikey (kind of sample name identifier)
            sample_  = [txtfile, ikey]
            ## push information about one sample into global list.
            allsample.append(sample_)
        print allsample
        pool.map(runbbdm, allsample)
        ## this works fine but the output file name get same value becuase it is done via a text file at the moment, need to find a better way,
