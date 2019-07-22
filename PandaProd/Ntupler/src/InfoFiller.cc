#include "PandaProd/Ntupler/interface/InfoFiller.h"

using namespace panda;

InfoFiller::InfoFiller(TString n):
    BaseFiller()
{
  data = new PEvent();
  treename = n;
}

InfoFiller::~InfoFiller(){
  delete data;
}

void InfoFiller::init(TTree *t) {
  t->Branch(treename.Data(),&data,99);
}

int InfoFiller::analyze(const edm::Event& iEvent){
    isData = iEvent.isRealData(); 
    return 0;
}

int InfoFiller::analyzeLumi(const edm::LuminosityBlock &iLumi, TTree *t) {

    iLumi.getByToken( events_token, events_handle);
    if (!isData)
      iLumi.getByToken( weights_token, weights_handle);
    // iLumi.getByToken( putrue_token, putrue_handle);

    unsigned int nE = events_handle->size();
    for (unsigned int iE=0; iE!=nE; ++iE) {
      data->eventNumber = events_handle->at(iE);
      data->lumiNumber = iLumi.id().luminosityBlock();
      data->runNumber = iLumi.id().run(); // could probably do this outside the loop...
      if (!isData)
        data->mcWeight = weights_handle->at(iE);
      else
        data->mcWeight = 1;
      t->Fill();
      hDTotalEvents->Fill(0.5,1);
      hDTotalMCWeight->Fill(0.5,data->mcWeight);
    }

    return 0;
}
