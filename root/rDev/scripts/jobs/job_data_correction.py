

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
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

parser.add_argument('-c','--offEtCut', action='store', 
    dest='offEtCut', required = False, default = 15, type=float,
    help = "The Et Cut applied.")


parser.add_argument('--etbins', action='store', 
    dest='etbins', required = True, nargs='+', type=float,
    help = "The et bins like: 0 20 30 40 50 100000")

parser.add_argument('--etabins', action='store', 
    dest='etabins', required = True, nargs='+', type=float,
    help = "The eta bins like: 0 0.8 1.37 1.54 2.5")

parser.add_argument('-r','--relax', action='store', 
    dest='relax', required = True, nargs='+', type = float,
    help = "The relax param: Tight Medium Loose VLoose values...")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()

# treat data input
# convert to int
relax = {'Tight':args.relax[0],'Medium':args.relax[1],\
         'Loose':args.relax[2],'VLoose':args.relax[3]}

print relax

############################################################################################
level = LoggingLevel.INFO

# First event Looper
eventLooperZ = EventLooper( inputFiles = args.inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile=args.outputFile,
                            nov = args.nov,
                            level = level)

# Second Event Looper
eventLooperF = EventLooper( inputFiles = args.inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/fakes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile=args.outputFile,
                            nov = args.nov,
                            level = level)

############################################################################################

algZ = EventSelection('EventSelectionZ')
algZ.selectionZ     = True
algZ.selectionFakes = False
algZ.doTrigger      = True
algZ.l2EtCut        = args.offEtCut
algZ.setId(eventLooperZ.id())
algZ.set_pidname( 'el_lhVLoose' )

algF = EventSelection('EventSelectionF')
algF.selectionZ     = False
algF.selectionFakes = True
algF.doTrigger      = True
algF.l2EtCut        = args.offEtCut
algF.setId(eventLooperF.id())


# Add emultaion tool to emulate all NN outputs
from TrigEgammaDevelopments.helper import createEmulation_trigger_20170221_v6
# Create emulation Ringer tool
algEmu, chains_emulated =  createEmulation_trigger_20170221_v6( )
algEmu.setId(eventLooperZ.id())
algEmu.setId(eventLooperF.id())



# Calibration configs
algCalib = EffCorrTool( 'NNCalibration' )
algCalib.setEtBinningValues( args.etbins   )
algCalib.setEtaBinningValues( args.etabins )
algCalib.setProbesId( eventLooperZ.id() )
algCalib.setFakesId( eventLooperF.id() )
algCalib.doTrigger  = True

print args.etbins
print args.etabins
# create all ringer emulators
for pidname in chains_emulated:
  tgtname = ('EFCalo_isLH%sCaloOnly_rel21_20170217') % (pidname) # this will be the target
  algname = chains_emulated[pidname][0]
  algCalib.setTargets( pidname, algname, tgtname, relax[pidname] ) 

############################################################################################

from TrigEgammaDevelopments import job

job.push_back(eventLooperZ)
job.push_back(eventLooperF)
job.push_back(algZ)
job.push_back(algF)
job.push_back(algEmu)
job.push_back(algCalib)

job.initialize()
job.execute()
job.finalize()


