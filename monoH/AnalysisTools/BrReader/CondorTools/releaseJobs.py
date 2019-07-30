import os, sys
import glob

path='.'

os.system('condor_q dekumar > mycondorJobs.txt')
file='mycondorJobs.txt'

with open(file) as f:
    data = f.readlines()
lastline = data[-1]

print "===============status of jobs==========="+'\n'
print lastline
IDs=[]


with open(file) as f:
    lines = filter(None, (line.rstrip() for line in f))
    for line in lines:
        #print line
        if line.split()[5]=='H':
            #IDs.append((line.split()[0].strip('.0')))
            IDs.append((line.split()[0].replace('.0','')))

print "Total no of jobs which are in held  :   ",len(IDs), "and IDs",IDs

dirs=[ i for i in os.listdir(path) if 'tempFilelists' in i]
fnlDir=sorted(dirs)[-1]

#for str in ['Yrs','mnth','date','Hrs','Min','Sec']:
#    exec(str+"=[]")
    #exec("print "+str )

# mystr=[Yrs,mnth,date,Hrs,Min,Sec]
'''for dir in dirs:
    templine=dir.split('-')
    # print (templine[0].split('_')[-1])
    Yrs.append(templine[0].split('_')[-1])
    mnth.append(templine[1])
    date.append(templine[2])
    Hrs.append(templine[3])
    Min.append(templine[4])
    Sec.append(templine[5])'''
#mystr=[Yrs,mnth,date,Hrs,Min,Sec]
#print "tesmdir",mystr

#
# for i in ['Y','MNT','D','H','M','S']:
#Y=max(Yrs)
#MNT=max(mnth)
#D=max(date)
#H=max(Hrs)
#M=max(Min)
#S=max(Sec)

#print "Y",Y, MNT, D,H,M,S
#fnlDir='tempFilelists_'+Y+'-'+MNT+'-'+D+'-'+H+'-'+M+'-'+S

os.system('mkdir '+fnlDir+'/oldfiles')
# print "This is latest dir ", fnlDir
oldfile=fnlDir+'/oldfiles'

def getErrorFile(id):
    file='error/condor'+'.'+id+'.'+'0'+'.'+'err'
    f = open(file,'read')
    found=False
    for line in f:
        if 'TBranchElement::GetBasket' in line and 'root://se01.indiacms.res.in' in line:
            curruptFile=[f for f in line.split() if 'root://se01.indiacms.res.in' in f ]
            dataset=curruptFile[0].split('/')[-2]
            fl=curruptFile[0].split('/')[-1]
            found=True
            return dataset, fl
    if not found:
        print "This JobID: ",id,"  has different error please check inside error dir"
        return 0,0


def replacefile(fnlDir,dataset,skimfile):
    skimfiles=[ f for f in os.listdir(fnlDir) if dataset in f]
    isFile=False
    gottxt=''
    for skim in skimfiles:
        sfl=open(fnlDir+'/'+skim,'read')
        for line in sfl:
            if skimfile in line:
                gottxt=skim
                isFile=True
                print "This txt file has corrupted file",gottxt
    if not isFile: print "script could not find the proper file corresponding this id"
    if isFile:
        temptxt=open('tempfile.txt','w')
        realfile=open(fnlDir+'/'+gottxt,'read')
        for line in realfile:
            if skimfile not in line:
                #print "We are writing this line",line
                temptxt.write(line)
            else: print "We are skipping this line",line
        temptxt.close()
        temf='tempfile.txt'
        os.system('mv'+' '+fnlDir+'/'+gottxt+' '+oldfile+'/OldFile_'+gottxt)
        os.system('mv'+' '+temf+' '+fnlDir+'/'+gottxt)




count=0
notrel=[]
for jobid in IDs:
    print "++++++++++++++++++++++++++++++++++"+'\n'
    print "releasing this ID",jobid +"\n"
    print "\n"
    print "Latest temp dir:  ",fnlDir
    dataset, fl = getErrorFile(jobid)
    print "dataset and file name:  ",dataset, fl
    if dataset and fl:
        replacefile(fnlDir,dataset,fl)
        os.system('condor_release'+' '+jobid+'.'+'0')
        print 'condor_release'+' '+jobid+'.'+'0'
        print "\n"
        print "Released this job iD: ", jobid
        count +=1
    else:notrel.append(jobid)

print "===================================="+'\n'
print "Total no of released jobs",count
print "Jobs which are not released :", notrel
