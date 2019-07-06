




from TrigEgammaDevelopments.Event          import EventLooper
from TrigEgammaDevelopments.dataframe      import ElectronCandidate
from TuningTools.dataframe.EnumCollection  import Dataframe as DataframeEnum
from RingerCore                            import LoggingLevel, Logger


import argparse
mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFiles', action='store', 
    dest='inputFiles', required = True, nargs='+',
    help = "The input files.")

parser.add_argument('-o','--outputFile', action='store', 
    dest='outputFile', required = True,
    help = "The output store file name.")

parser.add_argument('-n','--nov', action='store', 
    dest='nov', required = False, default = -1,
    help = "Number of events.")

parser.add_argument('-m','--isMC', action='store_true',
    dest='isMC', required = False, default = False,
    help = "Use this to switch to Monte Carlo mode")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()
nov=int(args.nov)

 
############################################################################################
level    = LoggingLevel.INFO

# First event Looper
eventLooper1 = EventLooper( inputFiles = args.inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = nov,
                            outputFile = args.outputFile,
                            level = level)

# Second Event Looper
eventLooper2 = EventLooper( inputFiles = args.inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/fakes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile = args.outputFile,
                            nov = nov,
                            level = level)

############################################################################################

from TrigEgammaDevelopments.tools import EventSelection, QuadrantTool

algZ = EventSelection('EventSelectionZ')
algZ.selectionZ     = True
algZ.selectionFakes = False
algZ.doTrigger      = True
algZ.l2EtCut        = 15
algZ.offEtCut       = 15
algZ.setId(eventLooper1.id())
algZ.set_pidname( 'el_lhVLoose' )

algFakes = EventSelection('EventSelectionFakes')
algFakes.selectionZ = False
algFakes.selectionFakes = True
algFakes.doTrigger      = True
algFakes.l2EtCut = 15
algFakes.offEtCut = 15
algFakes.setId(eventLooper2.id())


from TrigEgammaDevelopments.helper import createEmulation_20170221_v6
# Create emulation Ringer tool
algEmu, chains_emulated =  createEmulation_20170221_v6( )
algEmu.setId(eventLooper1.id())
algEmu.setId(eventLooper2.id())
algEmu.doTrigger = True

alg3 = QuadrantTool("QuadrantProbes")
alg3.basepath = 'Event/QuadrantTool/Probes'
alg3.doTrigger = True
alg3.setId(eventLooper1.id())
alg4 = QuadrantTool("QuadrantFakes")
alg4.basepath = 'Event/QuadrantTool/Fakes'
alg4.setId(eventLooper2.id())
alg4.doTrigger = True

alg3.add_quadrant('L2Calo_isEMLoose&HLT_isLHVLoose_rel21_20170217'  ,'EFCalo_isRingerVLoose_v6&HLT_isLHVLoose_rel21_20170217' )
alg3.add_quadrant('L2Calo_isEMLoose&HLT_isLHLoose_rel21_20170217'   ,'EFCalo_isRingerLoose_v6&HLT_isLHLoose_rel21_20170217'   )
alg3.add_quadrant('L2Calo_isEMMedium&HLT_isLHMedium_rel21_20170217','EFCalo_isRingerMedium_v6&HLT_isLHMedium_rel21_20170217')
alg3.add_quadrant('L2Calo_isEMTight&HLT_isLHTight_rel21_20170217'   ,'EFCalo_isRingerTight_v6&HLT_isLHTight_rel21_20170217'   )
alg4.add_quadrant('L2Calo_isEMLoose&HLT_isLHVLoose_rel21_20170217'  ,'EFCalo_isRingerVLoose_v6&HLT_isLHVLoose_rel21_20170217' )
alg4.add_quadrant('L2Calo_isEMLoose&HLT_isLHLoose_rel21_20170217'   ,'EFCalo_isRingerLoose_v6&HLT_isLHLoose_rel21_20170217'   )
alg4.add_quadrant('L2Calo_isEMMedium&HLT_isLHMedium_rel21_20170217','EFCalo_isRingerMedium_v6&HLT_isLHMedium_rel21_20170217')
alg4.add_quadrant('L2Calo_isEMTight&HLT_isLHTight_rel21_20170217'   ,'EFCalo_isRingerTight_v6&HLT_isLHTight_rel21_20170217'   )



############################################################################################

from TrigEgammaDevelopments import job
job.push_back(eventLooper1)
job.push_back(eventLooper2)
job.push_back(algZ)
job.push_back(algFakes)
job.push_back(algEmu)
job.push_back(alg3)
job.push_back(alg4)
job.initialize()
job.execute()
job.finalize()



