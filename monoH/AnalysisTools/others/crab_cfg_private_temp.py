from CRABClient.UserUtilities import config
config = config()


workname='2017__20191015'
reqname='EXO-ggToXdXdHToBB_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_150_MH2_600_MHC_600_CP3Tune_13TeV_new'
dataset='/CRAB_PrivateMC/dekumar-EXO-ggToXdXdHToBB_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_150_MH2_600_MHC_600_CP3Tune_13TeV-a0e997d2f8238b61982782e35278a72a/USER'

config.section_("General")
config.General.transferLogs = True

config.General.requestName = reqname
config.General.workArea = 'privateSamples'


config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'treeMaker_Summer17_cfg.py'
config.JobType.maxMemoryMB = 10000


config.JobType.inputFiles = ['../../MetaData/data/DNN_models/breg_training_2017.pb',
'../../TreeMaker/data/BoostedSVDoubleCA15_withSubjet_v4.weights.xml',
]
config.JobType.sendExternalFolder = True
config.JobType.sendPythonFolder = True
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.splitting       = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = reqname
config.Data.inputDBS = 'phys03'
config.Data.outLFNDirBase = '/store/group/phys_exotica/bbMET/ExoPieElementTuples_20190821/signal_sample' 
config.Data.publication = False
config.Data.inputDataset = dataset


config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
