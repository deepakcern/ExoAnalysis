#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math

ROOT.gROOT.SetBatch(True)

ROOT.gROOT.LoadMacro("Loader.h+")

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)


parser.add_option("-i", "--inputfile",  dest="inputfile")
parser.add_option("-o", "--outputfile", dest="outputfile")
parser.add_option("-D", "--outputdir", dest="outputdir")
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

if outputdir!='.': os.system('mkdir -p '+outputdir)

if options.outputfile is None or options.outputfile==rootfile:
    if not isfarmout:
        outputfilename = "/Output_"+rootfile
    else:
        outputfilename = "/Output_"+rootfile.split('.')[0]+".root"
else:
    outputfilename = "/"+options.outputfile



outfilename = outputdir + outputfilename
#else:
#    outfilename = options.outputfile

print "Input:",options.inputfile, "; Output:", outfilename


#outfilename= 'SkimmedTree.root'
skimmedTree = TChain("tree/treeMaker")

if isfarmout:
    infile = open(inputfilename)
    failcount=0
    for ifile in infile:
        try:
            f_tmp = TFile.Open(ifile.rstrip(),'READ')
            if f_tmp.IsZombie():            # or fileIsCorr(ifile.rstrip()):
                failcount += 1
                continue
            skimmedTree.Add(ifile.rstrip())
        except:
            failcount += 1
    if failcount>0: print "Could not read %d files. Skipping them." %failcount

if not isfarmout:
    skimmedTree.Add(inputfilename)

