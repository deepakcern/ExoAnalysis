from itertools import izip_longest
from glob import glob
import os

cwd = os.getcwd()

'''
    For the given path, get the List of all files in the directory tree
'''

def listMaker(path):

    dirName = str(path)#'/eos/cms/store/group/phys_exotica/bbMET/monoH_2016SkimmedTrees_withReg/Filelist_2016_MC/';

    print ("*******=====done====*********")

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    fileout='Output_merged_Filelists.txt'
    Fout=open(fileout,'w')
    # Print the files
    for elem in listOfFiles:
        #print(elem)
        Fout.write(elem+'\n')


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def mergeFiles(path,outputdir,N):
    outPutDir=str(outputdir)
    os.system('rm -rf '+outPutDir)
    os.system('mkdir '+outPutDir)
#    path='/afs/cern.ch/work/d/dekumar/public/monoH/Filelists/NewSkimmed/test/Files'

    txtFiles = glob(path+'/*txt')

    if N < 20:
        print ('lower value is N=20, script setting N=20 now')
	n = 20
    elif N >= 900:
	print ('Please N < 900 . Script setting N = 900')
        n = 900 
    else: n = N

    dirName='splitted_TxtFiles'
    os.system('rm -rf '+dirName)
    os.system('mkdir '+dirName)

    for ifile in txtFiles:
        outstr=ifile.split('/')[-1].replace('.txt','')
     #   print ('outstr',outstr)

        with open(ifile) as f:
            for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
                with open(dirName+'/'+'splitted_'+outstr+'_{0}.txt'.format(i), 'w') as fout:
       	            fout.writelines(g)

    '''
    with open('copy_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_0000.txt') as f:
        for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
            with open(dirName+'/'+'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_{0}.txt'.format(i), 'w') as fout:
                fout.writelines(g)
    '''

    newPath = cwd+'/'+dirName

    #print ('newPath',newPath)
    splitFiles = glob(newPath+'/*.txt')
    #print ('splitFiles',splitFiles)

    for sfile in splitFiles:
    	strName=sfile.split('/')[-1].replace('.txt','.root').replace('splitted','Merged')
    #	print ('strName',strName)
    	os.system('hadd '+outPutDir+'/'+str(strName)+' '+'@'+sfile)

    outPath=cwd+'/'+outPutDir
    listMaker(outPath)


#path='/afs/cern.ch/work/d/dekumar/public/monoH/Filelists/NewSkimmed/test/Files'
#mergeFiles(path)
