
#basePath     = '/afs/cern.ch/work/j/jodafons/public/Online/tuning/201609XX/data/data16_13TeV.e24_lhmedium_nod0_iloose'
#basePath     = '/afs/cern.ch/work/j/jodafons/public/Online/tuning/201609XX/data/data16_13TeV.e28_lhtight_nod0_iloose'
basePath     = '/afs/cern.ch/work/j/jodafons/public/Online/tuning/mc15_201609XX/data'

sgnInputFile = 'probes'
#sgnInputFile = 'electrons'
bkgInputFile = 'background'

#outputFile   = 'data16_13TeV.sgn_probes.284285.refAcceptAll.bkg_enhancedBias.298967.302956.refAcceptAll.l120.l219.ef24.e24_lhmedium_nod0_iloose'
#outputFile   = 'data16_13TeV.sgn_electron.284285.refLHTight.bkg_enhancedBias.298967.302956.refAcceptAll.l120.l219.ef24.e24_lhtmedium_nod0_iloose'
#outputFile   = 'data16_13TeV.sgn_electron.284285.refLHTight.bkg_enhancedBias.298967.302956.refAcceptAll.l122.l223.ef28.e28_lhttight_nod0_iloose'
#outputFile   = 'data16_13TeV.sgn_probes.284285.refAcceptAll.bkg_enhancedBias.298967.302956.refAcceptAll.l122.l223.ef28.e28_lhtight_nod0_iloose'
outputFile   = 'mc15_13TeV.sgn_probes.361106.refAcceptAll.bkg_JF17.423300.vetoTruth.l120.l219.ef23.e23_lhmedium_nod0_iloose'
#outputFile   = 'mc15_13TeV.sgn_probes.361106.refAcceptAll.bkg_JF17.423300.vetoTruth.l122.l223.ef28.e28_lhtight_nod0_iloose'
#outputFile   = 'mc15_13TeV.sgn_electron.361106.refLH.bkg_JF17.423300.refLH.l120.l219.ef24.e24_lhmedium_nod0_iloose'


treePath     = ['HLT/Egamma/Expert/HLT_e24_lhmedium_nod0_iloose/probes',
                'HLT/Egamma/Expert/HLT_e24_lhmedium_nod0_iloose/trigger']

#treePath     = ['HLT/Egamma/Expert/HLT_e28_lhtight_nod0_iloose/probes',
#                'HLT/Egamma/Expert/HLT_e28_lhtight_nod0_iloose/trigger']


#basePath      = '/dynamic_data'
#sgnInputFile  = 'user.jodafons.mc14_13TeV.147406.PowhegPythia8_AZNLO_Zee.recon.RDO.rel20.7.3.6.e3059_s1982_s2008_r5993_reco01_01_PhysVal'
#bkgInputFile  = 'user.jodafons.mc14_13TeV.129160.Pythia8_AU2CTEQ6L1_perf_JF17.recon.RDO.rel20.7.3.6.e3084_s2044_s2008_r5988.reco01_01_PhysVal'
#treePath      = ['HLT/Egamma/TPNtuple/Ntuple/HLT_e28_lhtight_nod0_iloose',
#                 'HLT/Egamma/Ntuple/Ntuple/HLT_e28_lhtight_nod0_iloose']
#outputFile    = 'mc14_13TeV.sgn_probes.14706.refAcceptAll.bkg_JF17.129160.refTruth.l122.l223.ef28.e28_lhtight_nod0_iloose'
#outputFile    = 'mc14_13TeV.sgn_electrons.14706.refLHMedium.bkg_JF17.129160.refLHLoose.l122.l223.ef28.e28_lhtight_nod0_iloose'


crossValPath  = '/afs/cern.ch/work/j/jodafons/public/Online/tuning/mc15_201609XX/data/jobconfigs/user.wsfreund.crossValid-JackKnife.pic.gz/crossValid-JackKnife.pic.gz'

etBins       = [0, 30, 40, 50, 100000 ]
etaBins      = [0, 0.8 , 1.37, 1.54, 2.5]

from TuningTools.CrossValid import CrossValidArchieve
with CrossValidArchieve( crossValPath ) as CVArchieve:
  crossVal = CVArchieve
  del CVArchieve


from TuningTools import createData
from TuningTools import Reference, RingerOperation
from RingerCore  import expandFolders

createData( 
            basePath+'/'+sgnInputFile , 
            #'/tmp/jodafons/user.jodafons.mc15_13TeV.361106.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.merge.AOD.e3601_s2876_r7917_r7676.dump.trigEL.p0100_GLOBAL/',
            basePath+'/'+bkgInputFile ,
            RingerOperation.EFCalo,
            ringConfig      = 100,
            #referenceSgn    = Reference.AcceptAll,
            referenceSgn    = Reference.Off_Likelihood,
            #referenceBkg    = Reference.Truth,
            referenceBkg    = Reference.Off_Likelihood,
            treePath        = treePath,
            pattern_oFile   = outputFile,
            l1EmClusCut     = 20,
            l2EtCut         = 19,
            efEtCut         = 24,
            etBins          = etBins,
            etaBins         = etaBins,
            crossVal        = crossVal,
            nClusters       = 5000,
            #efficiencyValues = [97.0, 2.0], 
            toMatlab        = True)



from RingerCore import mkdir_p
mkdir_p(outputFile)
import os
os.system(('mv %s.* %s/') % (outputFile, outputFile) )
os.system(('mv *.pdf %s/') % (outputFile) )





