

USER=jodafons
TAG=p0010
INDS_MAIN=data16_13TeV.00284285.physics_Main.merge.AOD.f662_m1453_r8067_p2645 #GRL 2015
CLOUD=US

echo $INDS

pathena dump_trigProbes.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.dump_trigProbes.${TAG} \
--nFilesPerJob=1 \
--cloud=${CLOUD} --long --supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG 

pathena dump_trigElectrons.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.dump_trigElectrons.${TAG} \
--nFilesPerJob=1 \
--cloud=${CLOUD} --long --supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \

pathena run_probesAnalysis.py \
--inDS=${INDS}/ \
--outDS=user.${USER}.${INDS}.probesAnalysis.${TAG} \
--nFilesPerJob=1 \
--cloud=${CLOUD} --long --supStream=EXPERT,SHIFT,run_1,RUNSTAT,DEBUG \










