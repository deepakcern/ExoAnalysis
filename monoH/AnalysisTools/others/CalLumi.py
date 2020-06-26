import os, sys, math
out_fold = 'lumiInput_MET'#'lumiInput_resubmit'
os.system('mkdir '+out_fold)
crab_fold=sys.argv[1]
listfolders = [f for f in os.listdir(crab_fold)]
print 'listfolders', listfolders
'''
for fold1 in listfolders:
     os.system("brilcalc lumi -b \"STABLE BEAMS\" --byls --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i "+crab_fold+"/"+fold1+"/results/processedLumis.json > "+out_fold+"/"+fold1+".txt")
     print("Integrated luminosity calculated for  "+fold1+"\n")
'''

Lumi=[]

CalMET=True
for fold1 in listfolders:
        if not "MET" in fold1:continue
	f = open(out_fold+"/"+fold1+".txt",'r')
        lines = f.readlines()
        lumi= lines[-5].split('|')[-2]
        Lumi.append(float(lumi))
        print "luminosity for ",fold1, "   ", ": ", lumi
print "Lumi",sum(Lumi)

