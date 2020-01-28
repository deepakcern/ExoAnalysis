import os
from ROOT import TFile,TChain
from glob import glob

path='/home/deepakk/NewSkimmer/V1/ExoPieSlimmer/CondorJobs/FailedFiles_mc'

files=glob(path+'/*.txt')

deadfile=open('deadNtuplesFiles.txt','w')

#print 'Files', files
for infile in files:
    f = open(infile,'r')
    for line in f:
        #print 'fileName', line
        try:
            Tree = TChain("tree/treeMaker")
            Tree.Add(line.rstrip())
            NEntries = Tree.GetEntries()
            if NEntries==0 or NEntries<0:
                print 'File detected with zero entries'
	        deadfile.write(infile+'\n')
        except Exception as e:
	    print e
            print "Corrupt file detected"
            deadfile.write(infile+'\n')
            continue

