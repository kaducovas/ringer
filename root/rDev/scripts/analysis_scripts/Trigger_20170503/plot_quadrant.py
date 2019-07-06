




from TrigEgammaDevelopments.Event          import EventLooper
from TrigEgammaDevelopments.dataframe      import ElectronCandidate
from TuningTools.dataframe.EnumCollection  import Dataframe as DataframeEnum
from RingerCore                            import LoggingLevel, Logger


import argparse
mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFile', action='store', 
    dest='inputFile', required = True,
    help = "The input files.")

parser.add_argument('-o','--outputFile', action='store', 
    dest='outputFile', required = True,
    help = "The output store file name.")


parser.add_argument('--etbins', action='store', 
    dest='etbins', required = True, nargs='+', type=float,
    help = "The et bins like: 0 20 30 40 50 100000")

parser.add_argument('--etabins', action='store', 
    dest='etabins', required = True, nargs='+', type=float,
    help = "The eta bins like: 0 0.8 1.37 1.54 2.5")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()

from RingerCore import  restoreStoreGate
sg1 =  restoreStoreGate( args.inputFile )


############################################################################################

def make_quadrant( name ,basepath, etbins, etabins, doTrigger):
  from TrigEgammaDevelopments.tools import EventSelection, QuadrantTool

  alg = QuadrantTool(name)
  alg.basepath = basepath
  alg.doTrigger = doTrigger
  alg.setEtBinningValues( etbins   )
  alg.setEtaBinningValues( etabins )


  # Check the final trigger combination: T2Calo+HLT_LH and Ringer+HLT_LH
  #alg.add_quadrant('L2Calo_isEMLoose'  ,'EFCalo_isRingerVLoose_v6' , alias=['VLoose','L2CaloRinge X T2Calo'])
  #alg.add_quadrant('L2Calo_isEMLoose'  ,'EFCalo_isRingerLoose_v6'   , alias=['Loose','L2CaloRinger X T2Calo'])
  #alg.add_quadrant('L2Calo_isEMMedium' ,'EFCalo_isRingerMedium_v6' , alias=['Medium','L2CaloRinger X T2Calo'])
  #alg.add_quadrant('L2Calo_isEMTight'  ,'EFCalo_isRingerTight_v6'   , alias=['Tight','L2CaloRinger X T2Calo'])
  
  
  
  # Check the final trigger combination: T2Calo+HLT_LH and Ringer+HLT_LH
  alg.add_quadrant('L2Calo_isEMLoose&HLT_isLHVLoose_rel21_20170217'  ,
                    'EFCalo_isRingerVLoose_v6&HLT_isLHVLoose_rel21_20170217' , alias=['VLoose','L2Calo_Ringer_HLT_LH X L2Calo_CutBased_HLT_LH'])
  
  alg.add_quadrant('L2Calo_isEMLoose&HLT_isLHLoose_rel21_20170217'   ,
                    'EFCalo_isRingerLoose_v6&HLT_isLHLoose_rel21_20170217'   , alias=['Loose','L2Calo_Ringer_HLT_LH X L2Calo_CutBased_HLT_LH'])
  
  alg.add_quadrant('L2Calo_isEMMedium&HLT_isLHMedium_rel21_20170217' ,
                    'EFCalo_isRingerMedium_v6&HLT_isLHMedium_rel21_20170217' , alias=['Medium','L2Calo_Ringer_HLT_LH X L2Calo_CutBased_HLT_LH'])
  
  alg.add_quadrant('L2Calo_isEMTight&HLT_isLHTight_rel21_20170217'   ,
                    'EFCalo_isRingerTight_v6&HLT_isLHTight_rel21_20170217'   , alias=['Tight','L2Calo_Ringer_HLT_LH X L2Calo_CutBasedHLT_LH'] )

  return alg

############################################################################################

toPDF=True
toPDF=False
algZ=make_quadrant('Probes','Event/QuadrantTool/Probes',args.etbins,args.etabins,True)
algF=make_quadrant('Probes','Event/QuadrantTool/Fakes',args.etbins,args.etabins,True)


algZ.setStoreSvc(sg1)
algZ.plot(pdfoutput='data16_13TeV_quadrand_probes.pdf',pdftitle='Quadrant Probes Analysis (data16_13TeV)')
algF.setStoreSvc(sg1)
algF.plot(pdfoutput='data16_13TeV_quadrand_fakes.pdf',pdftitle='Quadrant Fake Analysis (data16_13TeV)')








