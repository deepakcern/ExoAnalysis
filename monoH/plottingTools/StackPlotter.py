import os
import sys
import datetime
import sys, optparse
import sample_xsec_2017 as sample_xsec
import ROOT as ROOT
import array

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

print ("Using dataset "+dtset)

datestr = datetime.date.today().strftime("%d%m%Y")

os.system('mkdir -p'+' '+str(datestr)+'/monoHPng')
os.system('mkdir -p'+' '+str(datestr)+'/monoHPdf')
os.system('mkdir -p'+' '+str(datestr)+'/monoHROOT')

#path='/Users/dekumar/MEGA/Fullwork/2017_Plotting/rootFiles_Oct5'
path='/Users/dekumar/MEGA/Fullwork/2017_Plotting/Files_ZCR'
#path='/home/deepak/MEGA/Fullwork/2017_Plotting/rootFiles'
#path='/Users/dekumar/Desktop/test/bkg_data'
#os.system("ls "+path+" | cat > samplelist.txt")

lumi2016 = 41.0 * 1000

# bins=[200,270,345,480,1000]

# xv = 1000.0/15.0;
# bins=[200+i*xv for i in range(15)]
#Double_t bins[16] = {200.0,200.0+xv,200.0+2*xv,200.0+3*xv,200.0+4*xv,200.0+5*xv,200.0+6*xv,200.0+7*xv,200.0+8*xv,200.0+9*xv,200.0+10*xv,200.0+11*xv,200.0+12*xv,200.0+13*xv,200.0+14*xv,200.0+15*xv};
def setHistStyle(h_temp2,hist):
    dovarbin=False
    h_temp_=h_temp2
    bins=[]
    if '1e2bW_ca15jet_pT' in hist or '1mu2bW_ca15jet_pT' in hist:
        xv = 1000.0/15.0;
        bins=[200+i*xv for i in range(16)]
        dovarbin= True

    elif '1e2bT_ca15jet_p' in hist or '1mu2bT_ca15jet_p' in hist:
        xv = 500.0/15.0;
        bins=[200+i*xv for i in range(16)]
        dovarbin= True

    elif '1e2bT_lep1_pT' in hist or '1mu2bT_lep1_pT' in hist:
        xv = 380.0/15.0;
        bins=[20.0+i*xv for i in range(16)]
        dovarbin= True


    elif '1e2bW_lep1_pT' in hist or '1mu2bW_lep1_pT' in hist:
        xv = 680.0/15.0;
        bins=[20.0+i*xv for i in range(16)]
        dovarbin= True

    elif '1e2bT_ca15jet_SD' in hist or '1mu2bT_ca15jet_SD' in hist or '1e2bW_ca15jet_SD' in hist or '1mu2bW_ca15jet_SD' in hist:
        xv = 50.0/15.0;
        bins=[100.0+i*xv for i in range(16)]
        dovarbin= True

    elif '1e2bT_N2_' in hist or '1mu2bT_N2_' in hist:
        xv=0.445/20.0
        bins=[0+i*xv for i in range(21)]
        dovarbin= True

    elif '1e2bT_N2DDT_' in hist or '1mu2bT_N2DDT_' in hist:
        xv=0.445/24.0
        bins=[-0.2+i*xv for i in range(25)]
        dovarbin= True

    elif 'hadrecoil' in hist or 'met' in hist:
        # xv = 680.0/15.0;
        bins=[200,270,345,480,1000]
        dovarbin= True

    if dovarbin:
        h_temp_=h_temp2.Rebin(len(bins)-1,"h_temp",array.array('d',bins))
        h_temp_.SetBinContent(len(bins)-1,h_temp_.GetBinContent(len(bins)-1)+h_temp_.GetBinContent(len(bins))) #Add overflow bin content to last bin
        h_temp_.SetBinContent(len(bins),0.)
        # h_temp_.GetXaxis().SetRangeUser(200,1000)
        # h_temp_.SetMarkerColor(kBlack);
        # h_temp_.SetMarkerStyle(2);

    if not dovarbin:
        h_temp_=h_temp2

    return h_temp_



