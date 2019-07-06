

from TrigEgammaDevelopments.Event                     import EventLooper
from TrigEgammaDevelopments.AlgBaseTool               import AlgBaseTool
from TrigEgammaDevelopments.tools.EfficiencyTool      import EfficiencyTool
from TrigEgammaDevelopments.tools.EffCorrTool         import EffCorrTool
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

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()
inputFiles = args.inputFiles
nov = int(args.nov)
level = LoggingLevel.INFO
outputFile = args.outputFile
if not outputFile:
  outputFile='histo.root'

etbins  = [0, 20, 30, 40, 50, 1e5 ]
etabins = [0, 0.8 , 1.37, 1.54, 2.5]


############################################################################################

# First event Looper
eventLooper1 = EventLooper( inputFiles = inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile=outputFile,
                            nov = nov,
                            level = level)

# Second Event Looper
eventLooper2 = EventLooper( inputFiles = inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/fakes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile=outputFile,
                            nov = nov,
                            level = level)

############################################################################################

algZ = EventSelection('EventSelectionZ')
algZ.selectionZ     = True
algZ.selectionFakes = False
algZ.doTrigger      = True
algZ.l2EtCut        = 15
algZ.setId(eventLooper1.id())
algZ.set_pidname( 'el_lhLoose' )

algFakes = EventSelection('EventSelectionFakes')
algFakes.selectionZ     = False
algFakes.selectionFakes = True
algFakes.doTrigger      = True
algFakes.l2EtCut        = 15
algFakes.setId(eventLooper2.id())

algEmu = EmulationTool( "EmulationTool" )
algEmu.setId(eventLooper1.id())
algEmu.setId(eventLooper2.id())

calibPath = '../../../data/Online/mc15_20170221_v5'
pidnames  = ['Tight','Medium','Loose','VeryLoose']

# Calibration configs
algCalib = EffCorrTool( 'Calibration' )
algCalib.basepath = 'Event/Correction'
algCalib.setBinning( etbins, etabins )
algCalib.setProbesId( eventLooper1.id() )
algCalib.setFakesId( eventLooper2.id() )
algCalib.doTrigger  = True


# create all ringer emulators
for pidname in pidnames:
  algname = ('EFCalo_isRinger%s_v5') % (pidname.replace('Very','V'))
  tgtname = ('EFCalo_isLH%sCaloOnly_rel21_20170217') % (pidname.replace('Very','V'))
  selector = CaloRingerSelectorTool( algname )
  selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname))
  selector.calibPath = calibPath
  algEmu.add_trigger_selector(  algname, selector )
  algCalib.setTargets( pidname, algname, tgtname ) 


############################################################################################

from TrigEgammaDevelopments import job

job.push_back(eventLooper1)
job.push_back(eventLooper2)
job.push_back(algZ)
job.push_back(algFakes)
job.push_back(algEmu)
job.push_back(algCalib)
job.initialize()
job.execute()
job.finalize()


