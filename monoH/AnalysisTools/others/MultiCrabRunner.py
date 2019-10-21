from os import listdir, system
from os.path import isfile, join
import os,sys,optparse


'''
workname='DATA_20190814'

mypath="crab_"+workname+"/"
dirs = [f for f in listdir(mypath) if not isfile(join(mypath, f))]

njobs=len(dirs)

for ind in range(njobs):	
	print "\n==========================\nStatus of job "+str(ind+1)+" of "+str(njobs)+"\n==========================\n"
	system("crab status -d "+mypath+dirs[ind])
'''


def Jobstatus(dirname):
        mypath=dirname+'/'
	dirs = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
        njobs=len(dirs)
        for ind in range(njobs):
	    print "\n==========================\nStatus of job "+str(ind+1)+" of "+str(njobs)+"\n==========================\n"
            system("crab status -d "+mypath+dirs[ind])
            #os.system('mail -s '+' "Status of condorJobs" '+' dpv0011@gmail.com < SendEmail.txt')


def JobResubmit(dirname):
        mypath=dirname+'/'
	dirs = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
        njobs=len(dirs)
        for ind in range(njobs):
	    print "\n==========================\nResubmiting job "+str(ind+1)+" of "+str(njobs)+"\n==========================\n"
    	    system("crab resubmit -d "+mypath+dirs[ind])
	

def JobKill(dirname):
        mypath=dirname+'/'
	dirs = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
	njobs=len(dirs)
	for ind in range(njobs):
		print "\n==========================\nChecking job "+str(ind+1)+" of "+str(njobs)+"\n==========================\n"
		system("crab kill -d "+mypath+dirs[ind])

isSendStatus=True
def ResubmitFailedJob(dirname):
        mypath=dirname+'/'
	dirs = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
	njobs=len(dirs)
        totalFailedJobs=0
        TotalCrabJobs=0
        AllrunJobs=0
	for ind in range(njobs):
	    system("crab status -d "+mypath+dirs[ind]  +'> jobstatus.txt') 	
            f=open('jobstatus.txt','r')
            lines= [line for line in f.readlines() if 'failed' in line and not 'job' in line]
	    f=open('jobstatus.txt','r')
            runLines=[line for line in f.readlines() if 'running' in line and not 'job' in line]
            if len(runLines) >0:
		line=runLines[0]
                print "runLines", runLines

                runJobs=int(line.split()[-1].split('/')[0].replace('(',''))
                AllrunJobs+=runJobs
            #print "runJobs", runJobs
            if len(lines)>0:
		line=lines[0]
            	totalJobs=int(line.split()[-1].split('/')[-1].replace(')',''))
            	failedJobs= int(line.split()[-1].split('/')[0].replace('(',''))
            	totalFailedJobs+= failedJobs
                TotalCrabJobs+=totalJobs
            	if failedJobs>0:
			system("crab resubmit -d "+mypath+dirs[ind])
	    	#else:
		#	continue
	    f.close()

	if totalFailedJobs>0:
		fout=open('SendEmail.txt','w')
		fout.write("=====Status of crab jobs======"+'\n')	
		fout.write("TotalJobs: "+str(TotalCrabJobs)+'\n')
		fout.write("resubmitted Failed:      "+str(totalFailedJobs)+'\n')
                fout.write("RunningJobs: "+str(AllrunJobs)+'\n')
                fout.close()             
                if isSendStatus:
		    os.system('mail -s '+' "Status of condorJobs" '+' dpv0011@gmail.com < SendEmail.txt')

	if totalFailedJobs==0 and AllrunJobs==0:
		fout1=open('StopResubmit.txt','w')
		fout1.close()
                if isSendStatus:
                    os.system('mail -s '+' "Finished crabJobs" '+' dpv0011@gmail.com < StopResubmit.txt')


usage = "usage: python MultiCrabRunner.py status/resubmit/kill/mail/ --outDir name of directory"

parser = optparse.OptionParser(usage)
parser.add_option("--outDir", "--outputDirectory",  dest="outputDirectory")
(options, args) = parser.parse_args()

outputdir = options.outputDirectory

if not outputdir:
	print (usage)
	sys.exit()
'''
if not sys.argv[1]=="mail":
	f=open("StopResubmit.txt","w")
        f.close()
'''
if sys.argv[1]=="status":
    Jobstatus(outputdir)
elif sys.argv[1]=="resubmit":
    JobResubmit(outputdir)
elif sys.argv[1]=="kill":
    JobKill(outputdir)

elif sys.argv[1]=="mail":
    ResubmitFailedJob(outputdir)

else:
    print (usage)
    sys.exit()
