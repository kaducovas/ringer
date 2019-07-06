

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
from RingerCore import LoggingLevel


############################################################################################

NOV      = 5000
#NOV = -1
level    = LoggingLevel.DEBUG
#level    = LoggingLevel.INFO
#sgnData = '/home/wsfreund/CERN-DATA/Offline/skimmedNtuple/user.wsfreund.mc14_Zee_mcsel_skimntuple_offline_lhcalo_refs_SkimmedNtuple.root'
#bkgData = '/home/wsfreund/CERN-DATA/Offline/skimmedNtuple/user.wsfreund.mc14_JF17_mcsel_skimntuple_offline_lhcalo_refs_SkimmedNtuple.root'
sgnData  = '/home/jodafons/CERN-DATA/Online/data/mc15_13TeV/Zee/361106/user.jodafons.mc15_13TeV.361106.Zee.merge.SelectionZee.PhysVal.r0002_GLOBAL/'
bkgData  = '/home/jodafons/CERN-DATA/Online/data/mc15_13TeV/JF17/423300/user.jodafons.mc15_13TeV.423300.JF17.SelectionFakes.PhysVal.r0002_GLOBAL/'
 
############################################################################################

# First event Looper
eventLooper1 = EventLooper( inputFiles = sgnData, 
                            treePath = 'HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = NOV,
                            level = level)

# Second Event Looper
eventLooper2 = EventLooper( inputFiles = bkgData, 
                            treePath = 'HLT/Egamma/Expert/support/fakes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = NOV,
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
#algFakes.set_pidname( '!el_lhloose' )

algEmu = EmulationTool( "EmulationTool" )
algEmu.setId(eventLooper1.id())
algEmu.setId(eventLooper2.id())


calibPath = '../../data/Online/mc15_20170221_v5'
pidnames  = ['Tight','Medium','Loose','VeryLoose']
etbins    = [0, 20, 30, 40, 50, 1e5 ]
etabins   = [0, 0.8 , 1.37, 1.54, 2.5]


# Calibration configs
algCalib = EffCorrTool( 'Calibration' )
algCalib.basepath = 'Event/Correction'
algCalib.setProbesId( eventLooper1.id() )
algCalib.setFakesId( eventLooper2.id() )
algCalib.setLimits([1,25,50])
algCalib.doTrigger  = True
algCalib.setBinning( etbins, etabins )

# create all ringer emulators
for pidname in pidnames:
  selector = CaloRingerSelectorTool( ('EFCalo_isRinger%s_v5')%(pidname.replace('Very','V')))
  selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname))
  selector.calibPath = calibPath
  algname = ('EFCalo_isRinger%s_v5') % (pidname.replace('Very','V'))
  tgtname = ('EFCalo_isLH%sCaloOnly_rel21_20170217') % (pidname.replace('Very','V'))
  algCalib.setTargets( pidname, algname, tgtname ) 
  algEmu.add_trigger_selector( ('EFCalo_isRinger%s_v5')%(pidname.replace('Very','V')), selector )



############################################################################################

from TrigEgammaDevelopments import job

job.push_back(eventLooper1)
job.push_back(eventLooper2)
job.push_back(algZ)
job.push_back(algFakes)
job.push_back(algEmu)
job.push_back(algCalib)
# Start!
job.initialize()
job.execute()
job.finalize()