def makeplot(loc,hist,titleX,XMIN,XMAX,Rebin,ISLOG,NORATIOPLOT,reg,varBin):
    # try:

    print ('plotting histogram:   ',hist)
    isrebin=False #bool(varBin)
    files=open("samplelist_2017.txt","r")


    ROOT.gStyle.SetOptStat(0);
    ROOT.gStyle.SetOptTitle(0);
    ROOT.gStyle.SetFrameLineWidth(3);
    #gStyle->SetErrorX(0);
    ROOT.gStyle.SetLineWidth(1);

    if '_sr2' in hist:
        histolabel="#splitline{monoHbb}{boosted}"
    elif '2mu2b' in hist:
        histolabel="Dimuon CR"
    elif '2e2b' in hist:
        histolabel="Dielectron CR"
    elif 'Wmu' in hist and 'TopWmu' not in hist:
        histolabel="W CR (#mu)"
    elif 'We' in hist and 'TopWe' not in hist:
        histolabel="W CR (e)"
    elif 'Topmu' in hist:
        histolabel="t#bar{t} CR (#mu)"
    elif 'Tope' in hist:
        histolabel="t#bar{t} CR (e)"
    elif 'TopWe' in hist:
        histolabel="t#bar{t} + W CR (e)"

    elif 'TopWmu' in hist:
        histolabel="t#bar{t} + W CR (#mu)"
        # histolabel="t#bar{t} CR (e+#mu)"
    else:
        histolabel="testing"

    xsec=1.0
    norm = 1.0
    BLINDFACTOR = 1.0
    r_fold = 'rootFiles/'
    DIBOSON = ROOT.TH1F()
    Top = ROOT.TH1F()
    WJets = ROOT.TH1F()
    DYJets = ROOT.TH1F()
    ZJets = ROOT.TH1F()
    STop = ROOT.TH1F()
    GJets = ROOT.TH1F()
    QCD = ROOT.TH1F()
    SMH = ROOT.TH1F()

    DYJets_Hits   = []; ZJets_Hits   = []; WJets_Hists   = []; GJets_Hists  = []; DIBOSON_Hists = []; STop_Hists   = []; Top_Hists     = []; QCD_Hists    = []; SMH_Hists     = []
    MET_Hist      = []; SE_Hist      = []

    count=0
    for file in files.readlines()[:]:
        myFile=path+'/'+file.rstrip()
        print ('running for file',myFile)
        print ('histName',hist)
        Str=str(count)
        exec("f"+Str+"=ROOT.TFile(myFile,'READ')",locals(), globals())
        exec("h_temp=f"+Str+".Get("+"\'"+str(hist)+"\'"+")",locals(), globals())
        exec("h_total_weight=f"+Str+".Get('h_total_mcweight')",locals(), globals())
        total_events = h_total_weight.Integral()
        print ('selected events',h_temp.Integral())


        if 'WJetsToLNu_HT' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                WJets_Hists.append(h_temp2)
            else:WJets_Hists.append(h_temp)

        elif 'DYJetsToLL_M-50' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                DYJets_Hits.append(h_temp2)
            else:DYJets_Hits.append(h_temp)

        elif 'ZJetsToNuNu' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                ZJets_Hits.append(h_temp2)
            else:ZJets_Hits.append(h_temp)

        elif 'GJets_HT' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                GJets_Hists.append(h_temp2)
            else:GJets_Hists.append(h_temp)

        elif ('WWTo' in file) or ('WZTo' in file) or ('ZZTo' in file):
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                DIBOSON_Hists.append(h_temp2)
            else:DIBOSON_Hists.append(h_temp)


        elif ('ST_t' in file) or ('ST_s' in file):
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                STop_Hists.append(h_temp2)
            else:STop_Hists.append(h_temp)

        elif 'TTTo' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                Top_Hists.append(h_temp2)

            else:Top_Hists.append(h_temp)


        elif 'QCD' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                QCD_Hists.append(h_temp2)
            else:QCD_Hists.append(h_temp)

        elif 'HToBB' in file:
            xsec = sample_xsec.getXsec(file)
            # print ('xsec', xsec)
            if (total_events > 0): normlisation=(xsec*lumi2016)/(total_events)
            else: normlisation=0
            h_temp.Scale(normlisation)
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                SMH_Hists.append(h_temp2)
            else:SMH_Hists.append(h_temp)

        elif 'combined_data_MET' in file:
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                MET_Hist.append(h_temp2)
            else:MET_Hist.append(h_temp)

        elif 'combined_data_SE' in file:
            if isrebin:
                h_temp2=setHistStyle(h_temp,hist)
                SE_Hist.append(h_temp2)
            else:SE_Hist.append(h_temp)

        count+=1

