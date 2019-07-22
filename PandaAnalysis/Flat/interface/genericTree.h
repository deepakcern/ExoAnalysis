#ifndef GENERICTREE
#define GENERICTREE 1

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TLorentzVector.h"
#include "TClonesArray.h"

#define NMAX 8
#define NGENMAX 100

class genericTree {
  public:
    genericTree() {};
    virtual ~genericTree() {};
    TTree *treePtr;
    virtual void ReadTree(TTree *t)=0;
    virtual void WriteTree(TTree *t)=0;
};

#endif
