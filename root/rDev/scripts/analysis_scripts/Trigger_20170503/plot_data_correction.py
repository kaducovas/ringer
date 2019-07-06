

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
    dest='outputFile', required = True, 
    help = "The output pdf name file.")

parser.add_argument('--etbins', action='store', 
    dest='etbins', required = True, nargs='+', type=float,
    help = "The et bins like: 0 20 30 40 50 100000")

parser.add_argument('--etabins', action='store', 
    dest='etabins', required = True, nargs='+', type=float,
    help = "The eta bins like: 0 0.8 1.37 1.54 2.5")

parser.add_argument('-r','--relax', action='store', 
    dest='relax', required = True, nargs='+', type = float,
    help = "The relax param: Tight Medium Loose VLoose values...")

parser.add_argument('-n','--name', action='store', 
    dest='name', required = True, 
    help = "The name of the tuning correction. e.g. v6.")

parser.add_argument('-l','--limits', action='store', 
    dest='limits', required = True, nargs='+', type=int,
    help = "The limits to correct the output. e.g. 10 25 40")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()

# treat data input
# convert to int
relax = {'Tight':args.relax[0],'Medium':args.relax[1],\
         'Loose':args.relax[2],'VLoose':args.relax[3]}

from RingerCore import  restoreStoreGate
sg1 =  restoreStoreGate( args.inputFile )


# Calibration configs
algCalib = EffCorrTool( 'NNCalibration' )
algCalib.setEtBinningValues( args.etbins   )
algCalib.setEtaBinningValues( args.etabins )
algCalib.doTrigger  = True
algCalib.setAlias( args.name )
algCalib.setLimits( args.limits)

from TrigEgammaDevelopments.helper import createEmulation_trigger_20170221_v6
algEmu, chains_emulated =  createEmulation_trigger_20170221_v6( )
chains=[ pair[0] for key, pair in chains_emulated.iteritems() ]
selectors={}

# create all ringer emulators
for pidname, pair in chains_emulated.iteritems():
  tgtname = ('EFCalo_isLH%sCaloOnly_rel21_20170217') % (pidname) # this will be the target
  algname = pair[0]
  selectors[algname]=pair[1]
  selectors[algname].initialize()
  algCalib.setTargets( pidname, algname, tgtname, relax[pidname] ) 

algCalib.setStoreSvc(sg1)
algCalib.plot(selectorDict = selectors, pdfoutput=args.outputFile,
    dovertical=False,pdftitle='Data16_13TeV Threshold Correction')

