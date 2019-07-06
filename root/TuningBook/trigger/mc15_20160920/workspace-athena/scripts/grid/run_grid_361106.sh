

USER=jodafons
TAG=p0010

INDS=mc15_13TeV.361106.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.merge.AOD.e3601_s2876_r7917_r7676
CLOUD=US


echo $INDS

pathena dump_trigProbes.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.dump.trigPB.${TAG} \
--nEventsPerJob=500 \
--excludedSite=ANALY_BNL_SHORT\
--cloud=${CLOUD} \
--long \
--supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG 
##--goodRunListXML=${GRL}

pathena dump_trigElectrons.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.dump.trigEL.${TAG} \
--nEventsPerJob=500 \
--excludedSite=ANALY_BNL_SHORT\
--cloud=${CLOUD} \
--long \
--supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \
#--goodRunListXML=${GRL}

pathena run_probesAnalysis.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.mon.trigPB.${TAG} \
--nEventsPerJob=500 \
--cloud=${CLOUD} \
--long \
--supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \
##--goodRunListXML=${GRL}










