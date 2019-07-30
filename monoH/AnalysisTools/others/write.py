import os

f=open('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000.txt','r')

fout=open('output_test.txt','w')
for line in f:
    nl=(line.rstrip()).replace('root://eoscms.cern.ch/','')
    fout.write(nl+'\n')
