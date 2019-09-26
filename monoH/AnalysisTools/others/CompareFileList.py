import os
from glob import glob

def runFile(txtfile1,txtfile2,dirName):
    a=[];b=[]
    for line in open(txtfile1):
	a.append(line)
    for line in open(txtfile2):
	b.append(line)

    aminusb=set(a)-set(b)
    bminusa=set(b)-set(a)
    sameevent=set(a)&set(b)
    aminussame=set(a)-(set(a)&set(b))

    txtFilename=txtfile1.split('/')[-1]
    fout=open(dirName+'/'+str(txtFilename),'w')
    #fout.write("\n".join(aminussame))
    fout.write("".join(aminussame))


commanFile='deadfiles.txt'

path='/home/deepakk/NewSkimmer/V0/ExoPieSlimmer/CondorJobs_v2/FailedJobs_files/'

files=glob(path+'/*txt')

dirName='NewFiles'
os.system('rm -rf '+dirName)
os.system('mkdir '+dirName)

for infile in files:
    runFile(infile,commanFile,dirName)
