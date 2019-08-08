import ROOT as ROOT
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad, TFile, TGraphAsymmErrors,TLatex,TLine,gStyle,TLegend,TH2D

inputFile = TFile('electron_Trigger_eleTrig.root', 'READ')

hist=inputFile.Get('hEffEtaPt')#'hEffEtaPt')

xShift = hist.GetXaxis().GetBinWidth(1)/2.
yShift = hist.GetYaxis().GetBinWidth(1)/2.

Eta_range=[]
pT_range=[]
Eta_rangeDone=False
pT_rangeDone=False

values=[]
for i in range(1,hist.GetXaxis().GetNbins()+1):
    xlow  = hist.GetXaxis().GetBinLowEdge(i)#+xShift
    xhigh = hist.GetXaxis().GetBinUpEdge(i)#-xShift
    value=[]
    if not Eta_rangeDone:
        if i == hist.GetXaxis().GetNbins():
            Eta_range.append(xlow)
            Eta_range.append(xhigh)
            Eta_rangeDone=True
        else:Eta_range.append(xlow)
    for j in range(1,hist.GetYaxis().GetNbins()+1):
        ylow  = hist.GetYaxis().GetBinLowEdge(j)#+yShift
        yhigh = hist.GetYaxis().GetBinUpEdge(j)#-yShift
        if not pT_rangeDone:
            if j == hist.GetYaxis().GetNbins():
                pT_range.append(ylow)
                pT_range.append(yhigh)
                pT_rangeDone=True
            else:pT_range.append(ylow)

        value.append(hist.GetBinContent(i,j))
    values.append(value)

print (Eta_range)
print (pT_range)
#print ('lenpT',len(pT_range))
#print ('lenEta',len(Eta_range))
# print (values)

mat=np.matrix(values)
#
# print (mat)
np.savetxt("electron_Trigger_eleTrig.txt", mat)
