import os
import sys
import datetime
import sys, optparse
## Ratio is added Data/MC
## Template macro is fed to a python variable
## 1.)  is created on DateBase
## 2.) Starting Extension of your Dir..Like
## in a day you want 2 directories jsut
## change the DirPreName
## Monika Mittal Khuarana
## Raman Khurana


#if len(sys.argv) < 2 :
#    print "insufficiency inputs provided, please provide the directory with input files"
##just for argument, the input file path is explicitly provided in line no 101
#if len(sys.argv) ==2 :
#    print "plotting from directory ",sys.argv[1]
#    inputdirname = sys.argv[1]

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

parser.add_option("-d", "--data", dest="datasetname")
parser.add_option("-s", "--sr", action="store_true", dest="plotSRs")
parser.add_option("-m", "--mu", action="store_true", dest="plotMuRegs")
parser.add_option("-e", "--ele", action="store_true", dest="plotEleRegs")
parser.add_option("-p", "--pho", action="store_true", dest="plotPhoRegs")
parser.add_option("-q", "--qcd", action="store_true", dest="plotQCDRegs")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")

(options, args) = parser.parse_args()

if options.plotSRs==None:
    makeSRplots = False
else:
    makeSRplots = options.plotSRs

if options.plotMuRegs==None:
    makeMuCRplots = False
else:
    makeMuCRplots = options.plotMuRegs

if options.plotEleRegs==None:
    makeEleCRplots = False
else:
    makeEleCRplots = options.plotEleRegs

if options.plotPhoRegs==None:
    makePhoCRplots = False
else:
    makePhoCRplots = options.plotPhoRegs

if options.plotQCDRegs==None:
    makeQCDCRplots = False
else:
    makeQCDCRplots = options.plotQCDRegs

if options.verbose==None:
    verbose = False
else:
    verbose = options.verbose

if options.datasetname.upper()=="SE":
    dtset="SE"
elif options.datasetname.upper()=="SP":
    dtset="SP"
elif options.datasetname.upper()=="SM":
    dtset="SM"
else:
    dtset="MET"

print "Using dataset "+dtset

datestr = datetime.date.today().strftime("%d%m%Y")

#temp_macro=open('myMacro.C','r')

'''
TemplateOverlapMacro = open('TemplateOverlapMacro.C','w')
TemplateOverlapMacro.write(temp_macro)
TemplateOverlapMacro.close()
'''

#TemplateOverlapMacro = open('myMacro.C','r')

def makeplot(inputs):
    print inputs

    QCDSF=1
    if not 'QCD' in inputs[1]:
        if '1b' in inputs[1] or 'sr1' in inputs[1].lower():
            QCDSF=1.2508
        elif '2b' in inputs[1] or 'sr2' in inputs[1].lower():
            QCDSF=0.9458
    print QCDSF
    TemplateOverlapMacro = open('MY_TemplateOverlapMacro.C','r')
    NewPlot       = open('Plot.C','w')
    for line in TemplateOverlapMacro:
