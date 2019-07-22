#ifndef PandaAnalyzer_h
#define PandaAnalyzer_h

// STL
#include "vector"
#include "map"
#include <string>

// ROOT
#include <TTree.h>
#include <TFile.h>
#include <TMath.h>
#include <TH1D.h>
#include <TH2F.h>
#include <TLorentzVector.h>

#include "AnalyzerUtilities.h"
#include "GeneralTree.h"

#include "CondFormats/BTauObjects/interface/BTagEntry.h"
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"
#include "BTagCalibrationStandalone.h"
// JEC
//#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
//#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
//#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

/////////////////////////////////////////////////////////////////////////////
// some misc definitions

/////////////////////////////////////////////////////////////////////////////
// PandaAnalyzer definition
class PandaAnalyzer {
public :
  // configuration enums
  enum PreselectionBit {
   kMonotop     =(1<<0),
   kMonohiggs   =(1<<2),
   kMonojet     =(1<<3),
   kTriggers    =(1<<4),
   kVBF         =(1<<5)
  };

  enum ProcessType { 
    kNone,
    kZ,
    kW,
    kA,
    kTT,
    kTop, // used for non-ttbar top
    kV, // used for non V+jets W or Z
    kH
  };

  enum TriggerBits {
    kMETTrig       =(1<<0),
    kSingleEleTrig =(1<<1),
    kSinglePhoTrig =(1<<2),
    kSingleMuTrig  =(1<<3)
  };

  //////////////////////////////////////////////////////////////////////////////////////

  PandaAnalyzer();
  ~PandaAnalyzer();
  void Init(TTree *tree, TTree *infotree);
  void SetOutputFile(TString fOutName);
  float getMSDcorr(Float_t puppipt, Float_t puppieta);
  void ResetBranches();
  void Run();
  void Terminate();
  bool PassPreselection();
  bool PassEventFilters();
  bool PassGoodLumis();
  void SetDataDir(const char *s);
  void SetPreselectionBit(PreselectionBit b,bool on=true) {
    if (on) 
      preselBits |= b;
    else 
      preselBits &= ~b;
  }

  // public configuration
  void SetFlag(TString flag, bool b) { flags[flag]=b; }
  bool isData=false;                         // to do gen matching, etc
  int firstEvent=-1;
  int lastEvent=-1;                          // max events to process; -1=>all
  ProcessType processType=kNone;             // determine what to do the jet matching to

private:

  std::map<TString,bool> flags;

  std::map<panda::PGenParticle*,float> genObjects;                      // particles we want to match the jets to, and the 'size' of the daughters
  panda::PGenParticle *MatchToGen(double eta, double phi, double r2, int pdgid=0);    // private function to match a jet; returns NULL if not found
  std::vector<panda::PObject*> matchPhos, matchEles, matchLeps;
  
  // CMSSW-provided utilities
//  JetCorrectorParameters *ak8jec=0;
//  JetCorrectionUncertainty *ak8unc=0;

  void calcBJetSFs(TString readername, int flavor, double eta, double pt, double eff, double uncFactor, double &sf, double &sfUp, double &sfDown);
  BTagCalibration *btagCalib=0;
  BTagCalibration *btagCalib_alt=0;
  BTagCalibration *sj_btagCalib;

  std::map<TString,BTagCalibrationReader*> btagReaders;
  
  // BTagCalibrationReader *hfReader=0, *hfUpReader=0, *hfDownReader=0;
  // BTagCalibrationReader *lfReader=0, *lfUpReader=0, *lfDownReader=0;

  // BTagCalibrationReader *hfReader_alt=0, *hfUpReader_alt=0, *hfDownReader_alt=0;
  // BTagCalibrationReader *lfReader_alt=0, *lfUpReader_alt=0, *lfDownReader_alt=0;

  // BTagCalibrationReader *sj_hfReader=0, *sj_hfUpReader=0, *sj_hfDownReader=0;
  // BTagCalibrationReader *sj_lfReader=0, *sj_lfUpReader=0, *sj_lfDownReader=0;

  // files and histograms containing weights
  TFile *fEleSF=0, *fEleSFTight=0;
  TH2D *hEleVeto, *hEleTight;
  TFile *fMuSF=0, *fMuSFTight=0;
  TH2D *hMuLoose, *hMuTight;
  TFile *fEleSFTrack=0, *fMuSFTrack=0;
  TH1D *hMuTrack; TH2D *hEleTrack;

  TFile *fPU=0;
  TH1D *hPUWeight;

  TFile *fKFactor=0;
  TH1D *hZNLO, *hANLO, *hWNLO;
  TH1D *hZLO,  *hALO,  *hWLO;
  TH1D *hZEWK, *hAEWK, *hWEWK;
  TFile *fEleTrigB, *fEleTrigE, *fPhoTrig, *fEleTrigLow, *fMetTrig;
  TH1D *hEleTrigB, *hEleTrigE, *hPhoTrig, *hMetTrig;
  //TH1D *hEleTrigBUp=0, *hEleTrigBDown=0, *hEleTrigEUp=0, *hEleTrigEDown=0;
  TH2D *hEleTrigLow;

  TFile *MSDcorr;
  TF1* puppisd_corrGEN;
  TF1* puppisd_corrRECO_cen;
  TF1* puppisd_corrRECO_for;

  // IO for the analyzer
  TFile *fOut;   // output file is owned by PandaAnalyzer
  TTree *tOut;
  GeneralTree *gt; // essentially a wrapper around tOut
  TTree *tIn=0;  // input tree to read
  unsigned int preselBits=0;

  // objects to read from the tree
  panda::PEvent *event=0;                        // event object
  panda::VGenParticle *genparts=0;               // gen particle objects
  panda::VFatJet *fatjets=0;                     // CA15 fat jets
  panda::VJet *jets=0;                           // AK4 narrow jets
  panda::VElectron *electrons=0;
  panda::VMuon *muons=0;
  panda::VTau *taus=0;
  panda::VPhoton *photons=0;
  panda::PMET *pfmet=0, *puppimet=0;

  // configuration read from output tree
  std::vector<double> betas;
  std::vector<int> Ns; 
  std::vector<int> orders;

};


#endif

