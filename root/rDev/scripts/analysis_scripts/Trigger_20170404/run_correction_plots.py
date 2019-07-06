
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

parser.add_argument('-i','--inputFile', action='store', 
    dest='inputFile', required = True, 
    help = "The input files that will be used to generate the plots")

parser.add_argument('-o','--outputFile', action='store', 
    dest='outputFile', required = False, default = None,
    help = "The output store name.")

parser.add_argument('-l','--limits', action='store', 
    dest='limits', required = True, nargs='+',
    help = "The limits to correct the output")

parser.add_argument('-a','--alias', action='store', 
    dest='alias', required = False, default = 'tuning',
    help = "The tuning name")

parser.add_argument('-r','--relax', action='store', 
    dest='relax', required = False, nargs='+', default = [0.0],
    help = "The tuning relax factor")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()
outputFile = args.outputFile
limits = []

for l in args.limits:
  limits.append(int(l))

#etbins = [0,20,1e5]
#etabins = [0,2.5]
etbins  = [0, 20  , 30  , 40  , 50 , 1e5 ]
etabins = [0, 0.8 , 1.37, 1.54, 2.5]


calibPath = '../../../data/Online/mc15_20170221_v5'

metadata = {'UseLumiTool': False,
            'UseLumiVar' : False,
            'UseEtaVar'  : False,
            'LumiCut'    : 40,
            'DoPileupCorrection':True,
            'UseNoActivationFunctionInTheLastLayer': True,
            }

# create all ringer emulators
selectorDict={}
pidnames  = ['Tight','Medium','Loose','VeryLoose']
for pidname in pidnames:
  selector = CaloRingerSelectorTool( ('EFCalo_isRinger%s_v5')%(pidname.replace('Very','V')))
  selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname))
  selector.calibPath = calibPath
  selector.initialize()
  selectorDict[('EFCalo_isRinger%s_v5')%(pidname.replace('Very','V'))] = selector

# Calibration configs
algCalib = EffCorrTool( 'Calibration' )
algCalib.basepath = 'Event/Correction'
#algCalib.setLimits([10,25,40])
algCalib.setLimits(limits)

algCalib.doTrigger  = True
algCalib.setBinning( etbins, etabins )
algCalib.setMetadata(metadata)
algCalib.setAlias( args.alias )

relaxList = args.relax
if len(relaxList) == 0:
  relaxList = len(pidnames)*relaxList

# set all targets
for idx, pidname in enumerate(pidnames):
  algname = ('EFCalo_isRinger%s_v5') % (pidname.replace('Very','V'))
  tgtname = ('EFCalo_isLH%sCaloOnly_rel21_20170217') % (pidname.replace('Very','V'))
  algCalib.setTargets( pidname, algname, tgtname, float(relaxList[idx])/100. ) 

############################################################################################

from RingerCore import restoreStoreGate
store = restoreStoreGate( args.inputFile )
algCalib.setStoreSvc(store)
algCalib.plot( selectorDict = selectorDict )