###==========================================================add all the histograms regional based ======================================

    for i in range(len(WJets_Hists)):
        if i==0:
            WJets=WJets_Hists[i]
        else:WJets.Add(WJets_Hists[i])
    WJets.Sumw2()

    for i in range(len(DYJets_Hits)):
        if i==0:
            DYJets=DYJets_Hits[i]
        else:DYJets.Add(DYJets_Hits[i])
    DYJets.Sumw2()

    for i in range(len(ZJets_Hits)):
        if i==0:
            ZJets=ZJets_Hits[i]
        else:ZJets.Add(ZJets_Hits[i])
    ZJets.Sumw2()


    for i in range(len(GJets_Hists)):
        if i==0:
            GJets=GJets_Hists[i]
        else:GJets.Add(GJets_Hists[i])
    GJets.Sumw2()


    for i in range(len(DIBOSON_Hists)):
        if i==0:
            DIBOSON=DIBOSON_Hists[i]
        else:DIBOSON.Add(DIBOSON_Hists[i])
    DIBOSON.Sumw2()

    for i in range(len(STop_Hists)):
        if i==0:
            STop=STop_Hists[i]
        else:STop.Add(STop_Hists[i])
    STop.Sumw2()

    for i in range(len(Top_Hists)):
        if i==0:
            Top=Top_Hists[i]
        else:Top.Add(Top_Hists[i])
    Top.Sumw2()

    for i in range(len(QCD_Hists)):
        if i==0:
            QCD=QCD_Hists[i]
        else:QCD.Add(QCD_Hists[i])
    QCD.Sumw2()

    for i in range(len(SMH_Hists)):
        if i==0:
            SMH=SMH_Hists[i]
        else:SMH.Add(SMH_Hists[i])
    SMH.Sumw2()

