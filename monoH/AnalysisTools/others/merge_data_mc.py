import os,sys
from mergeFiles import mergeFiles 
import sys, optparse

#errmsg="Usage:\n$ python ListMaker.py crab T2path outfileprefix\nor\n$ python ListMaker.py st T2path outfileprefix"
# it needs N argument
usage = "usage: python merge_data_mc.py st/crab -i inputpath -o outputDir -N number_of_files_to_merge"

#example: python merge_data_mc.py st -i /eos/cms/store/group/phys_exotica/bbMET/2016_skimmer/tDM_06052019 -o merged_Files -N 30
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--inputpath",  dest="inputpath")
parser.add_option("-o", "--outputdir", dest="outputdir")
parser.add_option("-N", "--nFsplit", dest="nFsplit")

(options, args) = parser.parse_args()

inputpath = options.inputpath
outputdir = options.outputdir

n = options.nFsplit 

#filepref = outputdir  

if not options.inputpath or not options.outputdir or not options.nFsplit:
    print (usage)
    sys.exit()

if sys.argv[1]=="crab":
    isCrab=True
elif sys.argv[1]=="st":
    isCrab=False

else:
    print (usage)
    sys.exit()

'''
if len(sys.argv)==4:
    if sys.argv[1]=="crab":
        isCrab=True
    elif sys.argv[1]=="st":
        isCrab=False
    else:
        print errmsg
        sys.exit()
    T2path=sys.argv[2]
    filepref=sys.argv[3]
else:
    print errmsg
    sys.exit()
'''

filepref = 'beforeMerge'

inpfilename='List_'+filepref+'.txt'
os.system('ls -R '+inputpath+' | cat &> ' +inpfilename)

f=open(inpfilename,"r")


os.system("mkdir -p TxtFiles"+"_"+filepref)
#pref="root://eoscms.cern.ch/"
pref=""
filecount=1
lineminus1=""
lineminus2=""
fileopen=False
failedfile=False
#log=open("log_"+filepref+".txt","w")

for line in f:
    if not line=="\n":
        fname=line.split()[-1]
    else:
        fname=""

    if fname.endswith(".root") and not fileopen:
       # print "checking lineminu2", lineminus2[:-2]
        folder=pref+lineminus2[:-2]+"/"
        if 'failed' in lineminus2 or lineminus2.split("/")[-1].strip()=="failed:" or lineminus2.split("/")[-1].strip()=="log:": failedfile=True

        if not failedfile:
            if isCrab:
                realname=lineminus2.split("/")[-3]+"_"+lineminus2.split("/")[-1][:-2]
            else:
                realname=lineminus2.split("/")[-1][:-2]
            out=open("TxtFiles"+"_"+filepref+"/"+realname+".txt","w")
            out.write(folder+fname+"\n")
            filecount+=1
        fileopen=True
    elif fname.endswith(".root"):
        if not failedfile: out.write(folder+fname+"\n")
    elif fileopen:
        if not failedfile: out.close()
        fileopen=False
        failedfile=False

    #print ('end_lineminus2',lineminus2)
    if lineminus1=="\n":
        lineminus2=line
    else:
        lineminus2 = lineminus1
    lineminus1=line
    #print ('end_line', line)

#log.close()
f.close()
os.system('rm -rf '+inpfilename)
#print ("Created Filelist_%s directory and log_%s.txt." %(filepref,filepref))
cwd = os.getcwd()

outPutTxt = cwd+'/'+"TxtFiles"+"_"+filepref
#print (outPutTxt)

mergeFiles(outPutTxt,str(outputdir),int(n))
