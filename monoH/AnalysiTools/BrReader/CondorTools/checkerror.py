import os
import glob

path='/home/dekumar/deepak/MonoH/bbDM/bbMET/BR_Condor_Farmout/output/*.out'

files=sorted(glob.glob(path))

counts=[]

#for file in files:
    #f=open(file,'r')
    #if (f.readlines())[-1]==None:
            #print (f.readlines())
    #last_line=f.readlines()[-1]
    #if not str(last_line.split()[0])=='Completed.':
            #print "======Please check this cluster Id(Not finished) in error directory"
            #print file.split('/')[-1]
            #counts.append(1)

#print "Total errors:  ", len(counts)

for file in files:
    with open(file) as f:
        lines = filter(None, (line.rstrip() for line in f))
        if lines:
            last_line=lines[-1]#.readlines()[-1]
            if not str(last_line.split()[0])=='Completed.':
                print "======Please check this cluster Id file.This file has some error====="
                print file.split('/')[-1]
                counts.append(1)

print "Total errors:  ", len(counts)