##=================================================================

    ZJetsCount    =   ZJets.Integral();
    DYJetsCount   =   DYJets.Integral();
    WJetsCount    =   WJets.Integral();
    STopCount     =   STop.Integral();
    GJetsCount    =   GJets.Integral();
    TTCount       =   Top.Integral();
    VVCount       =   DIBOSON.Integral();
    QCDCount      =   QCD.Integral();
    SMHCount      =   SMH.Integral();


    mcsum = ZJetsCount + DYJetsCount + WJetsCount + STopCount + GJetsCount + TTCount + VVCount + QCDCount + SMHCount
    total_hists = WJets_Hists + DYJets_Hits + ZJets_Hits + GJets_Hists + DIBOSON_Hists + STop_Hists + Top_Hists + QCD_Hists + SMH_Hists


    DYLegend    =   "Z(ll) + jets "
    WLegend     =   "W(l#nu) + jets:"
    GLegend     =   "G jets "
    ZLegend     =   "Z(#nu#nu) + jets "
    STLegend    =   "Single t "
    TTLegend    =   "Top "
    VVLegend    =   "DIBOSON "
    QCDLegend   =   "QCD  "
    SMHLegend   =  "SM H "

    legend = ROOT.TLegend(0.60, 0.50, 0.94,0.94,'',"brNDC");
    legend.SetTextSize(0.020);
    legend.SetBorderSize(0);
    legend.SetLineColor(1);
    legend.SetLineStyle(1);
    legend.SetLineWidth(1);
    legend.SetFillColor(0);
    legend.SetFillStyle(0);
    legend.SetTextFont(42);
    legend.SetNColumns(1);

    # legend.AddEntry(DYJets,DYLegend,"f");
    # legend.AddEntry(ZJets,ZLegend,"f");
    # legend.AddEntry(WJets,WLegend,"f");
    # legend.AddEntry(Top,TTLegend,"f");
    # legend.AddEntry(STop,STLegend,"f");
    # legend.AddEntry(GJets,GLegend,"f");
    # legend.AddEntry(DIBOSON,VVLegend,"f");
    # legend.AddEntry(QCD,QCDLegend,"f");
    # legend.AddEntry(SMH,SMHLegend,"f");

    if dtset=="SE":
        h_data=SE_Hist[0]
    else:h_data=MET_Hist[0]
    h_data.Sumw2()
    #h_data.Rebin(REBIN)
    h_data.SetMarkerColor(ROOT.kBlack);
    h_data.SetMarkerStyle(20);
    h_data.SetLineColor(1)


    ROOT.gStyle.SetHistTopMargin(0.)


    if(not NORATIOPLOT):
        legend.AddEntry(h_data,"Data","PEL")
        # h_data.Draw("same p e1");

    legend.AddEntry(Top,TTLegend,"f");
    legend.AddEntry(STop,STLegend,"f");
    legend.AddEntry(WJets,WLegend,"f");
    legend.AddEntry(DIBOSON,VVLegend,"f");
    if GJetsCount > 0:legend.AddEntry(GJets,GLegend,"f");
    if ZJetsCount > 0:legend.AddEntry(ZJets,ZLegend,"f");
    legend.AddEntry(DYJets,DYLegend,"f");
    legend.AddEntry(QCD,QCDLegend,"f");
    legend.AddEntry(SMH,SMHLegend,"f");


#============== CANVAS DECLARATION ===================
    c12 = ROOT.TCanvas("Hist", "Hist", 0,0,1000,1000);

#==================Stack==============================
    hs = ROOT.THStack("hs"," ");

#============Colors for Histos
    DYJets.SetFillColor(ROOT.kGreen+2);
    DYJets.SetLineWidth(0);
    ZJets.SetFillColor(ROOT.kAzure+1);
    ZJets.SetLineWidth(0);
    DIBOSON.SetFillColor(ROOT.kBlue+2);
    DIBOSON.SetLineWidth(0);
    Top.SetFillColor(ROOT.kOrange-2);
    Top.SetLineWidth(0);
    WJets.SetFillColor(ROOT.kViolet-3);
    WJets.SetLineWidth(0);
    STop.SetFillColor(ROOT.kOrange+1);
    STop.SetLineWidth(0);
    GJets.SetFillColor(ROOT.kCyan-9);
    GJets.SetLineWidth(0);
    QCD.SetFillColor(ROOT.kGray+1);
    QCD.SetLineWidth(0);
    SMH.SetFillColor(ROOT.kRed-2);
    SMH.SetLineWidth(0);

#=====================Stack all the histogram =========================

    ZJetsCount    =   ZJets.Integral();
    DYJetsCount   =   DYJets.Integral();
    WJetsCount    =   WJets.Integral();
    STopCount     =   STop.Integral();
    GJetsCount    =   GJets.Integral();
    TTCount       =   Top.Integral();
    VVCount       =   DIBOSON.Integral();
    QCDCount      =   QCD.Integral();
    SMHCount      =   SMH.Integral();

    '''
    if (SMHCount > 0 ):    hs.Add(SMH,"hist");
    if (GJetsCount > 0):   hs.Add(GJets,"hist");
    if (VVCount > 0):      hs.Add(DIBOSON,"hist");
    if (QCDCount > 0):     hs.Add(QCD,"hist");
    if (STopCount > 0):    hs.Add(STop,"hist");
    if (TTCount > 0):      hs.Add(Top,"hist");
    if (WJetsCount > 0):   hs.Add(WJets,"hist");
    if (ZJetsCount > 0):   hs.Add(ZJets,"hist");
    if (DYJetsCount > 0):  hs.Add(DYJets,"hist");
    '''

    if (SMHCount > 0 ):    hs.Add(SMH,"hist");
    if (QCDCount > 0):     hs.Add(QCD,"hist");
    if (DYJetsCount > 0):  hs.Add(DYJets,"hist");
    if (ZJetsCount > 0):   hs.Add(ZJets,"hist");
    if (GJetsCount > 0):   hs.Add(GJets,"hist");
    if (VVCount > 0):      hs.Add(DIBOSON,"hist");
    if (WJetsCount > 0):   hs.Add(WJets,"hist");
    if (STopCount > 0):    hs.Add(STop,"hist");
    if (TTCount > 0):      hs.Add(Top,"hist");

    hasNoEvents=False
    Stackhist = hs.GetStack().Last()

    maxi = Stackhist.GetMaximum()
    Stackhist.SetLineWidth(2)
    if (Stackhist.GetEntries()==0):
        hasNoEvents=True
        print ('No events found! for '+hist+'\n')



