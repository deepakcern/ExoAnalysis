import ROOT
from ROOT import TFile, TTree, TChain, gPad, gDirectory, TH1F
from multiprocessing import Process
import multiprocessing
from optparse import OptionParser
from operator import add
import math
import sys
import time
import array
import numpy, ray

f='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0002/SkimmedTree_100.root'
f2='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1001.root'
f3='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1002.root'
f4='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1003.root'
f5='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1004.root'
f6='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1005.root'
f7='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1006.root'
f8='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1007.root'
f9='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1008.root'
f10='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v2/Filelist_2016_bkg/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000/SkimmedTree_1033.root'
#files=[f, f2,f3,f4,f5,f6,f7,f8,f9,f,f,f10]
files=[]
#fin=open('output_test.txt','r')
#for line in fin:
#    files.append(line.rstrip())
files=[f,f2]
def run(file):
    h_met=TH1F('h_met','h_met',100,0,1000)
#    print 'file', file
    outfilename='Output_'+file.split('/')[-2]+'_'+file.split('/')[-1].split('_')[-1].split('.')[0]+'.root'
    outfile = TFile(outfilename,'RECREATE')
   
    print "outfile",outfilename
    tf =  ROOT.TFile(file)
    tt = tf.Get("outTree")
    print 'Total entries', tt.GetEntries()
    nent = int(tt.GetEntries())
    for i in range(int(tt.GetEntries())):
        tt.GetEntry(int(i))
#        if(i % (1 * nent/100) == 0):
#            sys.stdout.write("\r[" + "="*int(20*i/nent) + " " + str(round(100.*i/nent,0)) + "% done")
#            sys.stdout.flush()

	pfmet = tt.st_pfMetCorrPt
        jmsd_8 = tt.st_AK8SDmass

        nMu  = tt.st_nMu
        muP4  =tt.st_muP4
        isTightMuon =tt.st_isTightMuon
        muChHadIso  =tt.st_muChHadIso
        muNeHadIso  =tt.st_muNeHadIso
        muGamIso    =tt.st_muGamIso
        muPUPt     =tt.st_muPUPt

        h_met.Fill(pfmet)
#    outfile.cd()
#    h_met.Write()
#    outfile.Close()
        #print (len(jmsd_8))

start = time.time()


funtion_coll=[ray.put(run(f)) for f in range(files)]
ray.get(funtion_coll)

#run(6)
'''
if __name__ == '__main__':
    try:
        pool = multiprocessing.Pool()
        pool.map(run,files)
        pool.close()
    except Exception as e:
            print e
            pass
'''
end = time.time()
print ('\n')
print(end - start)
