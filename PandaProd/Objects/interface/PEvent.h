#ifndef PANDA_PEVENTINFO
#define PANDA_PEVENTINFO

#include <TObject.h>
#include <TClonesArray.h>


namespace panda
{
  class PEvent : public TObject
  {
    public:
      PEvent():
        runNumber(0),
        lumiNumber(0),
        eventNumber(0),
        isData(false),
        npv(0),
        mcWeight(-1)
        {
          metfilters = new std::vector<bool>;
          tiggers = new std::vector<bool>;
	  mcWeights_syst = new std::vector<float>;
        }
	~PEvent(){ delete metfilters; delete tiggers; delete mcWeights_syst;}
    
    int runNumber, lumiNumber;
    ULong64_t eventNumber;
    bool isData;
    int npv;
    float mcWeight;
    std::vector<bool> *metfilters, *tiggers; std::vector<float> *mcWeights_syst;
    ClassDef(PEvent,1)
  };
}
#endif
