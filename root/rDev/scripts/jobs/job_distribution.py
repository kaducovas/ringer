



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
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

parser.add_argument('-m','--isMC', action='store_true',
    dest='isMC', required = False, default = False,
    help = "Use this to switch to Monte Carlo mode")

parser.add_argument('-f','--isFakes', action='store_true',
    dest='isFakes', required = False, default = False,
    help = "Use this to switch to fakes mode selection")

parser.add_argument('-c','--offEtCut', action='store', 
    dest='offEtCut', required = False, default = 15,type=float,
    help = "The offline et cut")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()



 
############################################################################################
level    = LoggingLevel.INFO

# First event Looper
eventLooper  = EventLooper( inputFiles = args.inputFiles, 
                            treePath = '*/HLT/Egamma/Expert/support/fakes' if args.isFakes else\
                                       '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = args.nov,
                            outputFile = args.outputFile,
                            level = level)

############################################################################################

from TrigEgammaDevelopments.tools import EventSelection

algE = EventSelection('EventSelection')
algE.selectionZ     = False if args.isFakes else True
algE.selectionFakes = True if args.isFakes else False
algE.doTrigger      = True
algE.l2EtCut        = args.offEtCut
algE.offEtCut       = args.offEtCut
algE.selectionMC    = True if args.isMC else False
if args.isFakes:
  algE.set_pidname( 'el_lhVLoose' )
algE.setId(eventLooper.id())


from TrigEgammaDevelopments.helper import createEmulation_trigger_20170221_v6
# Create emulation Ringer tool
algEmu, chains_emulated =  createEmulation_trigger_20170221_v6( )
algEmu.setId(eventLooper.id())
algEmu.doTrigger = True


from TrigEgammaDevelopments.tools import DistributionTool
algDist = DistributionTool('DistributionTool')
if args.isMC:
  algDist.setMCId(eventLooper.id())
else:
  algDist.setDataId(eventLooper.id())

algDist.setId(eventLooper.id())

chains=[ pair[0] for pair in chains_emulated ]
algDist.setDiscriminantList( chains )
algDist.doTrigger = True


############################################################################################

from TrigEgammaDevelopments import job
job.push_back(eventLooper)
job.push_back(algE)
job.push_back(algEmu)
job.push_back(algDist)
job.initialize()
job.execute()
job.finalize()




