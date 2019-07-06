from TrigEgammaDevelopments.Event                     import EventLooper
from TrigEgammaDevelopments.AlgBaseTool               import AlgBaseTool
from TrigEgammaDevelopments.tools.EfficiencyTool      import EfficiencyTool
from TrigEgammaDevelopments.tools.QuadrantTool        import QuadrantTool
from TrigEgammaDevelopments.tools.EmulationTool       import EmulationTool
from TrigEgammaDevelopments.tools.EventSelection      import EventSelection
from TrigEgammaDevelopments.selector.SelectorAlgTool  import CaloRingerSelectorTool, egammaRingerPid 
from TrigEgammaDevelopments.dataframe                 import ElectronCandidate
from TuningTools.dataframe.EnumCollection             import Dataframe as DataframeEnum
from RingerCore                                       import Logger, LoggingLevel, BooleanStr
import argparse

mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFiles', action='store', 
    dest='inputFiles', required = True, nargs='+',
    help = "The input files that will be used to generate the plots")

parser.add_argument('-o','--outputFile', action='store', 
    dest='outputFile', required = False, default = None,
    help = "The output store name.")

parser.add_argument('-n','--nov', action='store', 
    dest='nov', required = False, default = -1,
    help = "Number of events.")

parser.add_argument('-rc','--ringerCalibPath', action='store', 
    dest='ringerCalibPath', required = True, default = None,
    help = "The ringer calib path.")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()
inputFiles = args.inputFiles
nov = int(args.nov)
level = LoggingLevel.INFO

if args.outputFile:
  outputFile = args.outputFile
else:
  outputFile = inputFiles[0].split('/')[-1]+'.histos.root'


############################################################################################


monList  = [
           'EFCalo_isLHVLooseCaloOnly_rel21_20170214',
           'EFCalo_isLHLooseCaloOnly_rel21_20170214',
           'EFCalo_isLHMediumCaloOnly_rel21_20170217',
           'EFCalo_isLHTightCaloOnly_rel21_20170217',
           'EFCalo_isRingerVLoose_v6', 
           'EFCalo_isRingerLoose_v6', 
           'EFCalo_isRingerMedium_v6', 
           'EFCalo_isRingerTight_v6', 
           'EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217',
           'EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217',
           'EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217',
           'EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217',
           'EFCalo_isRingerVLoose_v6&HLT_isLHVLoose_rel21_20170217',
           'EFCalo_isRingerLoose_v6&HLT_isLHLoose_rel21_20170217',
           'EFCalo_isRingerMedium_v6&HLT_isLHMedium_rel21_20170217',
           'EFCalo_isRingerTight_v6&HLT_isLHTight_rel21_20170217',
           ] 
 
############################################################################################

# First event Looper
eventLooper1 = EventLooper( inputFiles = inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = nov,
                            outputFile = outputFile,
                            level = level)

# Second Event Looper
eventLooper2 = EventLooper( inputFiles = inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/fakes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile = outputFile,
                            nov = nov,
                            level = level)

############################################################################################

algZ = EventSelection('EventSelectionZ')
algZ.selectionZ = True
algZ.selectionFakes = False
algZ.doTrigger  = True
algZ.set_pidname( 'el_lhLoose' )
algZ.setId(eventLooper1.id())
algZ.l2EtCut = 15
algZ.offEtCut = 15

# Apply Internal MC selection
algFakes = EventSelection('EventSelectionFakes')
algFakes.selectionZ = False
algFakes.selectionFakes = True
algFakes.doTrigger      = True
algFakes.setId(eventLooper2.id())
algFakes.l2EtCut = 15
algFakes.offEtCut = 15


# Create emulation Ringer tool
algEmu = EmulationTool( "EmulationTool" )
algEmu.setId(eventLooper1.id())
algEmu.setId(eventLooper2.id())

calibPath = args.ringerCalibPath
pidnames  = ['Tight','Medium','Loose','VeryLoose']
# create all ringer emulators
for pidname in pidnames:
  selector = CaloRingerSelectorTool( ('EFCalo_isRinger%s_v6')%(pidname.replace('Very','V')))
  selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname))
  selector.calibPath = calibPath
  algEmu.add_trigger_selector( ('EFCalo_isRinger%s_v6')%(pidname.replace('Very','V')), selector )


alg1 = EfficiencyTool( "EfficiencyToolProbes")
alg1.basepath = 'Event/EfficiencyTool/Probes'
alg1.set_monitoring( monList )
alg1.eventType = ElectronCandidate.Probe
alg1.setId(eventLooper1.id())

alg2= EfficiencyTool( "EfficiencyToolFakes")
alg2.basepath = 'Event/EfficiencyTool/Fakes'
alg2.set_monitoring( monList )
alg2.eventType = ElectronCandidate.Fake
alg2.setId(eventLooper2.id())

alg3 = QuadrantTool("QuadrantProbes")
alg3.basepath = 'Event/QuadrantTool/Probes'
alg3.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217','EFCalo_isRingerVLoose_v6')
alg3.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217','EFCalo_isRingerLoose_v6')
alg3.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217','EFCalo_isRingerMedium_v6')
alg3.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217','EFCalo_isRingerTight_v6')
alg3.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217' ,'EFCalo_isRingerVLoose_v6&HLT_isLHVLoose_rel21_20170217')
alg3.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217' ,'EFCalo_isRingerLoose_v6&HLT_isLHLoose_rel21_20170217')
alg3.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217' ,'EFCalo_isRingerMedium_v6&HLT_isLHMedium_rel21_20170217')
alg3.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217' ,'EFCalo_isRingerTight_v6&HLT_isLHTight_rel21_20170217')
alg3.setId(eventLooper1.id())

alg4 = QuadrantTool("QuadrantFakes")
alg4.basepath = 'Event/QuadrantTool/Fakes'
alg4.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217','EFCalo_isRingerVLoose_v6')
alg4.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217','EFCalo_isRingerLoose_v6')
alg4.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217','EFCalo_isRingerMedium_v6')
alg4.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217','EFCalo_isRingerTight_v6')
alg4.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217' ,'EFCalo_isRingerVLoose_v6&HLT_isLHVLoose_rel21_20170217')
alg4.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217' ,'EFCalo_isRingerLoose_v6&HLT_isLHLoose_rel21_20170217')
alg4.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217' ,'EFCalo_isRingerMedium_v6&HLT_isLHMedium_rel21_20170217')
alg4.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217' ,'EFCalo_isRingerTight_v6&HLT_isLHTight_rel21_20170217')
alg4.setId(eventLooper2.id())


############################################################################################

from TrigEgammaDevelopments import job

job.push_back(eventLooper1)
job.push_back(eventLooper2)
job.push_back(algZ)
job.push_back(algFakes)
job.push_back(algEmu)
job.push_back(alg1)
job.push_back(alg2)
job.push_back(alg3)
job.push_back(alg4)
# Start!
job.initialize()
job.execute()
job.finalize()