# =====================histogram for systematic/ statistical uncertainty ========================

    h_err = total_hists[0].Clone("h_err");

    # h_err.Sumw2()
    h_err.Reset()
    for i in range(len(total_hists)):
        if i==0: continue
        else:
            if (total_hists[i].Integral()>0):
                h_err.Add(total_hists[i])
    h_err.Sumw2()
    h_err.SetFillColor(ROOT.kGray+3)
    h_err.SetLineColor(ROOT.kGray+3)
    h_err.SetMarkerSize(0)
    h_err.SetFillStyle(3013)





    if(NORATIOPLOT):
        c1_2 = ROOT.TPad("c1_2","newpad",0,0.05,1,1);   #0.993);
        c1_2.SetRightMargin(0.04);

    else:
        c1_2 =  ROOT.TPad("c1_2","newpad",0,0.28,1,1);

    c1_2.SetBottomMargin(0.09);
    c1_2.SetTopMargin(0.06);
    c1_2.SetLogy(ISLOG);
    #if(VARIABLEBINS){ c1_2->SetLogx(0);}
    c1_2.Draw();
    c1_2.cd();
    hs.Draw()
#    h_err.Draw("E2 SAME")

#####================================= data section =========================

    # if dtset=="SE":
    #     h_data=SE_Hist[0]
    # else:h_data=MET_Hist[0]
    # h_data.Sumw2()
    # #h_data.Rebin(REBIN)
    # h_data.SetLineColor(1)
    #
    #
    # ROOT.gStyle.SetHistTopMargin(0.)
    #
    #
    if(not NORATIOPLOT):
        h_data.Draw("same p e1");
    # if(ISLOG==1):    hs.SetMinimum(0.28);
    # if(ISLOG==0):    hs.SetMaximum(maxi*1.35);
    # if(ISLOG==0):    hs.SetMinimum(0.0001);


    if (ISLOG):
        #print ('maxima:',maxi,'   for   ', hist)
        hs.SetMaximum(maxi * 50)
        hs.SetMinimum(0.1)
    else:
        hs.SetMaximum(maxi * 1.35)
        hs.SetMinimum(0)
