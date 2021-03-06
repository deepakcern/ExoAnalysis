#coded by pctiwari
import ROOT as rt
import math,os,sys
import CMS_lumi, tdrstyle
import array, sample_xsec,optparse
import datetime
import os.path
import array as array

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

datestr = str(datetime.date.today().strftime("%d%m%Y"))


# In[2]:


#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600
W_ref = 800
W = W_ref
H  = H_ref

iPeriod = 4

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

canvas = rt.TCanvas("c2","c2",50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)

hists=[]
regions=[]
PUreg=[]
lumi = 41 * 1000


print('Done')


# In[3]:


def makeplot(plot_location,plot,titleX,XMIN,XMAX,Rebin,ISLOG,NORATIOPLOT,reg):
    file=open("samplelist_2017.txt","r")
    xsec=1.0
    norm = 1.0
    BLINDFACTOR = 1.0
    r_fold = 'rootFiles/'
    DIBOSON = rt.TH1F()
    Top = rt.TH1F()
    WJets = rt.TH1F()
    DYJets = rt.TH1F()
    ZJets = rt.TH1F()
    STop = rt.TH1F()
    GJets = rt.TH1F()
    QCD = rt.TH1F()
    DYJets_files  = []; ZJets_files = []
    WJets_files  = []; GJets_files = []
    DIBOSON_files = []; STop_files  = []
    Top_files     = []; QCD_files   = []
    data_file_MET = []; data_file_SE = []
    for i in file.readlines()[:]:
        f = rt.TFile('rootFiles/'+str(i.rstrip()),'READ')
        file_name = str(f)
        if 'data_combined_MET' in file_name:
            data_file_MET.append(f)
        elif 'data_combined_SE' in file_name:
            data_file_SE.append(f)
        elif 'DYJetsToLL_M-50' in file_name:
            DYJets_files.append(f)
        elif 'ZJetsToNuNu' in file_name:
            ZJets_files.append(f)
        elif 'WJetsToLNu' in file_name:
            WJets_files.append(f)
        elif 'GJets' in file_name:
            GJets_files.append(f)
        elif 'QCD' in file_name:
            QCD_files.append(f)
        #elif 'TT_T' or 'TTT' in file_name:
        elif 'TT_T' in file_name:
            Top_files.append(f)
        elif ('WWTo' in file_name) or ('WZTo' in file_name) or ('ZZTo' in file_name):
            DIBOSON_files.append(f)
        elif ('ST_t' in file_name) or ('ST_s' in file_name):
            STop_files.append(f)

    plot_recoil = 'hadrecoil' in str(plot)

    #print (plot_recoil)
    bins=[200,250,300,400,500,700,1000,2000]
    for inum in range(len(DYJets_files)):
        xsec = sample_xsec.getXsec(str(DYJets_files[inum]))
        hist_integral = DYJets_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            DYJets = (DYJets_files[inum].Get(str(plot)))
            DYJets.Scale(norm)
            if plot_recoil:
                DYJets=DYJets.Rebin(len(bins)-1,"DYJets",array.array('d',bins))
                DYJets.SetBinContent(len(bins)-1,DYJets.GetBinContent(len(bins)-1)+DYJets.GetBinContent(len(bins)))
                DYJets.SetBinContent(len(bins),0.)
        else:
            temp_hist = DYJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            DYJets.Add(temp_hist)

    for inum in range(len(GJets_files)):
        xsec = sample_xsec.getXsec(str(GJets_files[inum]))
        hist_integral = GJets_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            GJets = (GJets_files[inum].Get(str(plot)))
            GJets.Scale(norm)
            if plot_recoil:
                GJets=GJets.Rebin(len(bins)-1,"GJets",array.array('d',bins))
                GJets.SetBinContent(len(bins)-1,GJets.GetBinContent(len(bins)-1)+GJets.GetBinContent(len(bins)))
                GJets.SetBinContent(len(bins),0.)
        else:
            temp_hist = GJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            GJets.Add(temp_hist)

    for inum in range(len(ZJets_files)):
        xsec = sample_xsec.getXsec(str(ZJets_files[inum]))
        hist_integral = ZJets_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            ZJets = (ZJets_files[inum].Get(str(plot)))
            ZJets.Scale(norm)
            if plot_recoil:
                ZJets=ZJets.Rebin(len(bins)-1,"ZJets",array.array('d',bins))
                ZJets.SetBinContent(len(bins)-1,ZJets.GetBinContent(len(bins)-1)+ZJets.GetBinContent(len(bins)))
                ZJets.SetBinContent(len(bins),0.)
        else:
            temp_hist = ZJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            ZJets.Add(temp_hist)

    for inum in range(len(WJets_files)):
        xsec = sample_xsec.getXsec(str(WJets_files[inum]))
        hist_integral = WJets_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            WJets = (WJets_files[inum].Get(str(plot)))
            WJets.Scale(norm)
            if plot_recoil:
                WJets=WJets.Rebin(len(bins)-1,"WJets",array.array('d',bins))
                WJets.SetBinContent(len(bins)-1,WJets.GetBinContent(len(bins)-1)+WJets.GetBinContent(len(bins)))
                WJets.SetBinContent(len(bins),0.)
        else:
            temp_hist = WJets_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            WJets.Add(temp_hist)

    for inum in range(len(DIBOSON_files)):
        xsec = sample_xsec.getXsec(str(DIBOSON_files[inum]))
        hist_integral = DIBOSON_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            DIBOSON = (DIBOSON_files[inum].Get(str(plot)))
            DIBOSON.Scale(norm)
            if plot_recoil:
                DIBOSON=DIBOSON.Rebin(len(bins)-1,"DIBOSON",array.array('d',bins))
                DIBOSON.SetBinContent(len(bins)-1,DIBOSON.GetBinContent(len(bins)-1)+DIBOSON.GetBinContent(len(bins)))
                DIBOSON.SetBinContent(len(bins),0.)
        else:
            temp_hist = DIBOSON_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            DIBOSON.Add(temp_hist)

    for inum in range(len(Top_files)):
        xsec = sample_xsec.getXsec(str(Top_files[inum]))
        hist_integral = Top_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            Top = (Top_files[inum].Get(str(plot)))
            Top.Scale(norm)
            if plot_recoil:
                Top=Top.Rebin(len(bins)-1,"Top",array.array('d',bins))
                Top.SetBinContent(len(bins)-1,Top.GetBinContent(len(bins)-1)+Top.GetBinContent(len(bins)))
                Top.SetBinContent(len(bins),0.)
        else:
            temp_hist = Top_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            Top.Add(temp_hist)

    for inum in range(len(STop_files)):
        xsec = sample_xsec.getXsec(str(STop_files[inum]))
        hist_integral = STop_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            STop = (STop_files[inum].Get(str(plot)))
            STop.Scale(norm)
            if plot_recoil:
                STop=STop.Rebin(len(bins)-1,"STop",array.array('d',bins))
                STop.SetBinContent(len(bins)-1,STop.GetBinContent(len(bins)-1)+STop.GetBinContent(len(bins)))
                STop.SetBinContent(len(bins),0.)
        else:
            temp_hist = STop_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            STop.Add(temp_hist)

    for inum in range(len(QCD_files)):
        xsec = sample_xsec.getXsec(str(QCD_files[inum]))
        hist_integral = QCD_files[inum].Get('h_total').Integral()
        norm = (lumi*xsec)/(hist_integral)
        if inum==0:
            QCD = (QCD_files[inum].Get(str(plot)))
            QCD.Scale(norm)
            if plot_recoil:
                QCD=QCD.Rebin(len(bins)-1,"QCD",array.array('d',bins))
                QCD.SetBinContent(len(bins)-1,QCD.GetBinContent(len(bins)-1)+QCD.GetBinContent(len(bins)))
                QCD.SetBinContent(len(bins),0.)
        else:
            temp_hist = QCD_files[inum].Get(str(plot))
            temp_hist.Scale(norm)
            if plot_recoil:
                temp_hist=temp_hist.Rebin(len(bins)-1,"temp_hist",array.array('d',bins))
                temp_hist.SetBinContent(len(bins)-1,temp_hist.GetBinContent(len(bins)-1)+temp_hist.GetBinContent(len(bins)))
                temp_hist.SetBinContent(len(bins),0.)
            QCD.Add(temp_hist)

    ZJetsCount = ZJets.Integral()
    DYJetsCount = DYJets.Integral()
    WJetsCount = WJets.Integral()
    STopCount = STop.Integral()
    GJetsCount = GJets.Integral()
    TopCount = Top.Integral()
    VVCount = DIBOSON.Integral()
    QCDCount = QCD.Integral()

    mcsum = ZJetsCount + DYJetsCount + WJetsCount + STopCount + GJetsCount + TopCount + VVCount +  QCDCount

    hs = rt.THStack("hs", " ")
    #Colors for Histos
    DYJets.SetFillColor(rt.kGreen + 2)
    ZJets.SetFillColor(rt.kAzure + 1)
    DIBOSON.SetFillColor(rt.kBlue + 2)
    Top.SetFillColor(rt.kOrange - 2)
    WJets.SetFillColor(rt.kViolet - 3)
    STop.SetFillColor(rt.kOrange + 1)
    GJets.SetFillColor(rt.kCyan - 9)
    QCD.SetFillColor(rt.kGray + 1)

    #add the histos to THStack
    hs.Add(GJets, "hist")
    hs.Add(DIBOSON, "hist")
    hs.Add(QCD, "hist")
    hs.Add(STop, "hist")
    hs.Add(Top, "hist")
    hs.Add(WJets, "hist")
    hs.Add(ZJets, "hist")
    hs.Add(DYJets, "hist")

    if makeMuCRplots or makeSRplots:
        data_obs = data_file_MET[0].Get(str(plot))
    elif makeEleCRplots:
        data_obs = data_file_SE[0].Get(str(plot))
    if plot_recoil:
        data_obs=data_obs.Rebin(len(bins)-1,"data_obs",array.array('d',bins))
        data_obs.SetBinContent(len(bins)-1,data_obs.GetBinContent(len(bins)-1)+data_obs.GetBinContent(len(bins)))
        data_obs.SetBinContent(len(bins),0.)
    data_obs.SetMarkerColor(rt.kBlack)
    data_obs.SetMarkerStyle(20)

    Stackhist = hs.GetStack().Last()
    maxi = Stackhist.GetMaximum()
    Stackhist.SetLineWidth(2)

    #error
    h_err = rt.TH1F()
    h_err = data_obs.Clone("h_err")
    h_err.Sumw2()
    h_err.Reset()
    for i in file.readlines():
        if 'data_combined' in i: continue
        h_err.Add(file.Get(plot))
    # MC.Draw("histsame")
    # data.Draw("esamex0")

    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()

    if (NORATIOPLOT):
        canvas1_1 = rt.TPad("canvas1_1", "newpad", 0, 0.05, 1, 1); canvas1_1.Draw()
    else:
        canvas1_1 = rt.TPad("canvas1_1", "newpad", 0, 0.28, 1, 1); canvas1_1.Draw()

    canvas1_1.SetLeftMargin( L/W )
    canvas1_1.SetRightMargin( R/W )
    canvas1_1.SetBottomMargin(0.001)
    #canvas1_1.SetTopMargin( T/H )
    canvas1_1.SetLogy(ISLOG)
    canvas1_1.Draw()
    canvas1_1.cd()
    hs.Draw()
    hs.GetXaxis().SetRangeUser(XMIN, XMAX)
    hs.GetXaxis().SetTitle('Events')
    hs.SetMaximum(maxi * 1.35)
    hs.GetXaxis().SetTickLength(0.07);
    #hs.GetXaxis().SetNdivisions(508);
    if (NORATIOPLOT):
        hs.GetYaxis().SetTitle("Events")
        hs.GetYaxis().SetTitleSize(0.05)
        hs.GetYaxis().SetTitleFont(42)
        hs.GetYaxis().SetLabelFont(42)
        hs.GetYaxis().SetLabelSize(.03)
        hs.GetYaxis().SetMoreLogLabels()
    else:
        hs.GetYaxis().SetTitle("Events")
        hs.GetYaxis().SetTitleSize(0.045)
        hs.GetYaxis().SetTitleOffset(1)
        hs.GetYaxis().SetTitleFont(42)
        hs.GetYaxis().SetLabelFont(42);
        hs.GetYaxis().SetLabelSize(.03)
        hs.GetYaxis().SetMoreLogLabels();

    if (ISLOG):
        hs.SetMinimum(10)
    else:
        hs.SetMinimum(0)

    data_obs.SetLineColor(rt.kBlack)
    data_obs.SetFillColor(rt.kBlack)
    if not NORATIOPLOT:
        data_obs.Draw("same PEL")

    #set the colors and size for the legend
    latex = rt.TLatex()
    n_ = 2

    x1_l = 0.92
    y1_l = 0.90

    dx_l = 0.25
    dy_l = 0.40
    x0_l = x1_l-dx_l
    y0_l = y1_l-dy_l

    legend = rt.TLegend(x0_l,y0_l,x1_l, y1_l,"", "brNDC")
    legend.SetNColumns(2)
    #legend =  rt.("legend_0","legend_0",x0_l,y0_l,x1_l, y1_l )
    legend.AddEntry(data_obs, "Data", "PEL")
    legend.AddEntry(DYJets, "Z(ll) + jets", "f")
    legend.AddEntry(ZJets, "Z(#nu#nu) + jets", "f")
    legend.AddEntry(WJets, "W(l#nu) + jets", "f")
    legend.AddEntry(Top, "Top", "f")
    legend.AddEntry(STop, "Single t", "f")
    legend.AddEntry(GJets, "G jets", "f")
    legend.AddEntry(DIBOSON, "VV, VH", "f")
    legend.AddEntry(QCD, "Multijet", "f")
    #legend.SetFillColor( rt.kGray )
    legend.Draw('same')

    ratiostaterr = h_err
    ratiostaterr.Sumw2()
    ratiostaterr.SetStats(0)
    ratiostaterr.SetMinimum(0)
    ratiostaterr.SetMarkerSize(0)
    ratiostaterr.SetFillColor(rt.kBlack)
    ratiostaterr.SetFillStyle(3013)

    for i in range(0,h_err.GetNbinsX()+2):
        ratiostaterr.SetBinContent(i, 1.0)
        if (h_err.GetBinContent(i) > 1e-6):
            binerror = h_err.GetBinError(i)/h_err.GetBinContent(i)
            ratiostaterr.SetBinError(i, binerror)
        else:
            ratiostaterr.SetBinError(i, 999.)

    ratiosysterr = ratiostaterr
    ratiosysterr.Sumw2()
    ratiosysterr.SetMarkerSize(0)
    ratiosysterr.SetFillColor(rt.kGray)
    ratiosysterr.SetFillStyle(1001)

    for i in range(0,h_err.GetNbinsX()+2):
        if (h_err.GetBinContent(i) > 1e-6):
            binerror2 = (pow(h_err.GetBinError(i), 2) +
                pow(0.25 * WJets.GetBinContent(i), 2) +
                pow(0.25 * ZJets.GetBinContent(i), 2) +
                pow(0.20 * DYJets.GetBinContent(i), 2) +
                pow(0.25 * Top.GetBinContent(i), 2) +
                pow(0.20 * GJets.GetBinContent(i), 2) +
                pow(0.20 * QCD.GetBinContent(i), 2) +
                pow(0.25 * STop.GetBinContent(i), 2) +
                pow(0.20 * DIBOSON.GetBinContent(i), 2))
            binerror = math.sqrt(binerror2)
            ratiosysterr.SetBinError(i, binerror/h_err.GetBinContent(i))

    ratioleg = rt.TLegend(0.6, 0.88, 0.89, 0.98)
    ratioleg.SetLineColor(0)
    ratioleg.SetShadowColor(0)
    ratioleg.SetTextFont(42)
    ratioleg.SetTextSize(0.09)
    ratioleg.SetBorderSize(1)
    ratioleg.SetNColumns(2)
    #ratioleg.AddEntry(ratiosysterr, "stat + syst", "f")
    ratioleg.AddEntry(ratiostaterr, "stat", "f")

    #For DATA:
    if not NORATIOPLOT:
        canvas.cd()
        #DataMC = rt.TH1F()
        DataMC = data_obs.Clone("DataMC")
        DataMCPre = data_obs
        DataMC.Divide(Stackhist)
        #DataMCPre->Divide(h_prefit)
        DataMC.GetYaxis().SetTitle("Data/Pred.")
        DataMC.GetYaxis().SetTitleSize(0.1)
        DataMC.GetYaxis().SetTitleOffset(0.42)
        DataMC.GetYaxis().SetTitleFont(42)
        DataMC.GetYaxis().SetLabelSize(0.08)
        DataMC.GetYaxis().CenterTitle()
        DataMC.GetXaxis().SetTitle(titleX)
        DataMC.GetXaxis().SetLabelSize(0.1)
        DataMC.GetXaxis().SetTitleSize(0.1)
        DataMC.GetXaxis().SetTitleOffset(1)
        DataMC.GetXaxis().SetTitleFont(42)
        DataMC.GetXaxis().SetTickLength(0.07)
        DataMC.GetXaxis().SetLabelFont(42)
        DataMC.GetYaxis().SetLabelFont(42)

    canvas1_2 = rt.TPad("canvas1_2", "newpad", 0, 0.00, 1, 0.3); canvas1_2.Draw()
    if not NORATIOPLOT: canvas1_2.Draw()
    canvas1_2.cd()
    canvas1_2.Range(-7.862408, -629.6193, 53.07125, 486.5489)
    canvas1_2.SetFillColor(0)
    canvas1_2.SetTicky(1)
    canvas1_2.SetLeftMargin( L/W )
    canvas1_2.SetRightMargin( R/W )
    canvas1_2.SetTopMargin(0.005)
    canvas1_2.SetBottomMargin((B/H)*2.2)
    canvas1_2.SetFrameFillStyle(0)
    canvas1_2.SetFrameBorderMode(0)
    canvas1_2.SetFrameFillStyle(0)
    canvas1_2.SetFrameBorderMode(0)
    canvas1_2.SetLogy(0)

    if not NORATIOPLOT:
        DataMC.GetXaxis().SetRangeUser(XMIN, XMAX)
        DataMC.SetMarkerSize(0.7)
        DataMC.SetMarkerStyle(20)
        DataMC.SetMarkerColor(1)
        DataMCPre.SetMarkerSize(0.7)
        DataMCPre.SetMarkerStyle(20)
        #DataMCPre.SetMarkerColor(rt.kRed)
        #DataMCPre.SetLineColor(rt.kRed)
        DataMC.Draw("P e1")
        ratiostaterr.Draw("e2 same")
        DataMC.Draw("P e1 same")
        DataMC.SetMinimum(-0.2)
        DataMC.SetMaximum(2.1)
        DataMC.GetXaxis().SetNdivisions(508)
        DataMC.GetYaxis().SetNdivisions(505)
        line0 = rt.TLine(XMIN, 1, XMAX, 1)
        line0.SetLineStyle(2)
        line0.Draw("same")
        canvas1_2.SetGridy()
        ratioleg.Draw("same")
        canvas1_2.Update()
        canvas1_2.Draw()
    canvas.Update()
    canvas.Draw()

    if not os.path.exists('plots/'+datestr+'/bbDMPng/'+reg):
        os.makedirs('plots/'+datestr+'/bbDMPng/'+reg)
    if not os.path.exists('plots/'+datestr+'/bbDMPdf/'+reg):
        os.makedirs('plots/'+datestr+'/bbDMPdf/'+reg)
    if not os.path.exists('plots/'+datestr+'/bbDMRoot/'+reg):
        os.makedirs('plots/'+datestr+'/bbDMRoot/'+reg)
    if (ISLOG == 0):
        canvas.SaveAs('plots/'+datestr+'/bbDMPdf/'+reg+'/'+plot+'.pdf')
        canvas.SaveAs('plots/'+datestr+'/bbDMPng/'+reg+'/'+plot+'.png')
        print("Saved. \n")
    if (ISLOG == 1):
        canvas.SaveAs('plots/'+datestr+'/bbDMPdf/'+reg+'/'+plot+'_log.pdf')
        canvas.SaveAs('plots/'+datestr+'/bbDMPng/'+reg+'/'+plot+'_log.png')
        print("Saved. \n")

    fshape = rt.TFile('plots/'+datestr+'/bbDMRoot/'+reg+'/'+plot, "RECREATE");
    fshape.cd();
    #Save root files for datacards
    Stackhist.SetNameTitle("bkgSum", "bkgSum");
    Stackhist.Write();
    DIBOSON.SetNameTitle("DIBOSON", "DIBOSON");
    DIBOSON.Write();
    ZJets.SetNameTitle("ZJets", "ZJets");
    ZJets.Write();
    GJets.SetNameTitle("GJets", "GJets");
    GJets.Write();
    QCD.SetNameTitle("QCD", "QCD");
    QCD.Write();
    STop.SetNameTitle("STop", "STop");
    STop.Write();
    Top.SetNameTitle("TT", "Top");
    Top.Write();
    WJets.SetNameTitle("WJets", "WJets");
    WJets.Write();
    DYJets.SetNameTitle("DYJets", "DYJets");
    DYJets.Write();
    data_obs.SetNameTitle("data_obs", "data_obs");
    data_obs.Write();
    fshape.Write();
    fshape.Close();
    #update the canvas to draw the legend


