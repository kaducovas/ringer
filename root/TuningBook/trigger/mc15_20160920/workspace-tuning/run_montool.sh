
TUNEDFILE=/afs/cern.ch/work/j/jodafons/public/Online/tuning/mc15_201609XX/nnstat/user.jodafons.nnstat.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.tight.npz


REFDATA=/afs/cern.ch/work/j/jodafons/public/Online/tuning/mc15_201609XX/data/mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.tight.npz

OUTPUT=report.user.jodafons.nnstat.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.tight.npz


mkdir $OUTPUT
cd $OUTPUT
crossValStatMonAnalysis.py -f $TUNEDFILE -r $REFDATA --doBeamer --grid -o $OUTPUT #--debug 
cd ../

