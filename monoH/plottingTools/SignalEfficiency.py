from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend,gROOT,TGraph
from ROOT import kBlack, kBlue, kRed
from array import array
import os

# gStyle.SetErrorX(0.5)
gStyle.SetFrameLineWidth(3)
gStyle.SetOptTitle(0)
# gStyle.SetOptStat(0)
# gStyle.SetLegendBorderSize(0)
# gStyle.SetFillColor(2)
# gStyle.SetLineWidth(1)
# gStyle.SetHistFillStyle(2)
gROOT.SetBatch(1)


def AddText(txt):
    texcms = TLatex(-20.0, 50.0, txt)
    texcms.SetNDC()
    texcms.SetTextAlign(12)
    texcms.SetX(0.2)
    texcms.SetY(0.8)
    texcms.SetTextSize(0.05)
    texcms.SetTextColor(4)
    texcms.SetTextSizePixels(32)
    return texcms


def SetCanvas():

    # CMS inputs
    # -------------
    H_ref = 1000;
    W_ref = 1000;
    W = W_ref
    H  = H_ref

    T = 0.08*H_ref
    B = 0.21*H_ref
    L = 0.12*W_ref
    R = 0.08*W_ref
    # --------------

    c1 = TCanvas("c2","c2",0,0,2000,1500)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetGridy()
    c1.SetGridx()
    c1.SetLogy(1)
    return c1


def setFrame():

    frame = TH1F("frame","",1000,50,500);
    # frame.SetMinimum(1);
    # frame.SetMaximum(50);
    frame.SetDirectory(0);
    frame.SetStats(0);
    frame.GetXaxis().SetTitle("m_{A} (GeV)");
    frame.GetXaxis().SetTickLength(0.02);
    frame.GetXaxis().SetLabelSize(0.03);
    frame.GetYaxis().SetTitle("Efficiency");
    frame.GetYaxis().SetMoreLogLabels();
    frame.GetYaxis().SetLabelSize(0.3);
    frame.Draw(" ");


def getLegend():
    legend=TLegend(.10,.79,.47,.89)
    legend.SetTextSize(0.038)
    legend.SetFillStyle(0)

    return legend


def getLatex():
    latex =  TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    latex.SetTextAlign(11);
    return latex



def getGraph(n,x,y):

     gr =TGraph(n,x,y)
     gr.SetFillColor(4)
     gr.SetFillStyle(3004)
     gr.SetLineColor(4)
     gr.SetLineWidth(-603)
     # gr.SetMarkerStyle(20)
     # gr.SetMarkerSize(1.5)
     # gr.SetLineColor(1)
     # gr.SetLineWidth(1)
     # gr.SetMarkerColor(1)
     gr.GetYaxis().SetTitle("Efficiency")
     gr.GetXaxis().SetTitle("m_{A} [GeV]")
     # gr.SetTitle("")
     return gr

SignalPath = '/Users/dekumar/MEGA/Fullwork/2017_Plotting/rootFiles_Signal'
SignalFiles = sorted([SignalPath+'/'+fl for fl in os.listdir(SignalPath) if '.root' in fl])

# mass =[]
# eff = []

mass, eff = array( 'd' ), array( 'd' )

for infile in SignalFiles:
    print ('infile',infile)
    fin       =   TFile(infile,"READ")
    rootFile = infile.split('/')[-1]
    ma=rootFile.split('_')[11]
    mA=rootFile.split('_')[9]
    mass.append(int(mA))
    temp = fin.Get('h_reg_SR_MET')
    selEvent = temp.Integral()
    h_total = fin.Get('h_total_mcweight')
    totalEvents = h_total.Integral()

    eff.append(float(selEvent)/float(totalEvents))

c = SetCanvas() #TCanvas("c","test",0,0,700,700);
c.SetTickx();
c.SetTicky();
c.SetGridx();
c.SetGridy();
setFrame()

mass, eff = zip(*sorted(zip(mass, eff)))
mass = array('d',mass)
eff  = array('d',eff)
gr=getGraph(len(mass),mass,eff)


gr.Draw()
latex=getLatex()
latex.DrawLatex(0.11, 0.93, " 2HDM+a                                                 boosted      monoHbb")
txt = '#splitline{tan#beta=1, sin#theta=0.35}{m_{a}=150 GeV}'
texcms = AddText(txt)
texcms.Draw("same")

c.SaveAs('efficiency_log.png')
c.SaveAs('efficiency_log.pdf')
