import ROOT

f=ROOT.TFile.Open('Output_SkimmedTree.root','READ')

hist = f.Get('h_met_sr2_')
h_total=f.Get('h_total_weight')

total=h_total.Integral()

#cs = 0.201769753605
cs= 1 * 0.588 

print ('CS:  ', cs)
lumi=35900

print ("Before scaling:  ", hist.Integral())
hist.Scale(cs*lumi/total)

print ("After scaling:  ", hist.Integral())

hist.Scale(1/hist.Integral())

c=ROOT.TCanvas()
hist.Draw('hist')
c.SaveAs('new_metFrom_me_norm1.png')
