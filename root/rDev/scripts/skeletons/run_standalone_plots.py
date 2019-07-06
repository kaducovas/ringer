from TrigEgammaDevelopments.Event                     import EventLooper
from TrigEgammaDevelopments.AlgBaseTool               import AlgBaseTool
from TrigEgammaDevelopments.tools.EfficiencyTool      import EfficiencyTool
from TrigEgammaDevelopments.tools.QuadrantTool        import QuadrantTool
from TrigEgammaDevelopments.tools.EmulationTool       import EmulationTool
from TrigEgammaDevelopments.tools.EventSelection      import EventSelection
from TrigEgammaDevelopments.selector.SelectorAlgTool  import CaloRingerSelectorTool, egammaRingerPid 
from TrigEgammaDevelopments.dataframe                 import ElectronCandidate
from TuningTools.dataframe.EnumCollection             import Dataframe as DataframeEnum
from RingerCore import LoggingLevel, restoreStoreGate

store = restoreStoreGate('histos.root')


alg1 = QuadrantTool("QuadrantProbes")
alg1.basepath = 'Event/QuadrantTool/ZeeProbes'
alg1.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217','EFCalo_isRingerVLoose_v5')
alg1.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217','EFCalo_isRingerLoose_v5')
alg1.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217','EFCalo_isRingerMedium_v5')
alg1.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217','EFCalo_isRingerTight_v5')
alg1.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217' ,'EFCalo_isRingerVLoose_v5&HLT_isLHVLoose_rel21_20170217')
alg1.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217' ,'EFCalo_isRingerLoose_v5&HLT_isLHLoose_rel21_20170217')
alg1.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217' ,'EFCalo_isRingerMedium_v5&HLT_isLHMedium_rel21_20170217')
alg1.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217' ,'EFCalo_isRingerTight_v5&HLT_isLHTight_rel21_20170217')
alg1.setStoreSvc(store)


alg2 = QuadrantTool("QuadrantFakes")
alg2.basepath = 'Event/QuadrantTool/JF17Fakes'
alg2.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217','EFCalo_isRingerVLoose_v5')
alg2.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217','EFCalo_isRingerLoose_v5')
alg2.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217','EFCalo_isRingerMedium_v5')
alg2.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217','EFCalo_isRingerTight_v5')
alg2.add_quadrant('EFCalo_isLHVLooseCaloOnly_rel21_20170217&HLT_isLHVLoose_rel21_20170217' ,'EFCalo_isRingerVLoose_v5&HLT_isLHVLoose_rel21_20170217')
alg2.add_quadrant('EFCalo_isLHLooseCaloOnly_rel21_20170217&HLT_isLHLoose_rel21_20170217' ,'EFCalo_isRingerLoose_v5&HLT_isLHLoose_rel21_20170217')
alg2.add_quadrant('EFCalo_isLHMediumCaloOnly_rel21_20170217&HLT_isLHMedium_rel21_20170217' ,'EFCalo_isRingerMedium_v5&HLT_isLHMedium_rel21_20170217')
alg2.add_quadrant('EFCalo_isLHTightCaloOnly_rel21_20170217&HLT_isLHTight_rel21_20170217' ,'EFCalo_isRingerTight_v5&HLT_isLHTight_rel21_20170217')
alg2.setStoreSvc(store)



alg1.plot(dirname='mc15_13TeV.QuadrantTool')
alg2.plot(dirname='mc15_13TeV.QuadrantTool')


