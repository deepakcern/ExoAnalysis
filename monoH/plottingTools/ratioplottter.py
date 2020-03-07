from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend
from ROOT import kBlack, kBlue, kRed
from array import array


f = TFile.Open('SingleMuon_combined_v3.root')
fout = TFile('TriggerEff_MET2017_R.root','recreate')
gStyle.SetFrameLineWidth(3)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetFillColor(2)
gStyle.SetLineWidth(1)
gStyle.SetHistFillStyle(2)

#bins=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,160,170,180,190,200,220,240,260,280,300,350,400,500,600,700,800,900,1000,1200,1500]

bins=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,160,170,180,190,200,220,240,260,280,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200]#,1300,1400,1500]


def setHistStyle(h_temp2,bins,name):

    h_temp=h_temp2.Rebin(len(bins)-1,"h_temp",array('d',bins))
    h_temp.SetLineWidth(1)
    #h_temp.SetBinContent(len(bins)-1,h_temp.GetBinContent(len(bins)-1)+h_temp.GetBinContent(len(bins))) #Add overflow bin content to last bin
    #h_temp.SetBinContent(len(bins),0.)
    #h_temp.GetXaxis().SetRangeUser(0,1500)
    #h_temp.SetMarkerColor(kBlack);
    h_temp.SetMarkerStyle(2);
    #h_temp.SetMarkerSize(5);
    h_temp.SetTitle(name)
    h_temp.SetName(name)
    return h_temp

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

    c1 = TCanvas("c2","c2",0,0,800,800)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    #c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.SetGridy()
    c1.SetGridx()
    return c1

def createRatio(h1, h2):
     h3 = h1.Clone("h3")
     h3.SetLineColor(kBlack)
     h3.SetMarkerStyle(20)
     h3.SetTitle("")
     h3.SetMinimum(0.1)
     h3.SetMaximum(1.35)

     # Set up plot for markers and errors
     h3.Sumw2()
     h3.SetStats(0)
     h3.Divide(h2)

     # Adjust y-axis settings
     y = h3.GetYaxis()
     y.SetTitle("Trigger efficiency ")
     # y.SetNdivisions(505)
     # y.SetTitleSize(20)
     # y.SetTitleFont(43)
     # y.SetTitleOffset(1.55)
     # y.SetLabelFont(43)
     # y.SetLabelSize(15)

     # Adjust x-axis settings
     x = h3.GetXaxis()
     x.SetTitleSize(20)
     x.SetTitleFont(43)
     x.SetTitleOffset(4.0)
     x.SetLabelFont(43)
     x.SetLabelSize(15)
     x.SetRangeUser(0,100)

     return h3


def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2

def getLegend():
    legend=TLegend(.50,.39,.87,.49)
    legend.SetTextSize(0.038)

    return legend

def getLatex():
    latex =  TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    latex.SetTextAlign(11);
    return latex


def combineHist(hists,leg_label,leg):

    myhists=[]
    for i in range(len(hists)):
        print (hists[i])
        myhists.append(f.Get(hists[i]))
    for i in range(len(myhists)):
        if i==0:
            myhists[i].SetXTitle("Recoil [GeV]")
            myhists[i].SetYTitle("Events")
            myhists[i].Rebin(20)
            #myhists[i].setHistStyle(hists[i],bins)
            myhists[i].SetLineColor(i+1)
            myhists[i].SetLineWidth(3)
            myhists[i].GetXaxis().SetRangeUser(0,1200)
            leg.AddEntry(myhists[i],leg_label[i],"L")
            myhists[i].Draw('hist')
        else:
            myhists[i].SetXTitle("Recoil [GeV]")
            myhists[i].SetYTitle("Events")
            myhists[i].Rebin(20)
            #myhists[i].setHistStyle(hists[i],bins)
            myhists[i].SetLineColor(i+1)
            myhists[i].SetLineWidth(3)
            myhists[i].GetXaxis().SetRangeUser(0,1500)
            leg.AddEntry(myhists[i],leg_label[i],"L")
            myhists[i].Draw('hist same')


def getGraph(h1,h2,col,name):
    gr=TGraphAsymmErrors(h1,h2)
    gr.GetXaxis().SetRangeUser(0,1200)
    #gr.GetYaxis().SetRangeUser(0.8,1.02)
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(1)
    gr.SetMarkerColor(col)
    gr.SetLineColor(col)
    gr.GetYaxis().SetTitle("Trigger Efficiency")
    gr.GetXaxis().SetTitle("Recoil [GeV]")
    gr.SetTitle(name)
    gr.SetName(name)
    return gr

def ratioplot():
     # create required parts

     leg=getLegend()
     latex=getLatex()
     c=SetCanvas()


     h1=f.Get('h_num_WlnuRecoil_R')
     h1=setHistStyle(h1,bins,'h_num_WlnuRecoil_R')
     h2=f.Get('h_den_WlnuRecoil_R')
     h2=setHistStyle(h2,bins,'h_den_WlnuRecoil_R')

     h3=f.Get('h_num_ZllRecoil_R')
     h3=setHistStyle(h3,bins,'h_num_ZllRecoil_R')
     h4=f.Get('h_den_ZllRecoil_R')
     h4=setHistStyle(h4,bins,'h_den_ZllRecoil_R')

     gr1 = getGraph(h1,h2,2,'Wmunu')
     gr2 = getGraph(h3,h4,3,'Zmumu')

     #h3 = createRatio(h1, h2)
     histogram_base = TH1F("histogram_base", "", 1000, 0, 1200.)
     # histogram_base.SetTitle("")
     # histogram_base.SetStats(0)
     # histogram_base.SetMarkerSize(2)
     #histogram_base.SetMinimum(0.0)
     histogram_base.GetYaxis().SetRangeUser(0,1.02)
     # histogram_base.GetXaxis().SetRangeUser(0,1200)
     # # histogram_base.SetMaximum(1.2)
     histogram_base.GetXaxis().SetTitle("Recoil [GeV]")
     histogram_base.GetYaxis().SetTitle("Efficiency")
     #histogram_base=setHistStyle(histogram_base,bins)


     histogram_base.Draw("HIST")
    # print ("ratio",ratio )
     # c, pad1, pad2 = createCanvasPads()
     #
     # # draw everything
     # pad1.cd()
     # h1.Draw()
     # h2.Draw("same")
     # to avoid clipping the bottom zero, redraw a small axis
     # h1.GetYaxis().SetLabelSize(0.0)
     # axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
     # axis.SetLabelFont(43)
     # axis.SetLabelSize(15)
     # axis.Draw()
     # pad2.cd()
     gr1.Draw('P')
     gr2.Draw('P same')
     leg.AddEntry(gr1,'W #rightarrow #mu#nu','PEL')
     leg.AddEntry(gr2,'Z #rightarrow #mu#mu','PEL')
     latex.DrawLatex(0.1, 0.93, "Trigger Efficiency in 2017 Single Muon")
     xmin=0.0
     line = TLine(max(xmin,histogram_base.GetXaxis().GetXmin()),1,1200,1)
     line.SetLineColor(1)
     line.SetLineWidth(1)
     line.SetLineStyle(7)
     line.Draw()
     leg.Draw()
     #h3.Draw('pl')
     c.SaveAs('Resolved_full.pdf')
     c.SaveAs('Resolved_full.png')
     fout.cd()
     gr1.Write()
     gr2.Write()
     fout.Write()

     # c.SaveAs("triggerTurnOn_WRecoil_B.pdf")
     # c.SaveAs("triggerTurnOn_WRecoil_B.root")

if __name__ == "__main__":
     ratioplot()
