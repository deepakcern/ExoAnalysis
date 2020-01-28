import os
from ROOT import TFile,TChain
from glob import glob

path='/eos/cms/store/group/phys_exotica/bbMET/2017_skimmedFiles/V0/MC_USCM_25Sep'

files=glob(path+'/*.txt')

deadfile=open('deadNtuplesFiles.txt','w')

for infile in files:
    for line in infile:
        try:
        Tree = TChain("tree/treeMaker")
        Tree.Add(line)
        NEntries = Tree.GetEntries()
        if NEntries==0 or NEntries<0:
            print 'File detected with zero entries'
	    deadfile.write(infile+'\n')
        except Exception as e:
	    print e
            print "Corrupt file detected"
            deadfile.write(infile+'\n')
            continue

