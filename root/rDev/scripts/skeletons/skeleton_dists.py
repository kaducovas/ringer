

from TrigEgammaDevelopments.Event                     import EventLooper
from TrigEgammaDevelopments.tools.EventSelection      import EventSelection
from TrigEgammaDevelopments.selector.SelectorAlgTool  import CaloRingerSelectorTool, egammaRingerPid 
from TrigEgammaDevelopments.dataframe                 import ElectronCandidate
from TuningTools.dataframe.EnumCollection             import Dataframe as DataframeEnum
from RingerCore import LoggingLevel


############################################################################################

histoName = 'fudge_MC.root'

NOV      = -1
level    = LoggingLevel.INFO
mcData   = '/home/jodafons/CERN-DATA/Online/data/mc15_13TeV/user.jodafons.mc15_13TeV.361106.Zee.merge.SelectionZee.PhysVal.r0005_GLOBAL/'
ppData   = '/home/jodafons/CERN-DATA/Online/data/data16_13TeV/user.jodafons.data16_13TeV.periodG.physicsMain.p3013.SelectionData.PhysVal.r0005_GLOBAL/'
 
############################################################################################

# First event Looper
eventLooper1 = EventLooper( inputFiles = mcData, 
                            treePath = '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            nov = -1,
                            outputFile = histoName,
                            level = level)

# Second Event Looper
eventLooper2 = EventLooper( inputFiles = ppData, 
                            treePath = '*/HLT/Egamma/Expert/support/probes', 
                            dataframe = DataframeEnum.PhysVal, 
                            outputFile = histoName,
                            nov = 0,
                            level = level)

############################################################################################

algZ = EventSelection('EventSelectionZ')
algZ.selectionZ = True
algZ.selectionFakes = False
algZ.doTrigger  = True
algZ.set_pidname( 'el_lhVLoose' )
algZ.setId(eventLooper1.id())
algZ.setId(eventLooper2.id())
algZ.l2EtCut = 15
algZ.offEtCut = 15

from TrigEgammaDevelopments.tools import DistributionTool, EmulationTool

# Create emulation Ringer tool
algEmu = EmulationTool( "EmulationTool" )
algEmu.setId(eventLooper1.id())
algEmu.setId(eventLooper2.id())
algEmu.doTrigger = True

calibPath = '../../data/Online/mc15_20170221_v6'
pidnames  = ['Tight','Medium','Loose','VeryLoose']
# create all ringer emulators
discrList=[]
for pidname in pidnames:
  selector = CaloRingerSelectorTool( ('EFCalo_isRinger%s_v6')%(pidname.replace('Very','V')))
  selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname))
  selector.calibPath = calibPath
  algname =  ('EFCalo_isRinger%s_v6')%(pidname.replace('Very','V'))
  algEmu.add_trigger_selector( algname, selector )
  discrList.append(algname)



alg = DistributionTool('DistributionTool')
alg.setMCId(eventLooper1.id())
alg.setDataId(eventLooper2.id())
alg.setId(eventLooper1.id())
alg.setId(eventLooper2.id())
alg.setDiscriminantList( discrList )
alg.doTrigger = True


############################################################################################

from TrigEgammaDevelopments import job

job.push_back(eventLooper1)
job.push_back(eventLooper2)
job.push_back(algZ)
job.push_back(algEmu)
job.push_back(alg)

# Start!
job.initialize()
job.execute()
job.finalize()

#from ROOT import kAzure
#alg.plot(basecolor=kAzure+7)



