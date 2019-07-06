
source setup.sh
cmt co Trigger/TrigHypothesis/TrigMultiVarHypo
cmt co Trigger/TrigAnalysis/TrigEgammaEmulationTool
cd Trigger/TrigAnalysis
git clone https://:@gitlab.cern.ch:8443/ringer/TrigEgammaAnalysisTools.git
cd ../..
source compile.sh