# In[4]:


dirnames=['']

srblindfactor='1'
srnodata='1'

for dirname in dirnames:

    regions=[]
    PUreg=[]

    if makeMuCRplots:
        regions+=['1mutop1b','1mutop2b','2mu1b','2mu2b','1mu1b','1mu2b']
        PUreg+=['mu_']
    if makeEleCRplots:
        regions+=['1etop1b','1etop2b','2e1b','2e2b','1e1b','1e2b']
        PUreg+=['ele_']
    if makePhoCRplots:
        regions+=['1gamma1b','1gamma2b']
        PUreg+=['pho_']
    if makeQCDCRplots:
        regions+=['QCD1b','QCD2b']
        PUreg+=[]
for reg in regions:
    if reg[0]=='2': makeplot(dirname+"reg_"+reg+"_ZpT",'h_reg_'+reg+'_ZpT_','Z candidate p_{T} (GeV)',0.,800.,reg[-2],1,0,reg)
    if reg[0]=='1': makeplot(dirname+"reg_"+reg+"_WpT",'h_reg_'+reg+'_WpT_','W candidate p_{T} (GeV)',200.,800.,1,1,0,reg)
    makeplot(dirname+"reg_"+reg+"_hadrecoil",'h_reg_'+reg+'_hadrecoil_','Hadronic Recoil (GeV)',200.,1000.,1,1,0,reg)
