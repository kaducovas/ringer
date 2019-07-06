

BASEPATH=/home/jodafons/CERN-DATA/Online/data/data16_13TeV


python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodA.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodA.physicsMain.histos.root &> logA.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodB.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodB.physicsMain.histos.root &> logB.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodC.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodC.physicsMain.histos.root &> logC.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodD.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodD.physicsMain.histos.root &> logD.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodE.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodE.physicsMain.histos.root &> logE.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodF.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodF.physicsMain.histos.root &> logF.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodG.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodG.physicsMain.histos.root &> logG.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodI.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodI.physicsMain.histos.root &> logI.log & 
python jobs/job_data16_13TeV_eventLooper.py -i $BASEPATH/user.jodafons.data16_13TeV.periodK.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodK.physicsMain.histos.root &> logK.log & 