##=============================== hs setting section =====================
#
    if (not hasNoEvents):
        hs.GetXaxis().SetNdivisions(508)
        if(NORATIOPLOT):
            hs.GetXaxis().SetTitleOffset(1.05)
            hs.GetXaxis().SetTitleFont(42)
            hs.GetXaxis().SetLabelFont(42)
            hs.GetXaxis().SetLabelSize(.03)
            hs.GetYaxis().SetTitle("Events")
            hs.GetYaxis().SetTitleSize(0.12)
            hs.GetYaxis().SetTitleOffset(1.5)
            hs.GetYaxis().SetTitleFont(42)
            hs.GetYaxis().SetLabelFont(42)
            hs.GetYaxis().SetLabelSize(0.05)
            hs.GetXaxis().SetTitle(str(titleX))
            hs.GetXaxis().SetTitleFont(42)
            hs.GetXaxis().SetLabelFont(42);
            hs.GetXaxis().SetLabelOffset(.01);
            hs.GetXaxis().SetLabelSize(0.03);
            hs.GetYaxis().SetTitle("Events");
            hs.GetYaxis().SetTitleSize(0.05);
            hs.GetYaxis().SetTitleFont(42);
            hs.GetYaxis().SetLabelFont(42);
            hs.GetYaxis().SetLabelSize(.03);
        else:
            #hs.GetXaxis().SetTitle(str(titleX))
            # hs.GetXaxis().SetTitleSize(0.00);
            hs.GetXaxis().SetTitleOffset(0.00);
            hs.GetXaxis().SetTitleFont(42);
            hs.GetXaxis().SetLabelFont(42);
            hs.GetXaxis().SetLabelOffset(.01);
            hs.GetXaxis().SetLabelSize(0.04);
            hs.GetYaxis().SetTitle("Events");
            hs.GetYaxis().SetTitleSize(0.045);
            hs.GetYaxis().SetTitleOffset(1);
            hs.GetYaxis().SetTitleFont(42);
            hs.GetYaxis().SetLabelFont(42);
            hs.GetYaxis().SetLabelSize(.03);

        if not isrebin: hs.GetXaxis().SetRangeUser(XMIN,XMAX);
        hs.GetXaxis().SetNdivisions(508)

#=============================legend section =========================================

    #legend.AddEntry(h_err,"Stat. Unc.","f")
    legendsig =  ROOT.TLegend(0.57, 0.5, 0.94,0.65,'',"brNDC");
    legendsig.SetTextSize(0.030);
    legendsig.SetBorderSize(0);
    legendsig.SetLineColor(1);
    legendsig.SetLineStyle(1);
    legendsig.SetLineWidth(1);
    legendsig.SetFillColor(0);
    legendsig.SetFillStyle(0);
    legendsig.SetTextFont(42);

    legend.Draw('same')

#=================================================latex section =====================
    latexPreCMSname= "#bf{CMS} #it{Preliminary}"
    t2c =  ROOT.TLatex(0.10,0.97,latexPreCMSname);
    t2c.SetTextSize(0.045)

    t2a =  ROOT.TLatex(0.7,0.97,'35.5 fb^{-1} (13TeV )');
    t2a.SetTextSize(0.040);

    t2b = ROOT.TLatex(0.22,0.88,'');
    t2b.SetTextSize(0.03);


    t2d = ROOT.TLatex(0.40,0.9,str(histolabel));
    t2d.SetTextSize(0.045);

    t2a.SetTextAlign(12);
    t2a.SetNDC(ROOT.kTRUE);
    t2a.SetTextFont(42);
    t2b.SetTextAlign(12);
    t2b.SetNDC(ROOT.kTRUE);
    t2b.SetTextFont(61);
    t2c.SetTextAlign(12);
    t2c.SetNDC(ROOT.kTRUE);
    t2c.SetTextFont(42);
    t2d.SetTextAlign(12);
    t2d.SetNDC(ROOT.kTRUE);
    t2d.SetTextFont(42);
    t2a.Draw("same");
    t2b.Draw("same");
    t2c.Draw("same");
    t2d.Draw("same");
#======================================== ratio log ================

    ratioleg =  ROOT.TLegend(0.6, 0.88, 0.89, 0.98);
    #//ratioleg->SetFillColor(0);
    ratioleg.SetLineColor(0);
    ratioleg.SetShadowColor(0);
    ratioleg.SetTextFont(42);
    ratioleg.SetTextSize(0.09);
    ratioleg.SetBorderSize(1);
    ratioleg.SetNColumns(2);


