

from TrigEgammaDevelopments.Event                     import EventLooper
from TrigEgammaDevelopments.AlgBaseTool               import AlgBaseTool
from TrigEgammaDevelopments.tools.EfficiencyTool      import EfficiencyTool
from TrigEgammaDevelopments.tools.QuadrantTool        import QuadrantTool
from TrigEgammaDevelopments.tools.EmulationTool       import EmulationTool
from TrigEgammaDevelopments.tools.EventSelection      import EventSelection
from TrigEgammaDevelopments.selector.SelectorAlgTool  import CaloRingerSelectorTool, egammaRingerPid 
from TrigEgammaDevelopments.dataframe                 import ElectronCandidate
from TuningTools.dataframe.EnumCollection             import Dataframe as DataframeEnum
from RingerCore import LoggingLevel


############################################################################################

histoName = 'mc15_13TeV.Zee_ProbesLHMedium.JF17_Truth.Analysis.root'

NOV      = -1
#level    = LoggingLevel.DEBUG
level    = LoggingLevel.INFO
#sgnData = '/home/wsfreund/CERN-DATA/Offline/skimmedNtuple/user.wsfreund.mc14_Zee_mcsel_skimntuple_offline_lhcalo_refs_SkimmedNtuple.root'
#bkgData = '/home/wsfreund/CERN-DATA/Offline/skimmedNtuple/user.wsfreund.mc14_JF17_mcsel_skimntuple_offline_lhcalo_refs_SkimmedNtuple.root'
sgnData  = '/home/jodafons/CERN-DATA/Online/data/mc15_13TeV/Zee/361106/user.jodafons.mc15_13TeV.361106.Zee.merge.SelectionZee.PhysVal.r0002_GLOBAL/'
bkgData  = '/home/jodafons/CERN-DATA/Online/data/mc15_13TeV/JF17/423300/user.jodafons.mc15_13TeV.423300.JF17.SelectionFakes.PhysVal.r0002_GLOBAL/'

monList  = [
           'EFCalo_isLHVLooseCaloOnly_rel21_20170214',
           'EFCalo_isLHLooseCaloOnly_rel21_20170214',
           'EFCalo_isLHMediumCaloOnly_rel21_20170217',
           'EFCalo_isLHTightCaloOnly_rel21_20170217',
           'EFCalo_isRingerVLoose_v5', 
           'EFCalo_isRingerLoose_v5', 
           'EFCalo_isRingerMedium_v5', 
           'EFCalo_isRingerTight_v5', 
           'EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217',
           'EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217',
           'EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217',
           'EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217',
           'EFCalo_isRingerVLoose_v5&HLT_isLHVLoose_rel21_20170217',
           'EFCalo_isRingerLoose_v5&HLT_isLHLoose_rel21_20170217',
           'EFCalo_isRingerMedium_v5&HLT_isLHMedium_rel21_20170217',
           'EFCalo_isRingerTight_v5&HLT_isLHTight_rel21_20170217',
           ] 
 
############################################################################################

# First event Looper
eventLooper1 = EventLooper( inputFiles = sgnData, 
                            treePath = 'HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = NOV,
                            outputFile = histoName,
                            level = level)

# Second Event Looper
eventLooper2 = EventLooper( inputFiles = bkgData, 
                            treePath = 'HLT/Egamma/Expert/support/fakes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile = histoName,
                            nov = NOV,
                            level = level)

############################################################################################

algZ = EventSelection('EventSelectionZ')
algZ.selectionZ = True
algZ.selectionFakes = False
algZ.doTrigger  = True
algZ.set_pidname( 'el_lhMedium' )
algZ.setId(eventLooper1.id())
algZ.l2EtCut = 15

# Apply Internal MC selection
algFakes = EventSelection('EventSelectionFakes')
algFakes.selectionZ = False
algFakes.selectionFakes = True
algFakes.doTrigger      = True
algFakes.setId(eventLooper2.id())
algFakes.l2EtCut = 15


# Create emulation Ringer tool
algEmu = EmulationTool( "EmulationTool" )
algEmu.setId(eventLooper1.id())
algEmu.setId(eventLooper2.id())


calibPath = '../../../data/Online/mc15_20170221_v5'
pidnames  = ['Tight','Medium','Loose','VeryLoose']
# create all ringer emulators
for pidname in pidnames:
  selector = CaloRingerSelectorTool( ('EFCalo_isRinger%s_v5')%(pidname.replace('Very','V')))
  selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname))
  selector.calibPath = calibPath
  algEmu.add_trigger_selector( ('EFCalo_isRinger%s_v5')%(pidname.replace('Very','V')), selector )


alg1 = EfficiencyTool( "EfficiencyToolProbes")
alg1.basepath = 'Event/EfficiencyTool/ZeeProbes'
alg1.set_monitoring( monList )
alg1.eventType = ElectronCandidate.Probe
alg1.setId(eventLooper1.id())

alg2= EfficiencyTool( "EfficiencyToolFakes")
alg2.basepath = 'Event/EfficiencyTool/JF17Fakes'
alg2.set_monitoring( monList )
alg2.eventType = ElectronCandidate.Fake
alg2.setId(eventLooper2.id())

alg3 = QuadrantTool("QuadrantProbes")
alg3.basepath = 'Event/QuadrantTool/ZeeProbes'
alg3.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217','EFCalo_isRingerVLoose_v5')
alg3.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217','EFCalo_isRingerLoose_v5')
alg3.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217','EFCalo_isRingerMedium_v5')
alg3.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217','EFCalo_isRingerTight_v5')
alg3.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217' ,'EFCalo_isRingerVLoose_v5&HLT_isLHVLoose_rel21_20170217')
alg3.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217' ,'EFCalo_isRingerLoose_v5&HLT_isLHLoose_rel21_20170217')
alg3.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217' ,'EFCalo_isRingerMedium_v5&HLT_isLHMedium_rel21_20170217')
alg3.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217' ,'EFCalo_isRingerTight_v5&HLT_isLHTight_rel21_20170217')
alg3.setId(eventLooper1.id())

alg4 = QuadrantTool("QuadrantFakes")
alg4.basepath = 'Event/QuadrantTool/JF17Fakes'
alg4.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217','EFCalo_isRingerVLoose_v5')
alg4.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217','EFCalo_isRingerLoose_v5')
alg4.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217','EFCalo_isRingerMedium_v5')
alg4.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217','EFCalo_isRingerTight_v5')
alg4.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217' ,'EFCalo_isRingerVLoose_v5&HLT_isLHVLoose_rel21_20170217')
alg4.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217' ,'EFCalo_isRingerLoose_v5&HLT_isLHLoose_rel21_20170217')
alg4.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217' ,'EFCalo_isRingerMedium_v5&HLT_isLHMedium_rel21_20170217')
alg4.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217' ,'EFCalo_isRingerTight_v5&HLT_isLHTight_rel21_20170217')
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



# Force finalize
#file='mc15_13TeV.Zee_ProbesLHMedium.JF17_Truth.Analysis.root'
#from RingerCore import StoreGate
#store = StoreGate(file,restoreStoreGate=True)
#alg3.setStoreSvc(store)
#alg4.setStoreSvc(store)
#alg3.finalize()
#alg4.finalize()



