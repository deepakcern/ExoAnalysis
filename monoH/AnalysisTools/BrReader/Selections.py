import os

def getSel(nEle,nMu,nTau,nBjets,nPho,nFatJet,isTightMuon,MuIso,eleIsPassTight,pfMet,nJets,dPhi_jet_MET_Cond,dPhi_jet_Wmurecoil_Cond,dPhi_jet_Werecoil_Cond,dPhi_jet_Zeerecoil_Cond,dPhi_jet_Zmumurecoil_Cond,ZeeMass,ZmumuMass,N2DDT,WenuRecoil,WmunuRecoil,ZeeRecoil,ZmumuRecoil):
    cuts ={}
    baseline       = nJets < 2 and nTau+nPho==0 and nFatJet==1# and N2DDT < 0
    #print ('baseline', baseline)
    cuts['signal'] = baseline and  dPhi_jet_MET_Cond  and nMu+nEle==0 and nBjets==0 and pfMet > 200.0
    cuts['tm']     = False
    cuts['te']     = False
    cuts['wmn']    = False
    cuts['wen']    = False
    cuts['zee']    = False
    cuts['zmm']    = False
    if nEle==1 and nMu==0:
        cuts['te']         = baseline and nBjets==1 and dPhi_jet_Werecoil_Cond > 0.4 and nMu==0 and nEle==1 and eleIsPassTight[0] and WenuRecoil > 200.0 and pfMet > 50
        cuts['wen']        = baseline and nBjets==0 and dPhi_jet_Werecoil_Cond > 0.4 and nMu==0 and nEle==1 and eleIsPassTight[0] and WenuRecoil > 200.0 and pfMet > 50
    if nEle==0 and nMu==1:
        cuts['tm']         = baseline and nBjets==1 and dPhi_jet_Wmurecoil_Cond > 0.4 and nEle==0 and nMu==1 and isTightMuon[0] and MuIso[0]<0.15 and WmunuRecoil > 200.0 and pfMet > 50.
        cuts['wmn']        = baseline and nBjets==0 and dPhi_jet_Wmurecoil_Cond > 0.4 and nEle==0 and nMu==1 and isTightMuon[0] and MuIso[0]<0.15 and WmunuRecoil > 200.0 and pfMet > 50.
    if nEle==2 and nMu==0:
        cuts['zee']        = baseline and nBjets==0 and dPhi_jet_Zeerecoil_Cond  and nMu==0 and nEle==2 and (eleIsPassTight[0] or eleIsPassTight[1]) and ZeeRecoil > 200.0 and ZeeMass > 60.0 and ZeeMass<120.0
    if nEle==0 and nMu==2:
        cuts['zmm']        = baseline and nBjets==0 and dPhi_jet_Zmumurecoil_Cond and nEle==0 and nMu==2 and ((isTightMuon[0] and MuIso[0]<0.15) or (isTightMuon[1] and MuIso[1]<0.15)) and ZmumuRecoil>200. and ZmumuMass>60.0 and ZmumuMass<120.0

    return cuts

