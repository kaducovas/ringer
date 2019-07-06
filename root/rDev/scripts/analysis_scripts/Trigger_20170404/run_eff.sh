

DATA=../analysis_scripts/Trigger_20170404/data/user.jodafons.data16_13TeV.311244.physicsMain.p3026.HLTMON.21.0.19.20170217.r0002_GLOBAL/user.jodafons.data16_13TeV.311244.physicsMain.p3026.HLTMON.21.0.19.20170217.r0002_GLOBAL.root

echo "eff plots"
python plot_eff.py -o eff-plots -i $DATA --key  "EMU:0:0:rel21,EMU:0:1:v6"
python plot_eff.py -o eff-plots -i $DATA --key  "EMU:0:2:rel21,EMU:0:3:v6"
python plot_eff.py -o eff-plots -i $DATA --key  "EMU:0:4:rel21,EMU:0:6:v6"
python plot_eff.py -o eff-plots -i $DATA --key  "EMU:0:8:rel21,EMU:0:9:v6"
python plot_eff.py -o eff-plots -i $DATA --key  "EMU:0:10:rel21,EMU:0:11:v6"



DATA=../analysis_scripts/Trigger_20170404/data/user.jodafons.data16_13TeV.00310574.physics_EnhancedBias.HLTMON.21.0.19.20170217.r0005_GLOBAL/user.jodafons.data16_13TeV.00310574.physics_EnhancedBias.HLTMON.21.0.19.20170217.r0005_GLOBAL.root

echo "const plots"
python plot_eff.py -o cost-plots -b -i $DATA --key  "EFF:0:0:rel21,EMU:0:1:v6"
python plot_eff.py -o cost-plots -b -i $DATA --key  "EFF:0:2:rel21,EMU:0:3:v6"
python plot_eff.py -o cost-plots -b -i $DATA --key  "EFF:0:4:rel21,EMU:0:6:v6"
python plot_eff.py -o cost-plots -b -i $DATA --key  "EFF:0:8:rel21,EMU:0:9:v6"
python plot_eff.py -o cost-plots -b -i $DATA --key  "EFF:0:10:rel21,EMU:0:11:v6"


DATA=../analysis_scripts/Trigger_20170404/data/user.jodafons.data16_13TeV.311244.physicsMain.p3026.HLTMON.21.0.19.20170217.r0002_GLOBAL/user.jodafons.data16_13TeV.311244.physicsMain.p3026.HLTMON.21.0.19.20170217.r0002_GLOBAL.root

echo "eff plots validation"
python plot_eff.py -o eff-plots-val -i $DATA --key  "EFF:0:0:rel21,EMU:0:0:emulated"
python plot_eff.py -o eff-plots-val -i $DATA --key  "EFF:0:2:rel21,EMU:0:2:emulated"
python plot_eff.py -o eff-plots-val -i $DATA --key  "EFF:0:4:rel21,EMU:0:4:emulated"
python plot_eff.py -o eff-plots-val -i $DATA --key  "EFF:0:8:rel21,EMU:0:8:emulated"
python plot_eff.py -o eff-plots-val -i $DATA --key  "EFF:0:10:rel21,EMU:0:10:emulated"


DATA=../analysis_scripts/Trigger_20170404/data/user.jodafons.data16_13TeV.00310574.physics_EnhancedBias.HLTMON.21.0.19.20170217.r0005_GLOBAL/user.jodafons.data16_13TeV.00310574.physics_EnhancedBias.HLTMON.21.0.19.20170217.r0005_GLOBAL.root

echo "cost plots validation"
python plot_eff.py -o cost-plots-val -b -i $DATA --key  "EFF:0:0:rel21,EMU:0:0:emulated"
python plot_eff.py -o cost-plots-val -b -i $DATA --key  "EFF:0:2:rel21,EMU:0:2:emulated"
python plot_eff.py -o cost-plots-val -b -i $DATA --key  "EFF:0:4:rel21,EMU:0:4:emulated"
python plot_eff.py -o cost-plots-val -b -i $DATA --key  "EFF:0:8:rel21,EMU:0:8:emulated"
python plot_eff.py -o cost-plots-val -b -i $DATA --key  "EFF:0:10:rel21,EMU:0:10:emulated"




