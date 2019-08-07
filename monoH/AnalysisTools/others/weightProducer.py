import numpy as np

def getEleTrigSF(pt,eta):
    matrix = np.loadtxt("SFs/electron_Trigger_eleTrig.txt")
    pT_range=[10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0, 200.0]
    Eta_range=[-2.5, -2.0, -1.566, -1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5]
    if pt > pT_range[-1]:pt = pT_range[-1]-1.0

    if eta >= Eta_range[-1]:eta = Eta_range[-2]
    if eta <= Eta_range[0]:eta = Eta_range[1]

    binxi=sorted([i for i, j in enumerate(pT_range) if j<=pt])[-1]
    binyj=sorted([i for i, j in enumerate(Eta_range) if j<=eta])[-1]
    print ([j for i, j in enumerate(Eta_range) if j<=eta][-1])


    return matrix[binyj,binxi])


def getElelooseIDSF(pt,eta):
    matrix = np.loadtxt("SFs/electron_Loose_ID_SFs_egammaEffi_txt_EGM2D.txt")
    pT_range=[10.0, 20.0, 35.0, 50.0, 90.0, 150.0, 500.0]
    Eta_range=[-2.5, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, 2.5]
    if pt > pT_range[-1]:pt = pT_range[-1]-1.0

    if eta >= Eta_range[-1]:eta = Eta_range[-2]
    if eta <= Eta_range[0]:eta = Eta_range[1]

    binxi=sorted([i for i, j in enumerate(pT_range) if j<=pt])[-1]
    binyj=sorted([i for i, j in enumerate(Eta_range) if j<=eta])[-1]
    print ([j for i, j in enumerate(Eta_range) if j<=eta][-1])

    return matrix[binyj,binxi])


def getEleTightIDSF(pt,eta):
    matrix = np.loadtxt("SFs/electron_Tight_ID_SFs_egammaEffi_txt_EGM2D.txt")

    pT_range=[10.0, 20.0, 35.0, 50.0, 90.0, 150.0, 500.0]
    Eta_range=[-2.5, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, 2.5]
    if pt > pT_range[-1]:pt = pT_range[-1]-1.0

    if eta >= Eta_range[-1]:eta = Eta_range[-2]
    if eta <= Eta_range[0]:eta = Eta_range[1]

    binxi=sorted([i for i, j in enumerate(pT_range) if j<=pt])[-1]
    binyj=sorted([i for i, j in enumerate(Eta_range) if j<=eta])[-1]
    print ([j for i, j in enumerate(Eta_range) if j<=eta][-1])

    return matrix[binyj,binxi])


def getEleRecoLowSF(pt,eta):
    matrix = np.loadtxt("SFs/electron_Reco_SFs_egammaEffi_txt_EGM2D_ptlt_20.txt")
    pT_range=[10.0, 20.0]
    Eta_range=[-2.5, -2.0, -1.566, -1.444, -1.0, 0.0, 1.0, 1.444, 1.566, 2.0, 2.5]
    if pt > pT_range[-1]:pt = pT_range[-1]-1.0

    if eta >= Eta_range[-1]:eta = Eta_range[-2]
    if eta <= Eta_range[0]:eta = Eta_range[1]

    binxi=sorted([i for i, j in enumerate(pT_range) if j<=pt])[-1]
    binyj=sorted([i for i, j in enumerate(Eta_range) if j<=eta])[-1]
    print ([j for i, j in enumerate(Eta_range) if j<=eta][-1])


    return matrix[binyj,binxi])

def getEleRecoHighSF(pt,eta):
    matrix = np.loadtxt("SFs/electron_Reco_SFs_egammaEffi_txt_EGM2D.txt")
    pT_range=[25.0, 500.0]
    Eta_range=[-2.5, -2.45, -2.4, -2.3, -2.2, -2.0, -1.8, -1.63, -1.566, -1.444, -1.2, -1.0, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 1.0, 1.2, 1.444, 1.566, 1.63, 1.8, 2.0, 2.2, 2.3, 2.4, 2.45, 2.5]

    if pt > pT_range[-1]:pt = pT_range[-1]-1.0

    if eta >= Eta_range[-1]:eta = Eta_range[-2]
    if eta <= Eta_range[0]:eta = Eta_range[1]

    binxi=sorted([i for i, j in enumerate(pT_range) if j<=pt])[-1]
    binyj=sorted([i for i, j in enumerate(Eta_range) if j<=eta])[-1]
    print ([j for i, j in enumerate(Eta_range) if j<=eta][-1])


    return matrix[binyj,binxi])
