
BASEPATH=~/CERN-DATA/Online/data/data16_13TeV

mkdir probes_distribution
cd probes_distribution/
command="python job_distribution.py -c 15"
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodA.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodB.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodC.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodD.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodE.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodF.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodG.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodI.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodK.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodL.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20

command="python job_distribution.py -c 15 --isMC"
python job_launcher.py -i ~/CERN-DATA/Online/data/mc15_13TeV/user.jodafons.mc15_13TeV.361106.Zee.merge.SelectionZee.PhysVal.r0005_GLOBAL -c $command -m -n 20
hadd probes_distribution.root *.root
mv probes_distribution.root ..
cd ../

mkdir fakes_distribution
cd fakes_distribution

command="python job_distribution.py -c 15 -f"
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodA.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodB.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodC.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodD.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodE.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodF.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodG.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodI.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodK.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20
python job_launcher.py -i $BASEPATH/user.jodafons.data16_13TeV.periodL.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL -c $command -m -n 20

command="python job_distribution.py -c 15 --isMC -f"
python job_launcher.py -i ~/CERN-DATA/Online/data/mc15_13TeV/user.jodafons.mc15_13TeV.423300.JF17.merge.SelectionFakes.PhysVal.r0005_GLOBAL -c $command -m -n 20
hadd fakes_distribution.root *.root
mv fakes_distribution.root ..
cd ../