def AnalyzeDataSet():

    outfile = TFile(outfilename,'RECREATE')

    NEntries = skimmedTree.GetEntries()
    #NEntries = 1000000
    print 'NEntries = '+str(NEntries)
    npass = 0
    
    bins_pT     = [20.0,50.0,80.0,120.0,200.0,300.0,400.0,500.0,700.0,1000.0]
    bins_eta    = [0.0,0.5,1.5,2.5]

    h_btag_num_pass=TH2D("h_btag_num_pass","",3,array('d',bins_eta),9,array('d',bins_pT))
    h_btag_num_fail=TH2D("h_btag_num_fail","",3,array('d',bins_eta),9,array('d',bins_pT))
    h_btag_den=TH2D("h_btag_den","",3,array('d',bins_eta),9,array('d',bins_pT))

    h_ctag_num_pass=TH2D("h_ctag_num_pass","",3,array('d',bins_eta),9,array('d',bins_pT))
    h_ctag_num_fail=TH2D("h_ctag_num_fail","",3,array('d',bins_eta),9,array('d',bins_pT))
    h_ctag_den=TH2D("h_ctag_den","",3,array('d',bins_eta),9,array('d',bins_pT))

    h_lighttag_num_pass=TH2D("h_lighttag_num_pass","",3,array('d',bins_eta),9,array('d',bins_pT))
    h_lighttag_num_fail=TH2D("h_lighttag_num_fail","",3,array('d',bins_eta),9,array('d',bins_pT))
    h_lighttag_den=TH2D("h_lighttag_den","",3,array('d',bins_eta),9,array('d',bins_pT))

    CSVLWP = 0.54
    for ievent in range(NEntries):
        if ievent%100==0: print "Processed "+str(ievent)+" of "+str(NEntries)+" events."
        skimmedTree.GetEntry(ievent)
        ## Get all relevant branches
        try:

            nTHINJets                  = skimmedTree.__getattr__('THINnJet')
            thinjetP4                  = skimmedTree.__getattr__('THINjetP4')
            thinJetCSV                 = skimmedTree.__getattr__('THINjetCISVV2')
            passThinJetTightID         = skimmedTree.__getattr__('THINjetPassIDTight')
            THINjetHadronFlavor        = skimmedTree.__getattr__('THINjetHadronFlavor')
            nEle                       = skimmedTree.__getattr__('nEle')
            eleP4                      = skimmedTree.__getattr__('eleP4')
            eleIsPassVeto              = skimmedTree.__getattr__('eleIsPassVeto')
            eleCharge                  = skimmedTree.__getattr__('eleCharge')

            pfMet                      = skimmedTree.__getattr__('pfMetCorrPt')
            pfMetPhi                   = skimmedTree.__getattr__('pfMetCorrPhi')


            nMu                        = skimmedTree.__getattr__('nMu')
            muP4                       = skimmedTree.__getattr__('muP4')
            isLooseMuon                = skimmedTree.__getattr__('isLooseMuon')
            isMediumMuon               = skimmedTree.__getattr__('isMediumMuon')
            isTightMuon                = skimmedTree.__getattr__('isTightMuon')
            muChHadIso                 = skimmedTree.__getattr__('muChHadIso')
            muNeHadIso                 = skimmedTree.__getattr__('muNeHadIso')
            muGamIso                   = skimmedTree.__getattr__('muGamIso')
            muPUPt                     = skimmedTree.__getattr__('muPUPt')
            muCharge                   = skimmedTree.__getattr__('muCharge')


        except Exception as e:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue




        myEles=[]
        for iele in range(nEle):
            if (eleP4[iele].Pt() > 10. ) & (abs(eleP4[iele].Eta()) <2.5) & (bool(eleIsPassVeto[iele]) == True) :
                myEles.append(iele)

        myMuos = []
        for imu in range(nMu):
            if (muP4[imu].Pt()>10.) & (abs(muP4[imu].Eta()) < 2.4) & (bool(isLooseMuon[imu]) == True):
                relPFIso = (muChHadIso[imu]+ max(0., muNeHadIso[imu] + muGamIso[imu] - 0.5*muPUPt[imu]))/muP4[imu].Pt()
                if relPFIso<0.25 :
                    myMuos.append(imu)

        ## for Single electron
	WenuRecoilPt = 0.0
        if len(myEles) == 1:
           ele1 = myEles[0]
           p4_ele1 = eleP4[ele1]
           WenuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_ele1.Px())
           WenuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_ele1.Py())
           WenuRecoilPt = math.sqrt(WenuRecoilPx**2  +  WenuRecoilPy**2)

        ## for Single muon
        WmunuRecoilPt = 0.0
        if len(myMuos) == 1:
           mu1 = myMuos[0]
           p4_mu1 = muP4[mu1]
           WmunuRecoilPx = -( pfMet*math.cos(pfMetPhi) + p4_mu1.Px())
           WmunuRecoilPy = -( pfMet*math.sin(pfMetPhi) + p4_mu1.Py())
           WmunuRecoilPt = math.sqrt(WmunuRecoilPx**2  +  WmunuRecoilPy**2)

	RecoilCond = False

        if (WmunuRecoilPt > 200 or WenuRecoilPt > 200): RecoilCond=True

        if not RecoilCond: continue

        for nb in range(nTHINJets):
            if THINjetHadronFlavor[nb]==5:
                h_btag_den.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())
                if thinJetCSV[nb] > CSVLWP:
		    h_btag_num_pass.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())
		else:
		    h_btag_num_fail.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())


	    if THINjetHadronFlavor[nb]==4:
                h_ctag_den.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())
	        if thinJetCSV[nb] > CSVLWP:
		    h_ctag_num_pass.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())

		else:
		    h_ctag_num_fail.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())

	    if THINjetHadronFlavor[nb]!=4 and THINjetHadronFlavor[nb]!=5:
		h_lighttag_den.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())
                if thinJetCSV[nb] > CSVLWP:
                    h_lighttag_num_pass.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())
                else:
		    h_lighttag_num_fail.Fill(thinjetP4[nb].Eta(),thinjetP4[nb].Pt())

    outfile.cd()
    h_btag_num_pass.Write()
    h_btag_num_fail.Write()
    h_btag_den.Write()
    h_ctag_num_pass.Write()
    h_ctag_num_fail.Write()
    h_ctag_den.Write()

    h_lighttag_num_pass.Write()
    h_lighttag_num_fail.Write()
    h_lighttag_den.Write()
    outfile.Close()
    #outfile.Write()


    print "ROOT file written to", outfilename

    print "Completed."


if __name__ == "__main__":
    AnalyzeDataSet()
