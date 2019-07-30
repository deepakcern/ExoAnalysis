import os
import glob

path='/afs/cern.ch/work/d/dekumar/public/monoH/ST_BR_test_2016/CMSSW_8_0_26_patch1/src/MonoH/bbDM/bbDM/bbMET/MP_BROutputs_bkg'


slist=['Output_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root',
'Output_WW_TuneCUETP8M1_13TeV-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WZ_TuneCUETP8M1_13TeV-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_ZZ_TuneCUETP8M1_13TeV-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-100To200_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-200To400_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-400To600_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-600To800_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-800To1200_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_MC25ns_LegacyMC_2017.root',
'Output_ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_MC25ns_LegacyMC_.root',
'Output_ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_MC25ns_LegacyMC_20170328.root',
'Output_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_MC25ns_LegacyMC_20170328.root',
'Output_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_MC25ns_LegacyMC_20170328.root',
'Output_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MC25ns_LegacyMC_20170328.root',
'Output_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
'Output_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
'Output_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
'Output_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
'Output_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
'Output_ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8.root',
'Output_ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8.root',
'Output_WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8.root',
'Output_WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8.root',
'Output_ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8.root',
'Output_ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8.root']

outDir='MP_haddOutput'
os.system('mkdir '+outDir)


logo=''' \n
====================**********************==================
===================************************=================
=================****************************===============\n

'''


for ifile in slist:
        myfiles=path+'/'+ifile.replace('.root','*') 
        print logo
        print 'doing hadd for file:  ', myfiles
        print logo
        #fls=glob.glob(myfiles)
        #print fls
	os.system('hadd '+outDir+'/'+ifile+' '+myfiles)
#        break



dpath='/afs/cern.ch/work/d/dekumar/public/monoH/ST_BR_test_2016/CMSSW_8_0_26_patch1/src/MonoH/bbDM/bbDM/bbMET/MP_BROutputs_data/'

dlist=['Output_MET-Run', 'Output_SingleElectron-Run']

#outdir='MP_haddout_data'
#os.system('rm -rf  '+outdir)
os.system('mkdir  '+outDir)
os.system('hadd '+outDir+'/'+'data_combined_MET.root'+' '+dpath+str(dlist[0])+'*')
os.system('hadd '+outDir+'/'+'data_combined_SE.root'+' '+dpath+str(dlist[1])+'*')
