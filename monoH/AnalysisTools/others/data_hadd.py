import os
import glob

path='/afs/cern.ch/work/d/dekumar/public/monoH/ST_BR_test_2016/CMSSW_8_0_26_patch1/src/MonoH/bbDM/bbDM/bbMET/MP_BROutputs_data/'

dlist=['Output_MET-Run', 'Output_SingleElectron-Run']

outdir='MP_haddout_data'
os.system('rm -rf  '+outdir)
os.system('mkdir  '+outdir)
os.system('hadd '+outdir+'/'+'data_combined_MET.root'+' '+path+str(dlist[0])+'*')
os.system('hadd '+outdir+'/'+'data_combined_SE.root'+' '+path+str(dlist[1])+'*')