#        line = line.replace("DATE_STR",str(datestr))
        line = line.replace("MYDATASET",str(dtset))
        line = line.replace("HISTPATH",inputs[0])
        line = line.replace("HISTNAME",inputs[1])
        line = line.replace("XAXISLABEL",inputs[2])
        line = line.replace("XMIN",inputs[3])
        line = line.replace("XMAX",inputs[4])
        line = line.replace("REBIN",inputs[5])
        line = line.replace("ISLOG",inputs[6])

        line = line.replace("QCDSF",str(QCDSF))
        line = line.replace("VERBOSE",str(int(verbose)))

        HistName=inputs[1]
        #if 'h_reg_' in HistName:
        #    histolabel=HistName.split('_')[2]
        if '_sr1' in HistName:
            histolabel="SR1"
        elif '_sr2' in HistName:
            histolabel="#splitline{monoHbb}{Boosted}"
        elif '2mu2b' in HistName:
            histolabel="Dimuon CR"
        elif '2e2b' in HistName:
            histolabel="Dielectron CR"
        elif '1mu2bW' in HistName:
            histolabel="W CR (#mu)"
        elif '1e2bW' in HistName:
            histolabel="W CR (e)"
        elif '1mu2bT' in HistName:
            histolabel="t#bar{t} CR (#mu)"
        elif '1e2bT' in HistName:
            histolabel="t#bar{t} CR (e)"
        elif '1mu1e2b' in HistName:
            histolabel="t#bar{t} CR (e+#mu)"
        else:
            histolabel=""

        line = line.replace("HISTOLABEL",histolabel)


        if len(inputs) > 7 :
            line = line.replace("ISCUTFLOW", inputs[7])
        else :
            line = line.replace("ISCUTFLOW", "0")

        if len(inputs) > 8 :
            line = line.replace("BLINDFACTOR", inputs[8])
        else :
            line = line.replace("BLINDFACTOR", "1")


        if len(inputs) > 9 :
            line = line.replace("NORATIOPLOT", inputs[9])
        else :
            line = line.replace("NORATIOPLOT", "0")
        if len(inputs) >10 :
            line = line.replace("VARIABLEBINS", inputs[10])
        else:
            line = line.replace("VARIABLEBINS", "0")
        if len(inputs) > 11 :
            line = line.replace("TEXTINFILE", inputs[11])
        else :
            line = line.replace("TEXTINFILE", "0")
        if len(inputs) > 12 :
            line = line.replace(".pdf",str(inputs[12]+".pdf"))
            line = line.replace(".png",str(inputs[12]+".png"))
        if len(inputs) > 13:
            line = line.replace("PREFITDIR",inputs[13]) ## PreFitMET or PreFitMass
            line = line.replace("DRAWPREFIT","1") ## 0 or 1
        else:
            line = line.replace("DRAWPREFIT","0")
        #print line
        NewPlot.write(line)
    NewPlot.close()
    os.system('root -l -b -q  Plot.C')
    print

##########Start Adding your plots here


dirnames=['']

emplist=open("Empty.txt","w")
emplist.close()

srblindfactor='1'
srnodata='1'

for dirname in dirnames:

    regions=[]
    PUreg=[]

#    if makeMuCRplots and makeEleCRplots:
#        regions=['2e1b','2mu1b','2e2b','2mu2b','1e1b','1mu1b','1e2b','1mu2b','1mu1e1b','1mu1e2b']
    if makeMuCRplots:
        regions+=['2mu2b','1mu2bT','1mu2bW']#,'1mu2bW_noMassCut','1mu2bW_nobtag','1mu2bW_noMassAndbtag']
        PUreg+=['mu_']
    if makeEleCRplots:
        regions+=['2e2b','1e2bT','1e2bW']#,'1e2bW_noMassCut','1e2bW_nobtag','1e2bW_noMassAndbtag']
        PUreg+=['ele_']
    if makePhoCRplots:
        regions+=['1gamma2b']
        PUreg+=['pho_']
    if makeQCDCRplots:
        regions+=['QCD2b']
        PUreg+=[]
#    else:
#        regions=[]
#        PUreg=[]

#    makeplot([dirname+"CRSum",'h_CRSum_','','0.','10.','1','1'])
#    if makeMuCRplots: makeplot([dirname+"CRSumMu",'h_CRSumMu_','','0.','6.','1','1'])
#    if makeEleCRplots: makeplot([dirname+"CRSumEle",'h_CRSumEle_','','0.','4.','1','1'])

    for dt in PUreg:
        makeplot([dirname+dt+"PuReweightPV",'h_'+dt+'PuReweightPV_','nPV after PU reweighting','0.','50.','1','0'])
        makeplot([dirname+dt+"noPuReweightPV",'h_'+dt+'noPuReweightPV_','nPV before PU reweighting','0.','50.','1','0'])
#        makeplot([dirname+dt+"PuReweightnPVert",'h_'+dt+'PuReweightnPVert_','nPV after PU reweighting (nPVert): '+dt,'0.','100.','100','0'])
#        makeplot([dirname+dt+"noPuReweightnPVert",'h_'+dt+'noPuReweightnPVert_','nPV before PU reweighting (nPVert): '+dt,'0.','100.','100','0'])

