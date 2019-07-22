#!/bin/bash

THISPROCESS=$1

WD=$PWD

export SCRAM_ARCH=slc6_amd64_gcc530
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

ls

export X509_USER_PROXY=${PWD}/x509up
export HOME=.

RELEASE=CMSSW_8_0_11
scram p CMSSW $RELEASE
tar xzf 8011.tgz -C $RELEASE

cd $RELEASE
eval `scram runtime -sh`
cd -

python skim.py $@

rm -rf $RELEASE skim.py x509up 8011.tgz local.cfg 
