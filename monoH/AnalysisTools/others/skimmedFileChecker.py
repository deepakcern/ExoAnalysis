import os
from ROOT import TFile
from glob import glob

path='/eos/cms/store/group/phys_exotica/bbMET/2017_skimmedFiles/V0/MC_USCM_25Sep'

files=glob(path+'/*.root')

deadfile=open('deadSkimmedFiles.txt','w')

for infile in files:
    f=TFile.Open(infile,'READ')
    h_total = f.Get('h_total_mcweight')
    try:
	TotalEvents = h_total.Integral()
    except Exception as e:
	print e
        print "Corrupt file detected"
        deadfile.write(infile+'\n')
        continue

