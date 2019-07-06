
BASEPATH=~/CERN-DATA/Online/data/data16_13TeV

mkdir correction
cp job_data_correction.py correction
cd correction

command="python job_data_correction.py --etbins 0 20 30 40 50 100000 --etabins 0 0.8 1.37 1.54 2.37 2.5 -r 0.5 0.5 0.2 0.2 -c 15"

run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodA.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodB.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodC.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodD.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodE.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodF.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodG.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodI.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodK.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20
run_jobs.py -i $BASEPATH/user.jodafons.data16_13TeV.periodL.physicsMain.p3013.SelectionData.PhysVal.r0062_GLOBAL -c $command -m -n 20

hadd correction.root *.root
mv correction.root ..
cd ..