#============================================= statistical error section ======================

    ratiostaterr = h_err.Clone("ratiostaterr")
    ratiostaterr.Sumw2()
    ratiostaterr.SetStats(0);
    ratiostaterr.SetMinimum(0);
    ratiostaterr.SetMarkerSize(0);
    ratiostaterr.SetFillColor(ROOT.kBlack);
    ratiostaterr.SetFillStyle(3013);
    for i in range(h_err.GetNbinsX()+2):
        ratiostaterr.SetBinContent(i, 0.0)

        if (h_err.GetBinContent(i) > 1e-6 ):
            binerror = h_err.GetBinError(i)/h_err.GetBinContent(i)
            ratiostaterr.SetBinError(i, binerror)
        else:ratiostaterr.SetBinError(i, 999.)

    ratioleg.AddEntry(ratiostaterr, "stat", "f")

 #============================================= Lower Tpad Decalaration ====================================
    if(not NORATIOPLOT):
        c12.cd()
        DataMC    = h_data.Clone()
        DataMC.Add(Stackhist,-1)   # remove for data/mc
        DataMCPre = h_data.Clone();
        DataMC.Divide(Stackhist);
        DataMC.GetYaxis().SetTitle("#frac{Data-Pred}{Pred}.");
        DataMC.GetYaxis().SetTitleSize(0.1);
        DataMC.GetYaxis().SetTitleOffset(0.42);
        DataMC.GetYaxis().SetTitleFont(42);
        DataMC.GetYaxis().SetLabelSize(0.08);
        DataMC.GetYaxis().CenterTitle();
        DataMC.GetXaxis().SetTitle(str(titleX))
        DataMC.GetXaxis().SetLabelSize(0.1);
        DataMC.GetXaxis().SetTitleSize(0.1);
        DataMC.GetXaxis().SetTitleOffset(1);
        DataMC.GetXaxis().SetTitleFont(42);
        DataMC.GetXaxis().SetTickLength(0.07);
        DataMC.GetXaxis().SetLabelFont(42);
        DataMC.GetYaxis().SetLabelFont(42);


    c1_1 = ROOT.TPad("c1_1", "newpad",0,0.00,1,0.3);
    if (not NORATIOPLOT): c1_1.Draw();
    c1_1.cd();
    c1_1.Range(-7.862408,-629.6193,53.07125,486.5489);
    c1_1.SetFillColor(0);
    c1_1.SetTicky(1);
    c1_1.SetLeftMargin(0.1);
    c1_1.SetRightMargin(0.1);
    c1_1.SetTopMargin(0.0);
    c1_1.SetBottomMargin(0.32);
    c1_1.SetFrameFillStyle(0);
    c1_1.SetFrameBorderMode(0);
    c1_1.SetFrameFillStyle(0);
    c1_1.SetFrameBorderMode(0);
    c1_1.SetLogy(0);

    if(not NORATIOPLOT):
        if (0): # if(VARIABLEBINS)
            c1_1.SetLogx(0)
            DataMC.GetXaxis().SetMoreLogLabels()
            DataMC.GetXaxis().SetNoExponent()
            DataMC.GetXaxis().SetNdivisions(508)

        if not isrebin: DataMC.GetXaxis().SetRangeUser(XMIN,XMAX)
        DataMC.SetMarkerSize(0.7)
        DataMC.SetMarkerStyle(20)
        DataMC.SetMarkerColor(1)
        DataMC.SetMinimum(-0.58)
        DataMC.SetMaximum(0.58)
        DataMC.GetXaxis().SetNdivisions(508)
        DataMC.GetYaxis().SetNdivisions(505)
        DataMC.Draw("P e1")
        ratiostaterr.Draw("e2 same")
        DataMC.Draw("P e1 same")
        line0=  ROOT.TLine(XMIN,1,XMAX,1)
        line0.SetLineStyle(2)
        line0.Draw("same")
        c1_1.SetGridy()
        ratioleg.Draw("same")
    c12.Draw()

    outputshapefilename=str(hist)
    if(ISLOG==0):
        c12.SaveAs(str(datestr)+'/monoHPdf/'+str(outputshapefilename)+'.pdf')
        c12.SaveAs(str(datestr)+'/monoHPng/'+str(outputshapefilename)+'.png')

    if(ISLOG==1):
        c12.SaveAs(str(datestr)+'/monoHPdf/'+str(outputshapefilename)+'log.pdf')
        c12.SaveAs(str(datestr)+'/monoHPng/'+str(outputshapefilename)+'log.png')


    rootFile=str(datestr)+'/monoHROOT/'+str(outputshapefilename)+'.root'
    print (rootFile)
    fshape = ROOT.TFile(rootFile,"RECREATE")
    fshape.cd()
    Stackhist.SetNameTitle("bkgSum","bkgSum")
    Stackhist.Write()
    DIBOSON.SetNameTitle("DIBOSON","DIBOSON");
    DIBOSON.Write()
    ZJets.SetNameTitle("ZJets","ZJets");
    ZJets.Write()
    GJets.SetNameTitle("GJets","GJets");
    GJets.Write()
    QCD.SetNameTitle("QCD","QCD");
    QCD.Write()
    SMH.SetNameTitle("SMH","SMH");
    SMH.Write();
    STop.SetNameTitle("STop","STop");
    STop.Write();
    Top.SetNameTitle("Top","Top");
    Top.Write();
    WJets.SetNameTitle("WJets","WJets");
    WJets.Write();
    DYJets.SetNameTitle("DYJets","DYJets");
    DYJets.Write();
    data_obs=h_data
    data_obs.SetNameTitle("data_obs","data_obs");
    data_obs.Write();
    fshape.Write();
    fshape.Close();


    # except Exception as e:
    #     print (e)
    #     print ('this hist does not exit in the root file'+'\n')
    #     pass
    # c1_2.SaveAs('test.png')
    # c1_2.SaveAs('test.pdf')
