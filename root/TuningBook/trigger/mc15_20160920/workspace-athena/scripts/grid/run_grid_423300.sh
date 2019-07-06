

USER=jodafons
TAG=p0010
INDS=mc15_13TeV.423300.Pythia8EvtGen_A14NNPDF23LO_perf_JF17.merge.AOD.e3848_s2876_r7917_r7676
CLOUD=US

echo $INDS

#pathena dump_trigProbes.py \
#--inDS=${INDS}/ \
#--outDS=user.${USER}.${INDS}.dump_trigProbes.${TAG} \
#--nFilesPerJob=1 \
#--cloud=US --long --supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG 
#--goodRunListXML=${GRL}

pathena dump_trigElectrons.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.dump.trigEL.${TAG} \
--excludedSite=ANALY_MWT2_SL6,ANALY_BNL_SHORT \
--cloud=${CLOUD} \
--long \
--supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \
--nEventsPerJob=500
##--goodRunListXML=${GRL}

#pathena run_probesAnalysis.py \
#--inDS=${INDS}/ \
#--outDS=user.${USER}.${INDS}.probesAnalysis.${TAG} \
#--nFilesPerJob=1 \
#--cloud=${CLOUD} --long --supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \
##--goodRunListXML=${GRL}

pathena run_backgroundAnalysis.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.mon.trigPB.${TAG} \
--nFilesPerJob=1 \
--excludedSite=ANALY_MWT2_SL6,ANALY_BNL_SHORT \
--cloud=${CLOUD} \
--long \
--supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \
--nEventsPerJob=500
#--goodRunListXML=${GRL}










