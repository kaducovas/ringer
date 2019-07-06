

# MC15 medium tuning: Using supprt trigger approach from TrigEgammaAnalysisToosl. Probes and Jetc > 15 GeV (Offline)
# For Signal, we uses the LH tuning 2016 05. For background we still using the old LH tuning, but doest matty because,
# we get the veto truth as selction. The reference for pd was adapt from LF pd refs. For Pf we set to 5%.

#runGRIDtuning.py -d user.jodafons.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.medium.npz \
#               -pp user.wsfreund.ppFile_et_eta_bins_indep.pic.gz \
#               -c user.wsfreund.config.nn5to20_sorts10_JackKnife_1by1_inits100_100by100 \
#               -x user.wsfreund.crossValid-JackKnife.pic.gz \
#               -o user.jodafons.nn.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.medium.npz \
#               --cloud US \
#               --long \
#               --site ANALY_BNL_LONG\
#               --eta-bins 0 3 --et-bin 0 4 
#
#

#runGRIDtuning.py -d user.jodafons.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.tight.npz \
#               -pp user.wsfreund.ppFile_et_eta_bins_indep.pic.gz \
#               -c user.wsfreund.config.nn5to20_sorts10_JackKnife_1by1_inits100_100by100 \
#               -x user.wsfreund.crossValid-JackKnife.pic.gz \
#               -o user.jodafons.nn.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.tight.npz \
#               --cloud US \
#               --long \
#               --site ANALY_BNL_LONG\
#               --eta-bins 0 3 --et-bin 0 4 

#runGRIDtuning.py -d user.jodafons.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.Loose.npz \
#               -pp user.wsfreund.ppFile_et_eta_bins_indep.pic.gz \
#               -c user.wsfreund.config.nn5to20_sorts10_JackKnife_1by1_inits100_100by100 \
#               -x user.wsfreund.crossValid-JackKnife.pic.gz \
#               -o user.jodafons.nn.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.Loose.npz \
#               --eta-bins 0 3 --et-bin 0 4 
#               #--cloud US \
#               #--long \
#               #--site ANALY_BNL_LONG\




runGRIDtuning.py -d user.jodafons.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.veryLoose.npz \
               -pp user.wsfreund.ppFile_et_eta_bins_indep.pic.gz \
               -c user.wsfreund.config.nn5to20_sorts10_JackKnife_1by1_inits100_100by100 \
               -x user.wsfreund.crossValid-JackKnife.pic.gz \
               -o user.jodafons.nn.mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.veryLoose.npz \
               --eta-bins 0 --et-bin 0
               #--cloud US \
               #--long \
               #--site ANALY_BNL_LONG\







