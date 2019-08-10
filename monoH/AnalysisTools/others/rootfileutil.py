import os,sys
from glob import glob

def getSampleDic(path,step='st'):
	if step=='st':isCrab=False
	if step=='crab':isCrab=True
	filepref='rootFiles'
	inpfilename='List_'+filepref+'.txt'
	os.system('ls -R '+path+' | cat &> ' +inpfilename)

	f=open(inpfilename,"r")

	os.system("mkdir -p Filelist"+"_"+filepref)
	#pref="root://eoscms.cern.ch/"
	pref=""
	filecount=1
	lineminus1=""
	lineminus2=""
	fileopen=False
	failedfile=False

	for line in f:
		if not line=="\n":
			fname=line.split()[-1]
		else:
			fname=""
		if fname.endswith(".root") and not fileopen:
			folder=pref+lineminus2[:-2]+"/"
			if 'failed' in lineminus2 or lineminus2.split("/")[-1].strip()=="failed:" or lineminus2.split("/")[-1].strip()=="log:": failedfile=True
			if not failedfile:
				if isCrab:
					realname=lineminus2.split("/")[-3]+"_"+lineminus2.split("/")[-1][:-2]
				else:
					realname=lineminus2.split("/")[-1][:-2]
				out=open("Filelist"+"_"+filepref+"/"+realname+".txt","w")
				out.write(folder+fname+"\n")
				filecount+=1
			fileopen=True
		elif fname.endswith(".root"):
			if not failedfile: out.write(folder+fname+"\n")
		elif fileopen:
			if not failedfile: out.close()
			fileopen=False
			failedfile=False
		if lineminus1=="\n":
			lineminus2=line
		else:
			lineminus2 = lineminus1
		lineminus1=line

	f.close()

	newPath="Filelist"+"_"+filepref
	sampleDic={}
	files = glob(newPath+'/*.txt')
	os.system('mkdir tempDir')
	for ifile in files:
		fname=ifile.split('/')[-1][:-9]
		pointFile=newPath+'/'+fname
		os.system('cat '+pointFile+'*'+' '+'>'+'tempDir/'+fname+'.txt')
		
	newFiles=glob('tempDir/*.txt')
	for ifile in newFiles:
		key=ifile.split('/')[-1].replace('.txt','')
		fin=open(ifile,'r')
		rootFiles = filter(None, (line.rstrip() for line in fin))
		sampleDic[key]=[rf for rf in rootFiles]
		
        os.system('rm -rf tempDir')
        os.system('rm -rf '+newPath)
        
	return sampleDic



#path='/eos/cms/store/group/phys_exotica/bbMET/2016_Skimmed_withReg_v4_looseEle/Filelist_2016_bkg'

#dic=getSampleDic(path)
#print (dic)
