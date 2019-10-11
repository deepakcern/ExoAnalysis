import os, sys
#//--------------------------------------------------------------------------------------
def getXsec(samplename):
    Xsec = 1.0
    if 'DYJetsToLL_M-50_HT-100to200'   in samplename: Xsec  = 147.4 #161.1
    if 'DYJetsToLL_M-50_HT-200to400'   in samplename: Xsec  = 40.99 #48.66
    if 'DYJetsToLL_M-50_HT-400to600'   in samplename: Xsec  = 5.678 #6.968
    if 'DYJetsToLL_M-50_HT-600to800'   in samplename: Xsec  = 1.367 #1.743
    if 'DYJetsToLL_M-50_HT-800to1200'  in samplename: Xsec  = 0.6304 #0.8052
    if 'DYJetsToLL_M-50_HT-1200to2500' in samplename: Xsec  = 0.1514 #0.1933
    if 'DYJetsToLL_M-50_HT-2500toInf'  in samplename: Xsec  = 0.003565 #0.003468

    if 'ZJetsToNuNu_HT-100to200'   in samplename: Xsec  = 280.35 #302.8
    if 'ZJetsToNuNu_HT-200to400'   in samplename: Xsec  = 77.67 #92.59
    if 'ZJetsToNuNu_HT-400to600'   in samplename: Xsec  = 10.73 #13.18
    if 'ZJetsToNuNu_HT-600to800'   in samplename: Xsec  = 2.559 #3.257
    if 'ZJetsToNuNu_HT-800to1200'  in samplename: Xsec  = 1.1796 #1.49
    if 'ZJetsToNuNu_HT-1200to2500' in samplename: Xsec  = 0.28833 #0.3419
    if 'ZJetsToNuNu_HT-2500toInf'  in samplename: Xsec  = 0.006945 #0.005146

    if 'WJetsToLNu_HT-100to200'   in samplename: Xsec  = 1345.0 #1395.0
    if 'WJetsToLNu_HT-200to400'   in samplename: Xsec  = 359.7 #407.9
    if 'WJetsToLNu_HT-400to600'   in samplename: Xsec  = 48.91 #57.48
    if 'WJetsToLNu_HT-600to800'   in samplename: Xsec  = 12.05 #12.87
    if 'WJetsToLNu_HT-800to1200'  in samplename: Xsec  = 5.501 #5.366
    if 'WJetsToLNu_HT-1200to2500' in samplename: Xsec  = 1.329 #1.074
    if 'WJetsToLNu_HT-2500toInf'  in samplename: Xsec  = 0.03216 #0.008001

    if 'GJets_HT-40To100'    in samplename: Xsec  = 20790 #18700.0
    if 'GJets_HT-100To200'   in samplename: Xsec  = 9238 #8640.0
    if 'GJets_HT-200To400'   in samplename: Xsec  = 2305 #2185.0
    #if 'GJets_HT-400To600'   in samplename: Xsec  =
    if 'GJets_HT-600ToInf'   in samplename: Xsec  = 93.46 #85.31

    if 'QCD_HT500To700'    in samplename: Xsec  = 32100 #29980.0
    if 'QCD_HT700to1000'   in samplename: Xsec  = 6831 #6334.0
    if 'QCD_HT1000to1500'  in samplename: Xsec  = 1207#1088.0
    if 'QCD_HT1500to2000'  in samplename: Xsec  = 119.9#99.11
    if 'QCD_HT2000toInf'   in samplename: Xsec  = 25.24 #20.23

    if 'TTToHadronic'      in samplename: Xsec = 687.1*0.46
    if 'TTToSemiLeptonic'  in samplename: Xsec = 687.1*0.45
    if 'TTTo2L2Nu'         in samplename: Xsec = 687.1*0.09

    if 'ST_s-channel_4f_leptonDecays' in samplename: Xsec = 3.74
    if 'ST_t-channel_antitop_4f'      in samplename: Xsec = 67.91
    if 'ST_t-channel_top_4f'          in samplename: Xsec = 113.3
    if 'ST_tW_antitop_5f'             in samplename: Xsec = 34.97
    if 'ST_tW_top_5f'                 in samplename: Xsec = 34.91

    if 'ZZ_TuneCP5_13TeV' in samplename: Xsec = 12.14
    if 'WW_TuneCP5_13TeV' in samplename: Xsec = 75.8
    if 'WZ_TuneCP5_13TeV' in samplename: Xsec = 27.6

    if 'ggZH_HToBB_ZToNuNu_M125'  in samplename: Xsec = 0.01222
    if 'ggZH_HToBB_ZToLL_M125'    in samplename: Xsec = 0.006185
    if 'WminusH_HToBB_WToQQ_M125' in samplename: Xsec = 0.3654
    if 'WplusH_HToBB_WToLNu_M125' in samplename: Xsec = 0.2819
    if 'ZH_HToBB_ZToLL_M125'      in samplename and 'ggZH_HToBB_ZToLL_M125' not in samplename:   Xsec = 0.07924
    if 'ZH_HToBB_ZToNuNu_M125'    in samplename and 'ggZH_HToBB_ZToNuNu_M125' not in samplename: Xsec = 0.1565


    return Xsec
