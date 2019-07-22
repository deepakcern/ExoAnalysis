#ifndef PANDA_PFATJET
#define PANDA_PFATJET

#include "PObject.h"
#include "PPFCand.h"
#include "PJet.h"
#include <tuple>

namespace panda
{

  class PFatJet : public PJet
  {
    public:
      PFatJet():
        PJet(),
        tau1(-1),
        tau2(-1),
        tau3(-1),
        mSD(-1),
        htt_mass(-1),
        htt_frec(-1),
       subjets(0)
      { }
    ~PFatJet() { }

    float tau1, tau2, tau3;
    float mSD, tau1SD=-1, tau2SD=-1, tau3SD=-1;
    float htt_mass, htt_frec;

    // beta = .5, 1, 2, 4
    float ecfs[3][4][4]; // [o-1][N-1][beta] = x

    float get_ecf(short o_, short N_, int ib_) const {
      if (o_<1 || o_>3 || N_<1 || N_>4 || ib_<0 || ib_>3) 
        return -1;
      return ecfs[o_-1][N_-1][ib_];
    }
    int set_ecf(int o_, int N_, int ib_, float x_) {
      if (o_<1 || o_>3 || N_<1 || N_>4 || ib_<0 || ib_>3) 
        return 1;
      ecfs[o_-1][N_-1][ib_] = x_;
      return 0;
    }

    VJet *subjets;

    ClassDef(PFatJet,1)
    
  };

  typedef std::vector<PFatJet*> VFatJet;
}
#endif