# Cutflow plots:
    if makeSRplots:
        makeplot([dirname+"cutflow",'h_cutflow_','Cutflow','0.','10','1','1','1',srblindfactor,srnodata])
        #makeplot([dirname+"cutflow_SR1",'h_cutflow_SR1_','SR1 Cutflow','0.','10','1','1','1',srblindfactor,srnodata])
        #makeplot([dirname+"cutflow_SR2",'h_cutflow_SR2_','SR2 Cutflow','0.','10','1','1','1',srblindfactor,srnodata])

    for reg in regions:
        makeplot([dirname+"cutflow_"+reg,'h_cutflow_'+reg+'_',reg+' Cutflow','0.','13','1','1','1'])

#Linear plots:
    if makeSRplots:
        #makeplot([dirname+"bb_Mass_sr2",'h_bb_Mass_sr2_','M(bb)','0.','250.','3','0','0',srblindfactor,srnodata])
	#makeplot([dirname+"MT_sr2",'h_MT_sr2_','MT(h,MET)','0.','1000.','2','0','0',srblindfactor,srnodata])
        makeplot([dirname+"ca15jet_SD_sr2",'h_ca15jet_SD_sr2_','SDMass (GeV)','100.','150.','50','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet1_eta_sr1",'h_jet1_eta_sr1_','jet 1 #eta','-3.','3.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_eta_sr1",'h_jet2_eta_sr1_','jet 2 #eta','-3.','3.','1','0','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"jet1_eta_sr2",'h_jet1_eta_sr2_','jet 1 #eta','-3.','3.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_eta_sr2",'h_jet2_eta_sr2_','jet 2 #eta','-3.','3.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet3_eta_sr2",'h_jet3_eta_sr2_','jet 3 #eta','-3.','3.','1','0','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"jet1_csv_sr1",'h_jet1_csv_sr1_','jet 1 csv','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_csv_sr1",'h_jet2_csv_sr1_','jet 2 csv','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"jet1_deepcsv_sr1",'h_jet1_deepcsv_sr1_','jet 1 deepcsv','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_deepcsv_sr1",'h_jet2_deepcsv_sr1_','jet 2 deepcsv','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # #makeplot([dirname+"presel_jet1_csv_sr1",'h_presel_jet1_csv_sr1_','jet 1 csv before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        # #makeplot([dirname+"presel_jet2_csv_sr1",'h_presel_jet2_csv_sr1_','jet 2 csv before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"jet1_csv_sr2",'h_jet1_csv_sr2_','jet 1 csv','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_csv_sr2",'h_jet2_csv_sr2_','jet 2 csv','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet3_csv_sr2",'h_jet3_csv_sr2_','jet 3 csv','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"jet1_deepcsv_sr2",'h_jet1_deepcsv_sr2_','jet 1 deepcsv','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_deepcsv_sr2",'h_jet2_deepcsv_sr2_','jet 2 deepcsv','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet3_deepcsv_sr2",'h_jet3_deepcsv_sr2_','jet 3 deepcsv','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # #makeplot([dirname+"presel_jet1_csv_sr2",'h_presel_jet1_csv_sr2_','jet 1 csv before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        # #makeplot([dirname+"presel_jet2_csv_sr2",'h_presel_jet2_csv_sr2_','jet 2 csv before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        # #makeplot([dirname+"presel_jet3_csv_sr2",'h_presel_jet3_csv_sr2_','jet 3 csv before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # #makeplot([dirname+"presel_jet1_chf_sr1",'h_presel_jet1_chf_sr1_','jet 1 CHadFrac before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        # #makeplot([dirname+"presel_jet1_chf_sr2",'h_presel_jet1_chf_sr2_','jet 1 CHadFrac before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        # #makeplot([dirname+"presel_jet1_nhf_sr1",'h_presel_jet1_nhf_sr1_','jet 1 NHadFrac before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        # #makeplot([dirname+"presel_jet1_nhf_sr2",'h_presel_jet1_nhf_sr2_','jet 1 NHadFrac before selection','0.','1.','1','0','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"jet1_chf_sr1",'h_jet1_chf_sr1_','jet 1 CHadFrac','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet1_chf_sr2",'h_jet1_chf_sr2_','jet 1 CHadFrac','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet1_nhf_sr1",'h_jet1_nhf_sr1_','jet 1 NHadFrac','0.','1.','1','0','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet1_nhf_sr2",'h_jet1_nhf_sr2_','jet 1 NHadFrac','0.','1.','1','0','0',srblindfactor,srnodata])

    ##for CRs
    for reg in regions:
        if reg[0]=='2': makeplot([dirname+"reg_"+reg+"_Zmass",'h_reg_'+reg+'_Zmass_','Z candidate mass (GeV)','70.','110.','1','0'])
        #if reg[0]=='2': makeplot([dirname+"reg_"+reg+"_Zmass",'h_reg_'+reg+'_Zmass_','Z candidate mass (GeV)','70.','110.',reg[-2],'0'])
        if reg[0]=='1': makeplot([dirname+"reg_"+reg+"_Wmass",'h_reg_'+reg+'_Wmass_','W candidate m_{T} (GeV)','40.','170.','1','0'])
        #makeplot([dirname+"reg_"+reg+"_jet1_eta",'h_reg_'+reg+'_jet1_eta_','Lead Jet #eta','-3.5','3.5','1','0'])
        #makeplot([dirname+"reg_"+reg+"_jet2_eta",'h_reg_'+reg+'_jet2_eta_','Second Jet #eta','-3.5','3.5','1','0'])
#
#         makeplot([dirname+"reg_"+reg+"_jet1_deepcsv",'h_reg_'+reg+'_jet1_deepcsv_','Lead Jet deepCSV','0.','1.','1','0'])
#         makeplot([dirname+"reg_"+reg+"_jet1_csv",'h_reg_'+reg+'_jet1_csv_','Lead Jet CSV','0.','1.','1','0'])
# #        makeplot([dirname+"reg_"+reg+"_jet2_csv",'h_reg_'+reg+'_jet2_csv_','Second Jet CSV','0.','1.','1','0'])


#Log plots:

###For SR
    if makeSRplots:
        #makeplot([dirname+"jet1_pT_sr1",'h_jet1_pT_sr1_','jet 1 p_{T} (GeV)','0.','800.','1','1','0',srblindfactor,srnodata])
        #makeplot([dirname+"jet2_pT_sr1",'h_jet2_pT_sr1_','jet 2 p_{T} (GeV)','0.','400.','1','1','0',srblindfactor,srnodata])
        #
        #
        # makeplot([dirname+"jet1_pT_sr2",'h_jet1_pT_sr2_','jet 1 p_{T} (GeV)','0.','800.','1','1','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet2_pT_sr2",'h_jet2_pT_sr2_','jet 2 p_{T} (GeV)','0.','400.','1','1','0',srblindfactor,srnodata])
        # makeplot([dirname+"jet3_pT_sr2",'h_jet3_pT_sr2_','jet 3 p_{T} (GeV)','0.','400.','1','1','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"min_dPhi_sr1",'h_min_dPhi_sr1_','min #Delta #phi','0.','3.2','1','1','0',srblindfactor,srnodata])
        # makeplot([dirname+"min_dPhi_sr2",'h_min_dPhi_sr2_','min #Delta #phi','0.','3.2','1','1','0',srblindfactor,srnodata])
        #
        # makeplot([dirname+"met_sr1",'h_met_sr1_','Missing Transverse Energy (GeV)','200.','1000','1','1','0',srblindfactor,srnodata])
        makeplot([dirname+"met_sr2",'h_met_sr2_','Missing Transverse Energy (GeV)','200.','1000','1','1','0',srblindfactor,srnodata])

    # Region based
    for reg in regions:
	# if reg[0]=='2': makeplot([dirname+"reg_"+reg+"_ZpT",'h_reg_'+reg+'_ZpT_','Z candidate p_{T} (GeV)','0.','800.','1','1'])
    #     #if reg[0]=='2': makeplot([dirname+"reg_"+reg+"_ZpT",'h_reg_'+reg+'_ZpT_','Z candidate p_{T} (GeV)','0.','800.',reg[-2],'1'])
        
        if reg[0]=='1': makeplot([dirname+"reg_"+reg+"_WpT",'h_reg_'+reg+'_WpT_','W candidate p_{T} (GeV)','0.','800.','1','1'])
        '''
        makeplot([dirname+"reg_"+reg+"_hadrecoil",'h_reg_'+reg+'_hadrecoil_','Hadronic Recoil (GeV)','200.','1000.','1','1'])
        makeplot([dirname+"reg_"+reg+"_bb_Mass",'h_reg_'+reg+'_bb_Mass_','M(bb)','0.','250.','1','0'])
	makeplot([dirname+"reg_"+reg+"_MT",'h_reg_'+reg+'_MT_','MT(h,MET)','0.','250.','1','0'])

        makeplot([dirname+"reg_"+reg+"_ca15jet_pT",'h_reg_'+reg+'_ca15jet_pT_','FATJET pT (GeV)','200.','700.','1','1'])
        
        makeplot([dirname+"reg_"+reg+"_ca15jet_SD",'h_reg_'+reg+'_ca15jet_SD_','SDMass (GeV)','100.','150.','1','0'])
	makeplot([dirname+"reg_"+reg+"_ca15jet_eta",'h_reg_'+reg+'_ca15jet_eta_','FATJET #eta (GeV)','-2.4','2.4','1','0'])
        '''
        makeplot([dirname+"reg_"+reg+"_N2DDT",'h_reg_'+reg+'_N2DDT_','N2DDT','-0.2','0.25','1','0'])
        
       # makeplot([dirname+"reg_"+reg+"_N2",'h_reg_'+reg+'_N2_','N2','0.','0.5','1','0'])
       # makeplot([dirname+"reg_"+reg+"_lep1_pT",'h_reg_'+reg+'_lep1_pT_','Lead Lepton p_{T} (GeV)','0.','700.','1','1'])
#	makeplot([dirname+"reg_"+reg+"_lep1_eta",'h_reg_'+reg+'_lep1_eta_','Lead Lepton #eta (GeV)','-2.4','2.4','1','0'])
#        makeplot([dirname+"reg_"+reg+"_njet",'h_reg_'+reg+'_njet_','Number of Jets','-1','10','1','1'])
        
        '''
        if not 'QCD' in reg:
            makeplot([dirname+"reg_"+reg+"_MET",'h_reg_'+reg+'_MET_','Real MET (GeV)','0.','400.','2','1'])
        else:
            makeplot([dirname+"reg_"+reg+"_MET",'h_reg_'+reg+'_MET_','Real MET (GeV)','200.','800.','2','1'])
        makeplot([dirname+"reg_"+reg+"_njet",'h_reg_'+reg+'_njet_','Number of Jets','-1','10','1','1'])

        if reg[:2]=='1e':
            makeplot([dirname+"reg_"+reg+"_njet_n_minus_1",'h_reg_'+reg+'_njet_n_minus_1_','Number of Jets (n-1 cuts plot)','-1','12','1','1'])
            makeplot([dirname+"reg_"+reg+"_unclean_njet_n_minus_1",'h_reg_'+reg+'_unclean_njet_n_minus_1_','Number of Jets without cleaning (n-1 cuts plot)','-1','12','1','1'])

            makeplot([dirname+"reg_"+reg+"_min_dR_jet_ele_preclean",'h_reg_'+reg+'_min_dR_jet_ele_preclean_','min dR between jets and electron before jet cleaning','0.','6.','1','1'])
            makeplot([dirname+"reg_"+reg+"_min_dR_jet_ele_postclean",'h_reg_'+reg+'_min_dR_jet_ele_postclean_','min dR between jets and electron after jet cleaning','0.','6.','1','1'])
        makeplot([dirname+"reg_"+reg+"_min_dPhi_jet_Recoil",'h_reg_'+reg+'_min_dPhi_jet_Recoil_','min d #phi between jets and recoil','0.','6.','1','1'])
        makeplot([dirname+"reg_"+reg+"_min_dPhi_jet_MET",'h_reg_'+reg+'_min_dPhi_jet_MET_','min d #phi between jets and real MET','0.','6.','1','1'])

        makeplot([dirname+"reg_"+reg+"_min_dPhi_jet_Recoil_n_minus_1",'h_reg_'+reg+'_min_dPhi_jet_Recoil_n_minus_1_','min d #phi between jets and recoil before d#phi cut','0.','6.','1','1'])
	makeplot([dirname+"reg_"+reg+"_nca15jet",'h_reg_'+reg+'_nca15jet_','Number of CA15Jet','-1','4','1','1']) #nca15jet
        makeplot([dirname+"reg_"+reg+"_ntau",'h_reg_'+reg+'_ntau_','Number of Taus','-1','4','1','1'])
        makeplot([dirname+"reg_"+reg+"_nUncleanTau",'h_reg_'+reg+'_nUncleanTau_','Number of Taus (before cleaning)','-1','6','1','1'])
#            makeplot([dirname+"reg_"+reg+"_ntaucleaned",'h_reg_'+reg+'_ntaucleaned_','Number of Taus (after Tau cleaning)','-1','4','5','1'])
        makeplot([dirname+"reg_"+reg+"_nele",'h_reg_'+reg+'_nele_','Number of Electrons','-1','5','1','1'])
        if reg[0]=='2': makeplot([dirname+"reg_"+reg+"_npho",'h_reg_'+reg+'_npho_','Number of Photons','-1','5','1','1'])
#            makeplot([dirname+"reg_"+reg+"_nUncleanEle",'h_reg_'+reg+'_nUncleanEle_','Number of Eles (before cleaning)','-1','6','7','1'])
        makeplot([dirname+"reg_"+reg+"_nmu",'h_reg_'+reg+'_nmu_','Number of Muons','-1','5','1','1'])
#            makeplot([dirname+"reg_"+reg+"_nUncleanMu",'h_reg_'+reg+'_nUncleanMu_','Number of Muons (before cleaning)','-1','6','7','1'])
        makeplot([dirname+"reg_"+reg+"_lep1_pT",'h_reg_'+reg+'_lep1_pT_','Lead Lepton p_{T} (GeV)','0.','500.','1','1'])
        makeplot([dirname+"reg_"+reg+"_lep2_pT",'h_reg_'+reg+'_lep2_pT_','Second Lepton p_{T} (GeV)','0.','250.','1','1'])
        if reg.startswith('1mu1e'): makeplot([dirname+"reg_"+reg+"_e_pT",'h_reg_'+reg+'_e_pT_','Electron p_{T} (GeV)','0.','500.','1','1'])         #Top
        if reg.startswith('1mu1e'): makeplot([dirname+"reg_"+reg+"_mu_pT",'h_reg_'+reg+'_mu_pT_','Muon p_{T} (GeV)','0.','500.','1','1'])           #Top
        makeplot([dirname+"reg_"+reg+"_pho_pT",'h_reg_'+reg+'_pho_pT_','Photon p_{T} (GeV)','0.','500.','1','1'])
        if reg[1]=='m': makeplot([dirname+"reg_"+reg+"_lep1_iso",'h_reg_'+reg+'_lep1_iso_','Lead Lepton isolation','0.','800.','1','1'])
        if reg[1]=='m': makeplot([dirname+"reg_"+reg+"_lep2_iso",'h_reg_'+reg+'_lep2_iso_','Second Lepton isolation','0.','800.','1','1'])
        if reg.startswith('1mu1e'): makeplot([dirname+"reg_"+reg+"_mu_iso",'h_reg_'+reg+'_mu_iso_','Muon isolation','0.','800.','1','1'])            #Top
        makeplot([dirname+"reg_"+reg+"_jet1_pT",'h_reg_'+reg+'_jet1_pT_','Lead Jet p_{T} (GeV)','0.','800.','1','1'])
        makeplot([dirname+"reg_"+reg+"_jet2_pT",'h_reg_'+reg+'_jet2_pT_','Second Jet p_{T} (GeV)','0.','400.','1','1'])
#            makeplot([dirname+"reg_"+reg+"_lep1_dR_tau",'h_reg_'+reg+'_lep1_dR_tau_','dR b/w tau and lead lepton','0.','6.','120','1'])
#            makeplot([dirname+"reg_"+reg+"_lep2_dR_tau",'h_reg_'+reg+'_lep2_dR_tau_','dR b/w tau and second lepton','0.','6.','120','1'])
#            makeplot([dirname+"reg_"+reg+"_min_lep_dR_tau",'h_reg_'+reg+'_min_lep_dR_tau_','minimum dR b/w tau and leptons','0.','6.','120','1'])
       '''