#=======================================================================


######################################################################

regions=[]
PUreg=[]


#makeplot("reg_Topmu_Recoil",'h_reg_Topmu_Recoil','Hadronic Recoil (GeV)',200.,1000.,1,1,0,'reg',varBin=False)
#makeplot("reg_Wmu_Recoil",'h_reg_Wmu_Recoil','Hadronic Recoil (GeV)',200.,1000.,1,1,0,'reg',varBin=False)
#makeplot("reg_We_Recoil",'h_reg_We_Recoil','Hadronic Recoil (GeV)',200.,1000.,1,1,0,'reg',varBin=False)
#makeplot("reg_Tope_Recoil",'h_reg_Tope_Recoil','Hadronic Recoil (GeV)',200.,1000.,1,1,0,'reg',varBin=False)


if makeMuCRplots:
    regions+=['Topmu','Wmu','TopWmu']
    PUreg+=['mu_']
if makeEleCRplots:
    regions+=['Tope','We','TopWe']
'''
    PUreg+=['ele_']
if makePhoCRplots:
    regions+=['1gamma2b']
    PUreg+=['pho_']
if makeQCDCRplots:
    regions+=['QCD2b']
    PUreg+=[]
'''

for reg in regions:
    makeplot("reg_"+reg+"_Recoil",'h_reg_'+reg+'_Recoil','Hadronic Recoil (GeV)',200.,1000.,1,1,0,'reg',varBin=False)

    makeplot("reg_"+reg+"_FJetPt",'h_reg_'+reg+'_FJetPt','FATJET p_{T} (GeV)',200.,1000.,1,1,0,'reg',varBin=False)
    makeplot("reg_"+reg+"_FJetEta",'h_reg_'+reg+'_FJetEta','FATJET #eta',-2.5,2.5,1,0,0,'reg',varBin=False)
    makeplot("reg_"+reg+"_FJetPhi",'h_reg_'+reg+'_FJetPhi','FATJET #phi',-3.14,3.14,1,0,0,'reg',varBin=False)

    # makeplot("reg_"+reg+"_Jet1Pt",'h_reg_'+reg+'_Jet1Pt','Jet1 p_{T}',200.,1000.,1,1,0,'reg',varBin=False)
    # makeplot("reg_"+reg+"_Jet1Eta",'h_reg_'+reg+'_Jet1Eta','Jet1 #eta',-2.5,2.5,1,0,0,'reg',varBin=False)
    # makeplot("reg_"+reg+"_Jet1Phi",'h_reg_'+reg+'_Jet1Phi','Jet1 #phi',-3.14,3.14,1,0,0,'reg',varBin=False)
    #
    makeplot("reg_"+reg+"_lep1_pT",'h_reg_'+reg+'_lep1_pT','lepton1 p_{T}',0,500,1,1,0,'reg',varBin=False)
