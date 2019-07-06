

BASEPATH=/home/jodafons/CERN-DATA/Online/data/data16_13TeV


python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodA.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodA.physicsMain.correction.root &> logA_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodB.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodB.physicsMain.correction.root &> logB_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodC.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodC.physicsMain.correction.root &> logC_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodD.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodD.physicsMain.correction.root &> logD_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodE.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodE.physicsMain.correction.root &> logE_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodF.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodF.physicsMain.correction.root &> logF_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodG.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodG.physicsMain.correction.root &> logG_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodI.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodI.physicsMain.correction.root &> logI_correction.log & 
python jobs/job_data16_13TeV_correction.py -i $BASEPATH/user.jodafons.data16_13TeV.periodK.physicsMain.p3013.SelectionData.PhysVal.r0004_GLOBAL \
  -o data16_13TeV.periodK.physicsMain.correction.root &> logK_correction.log & 










