# Job options for standalone and Tier0 running of AnalysisTools 
# Authors: 
# Ryan Mackenzie White <ryan.white@cern.ch>
# 
# Tool and algorithm configuration done using egamma Factories
# Default configurations found in TrigEgammaAnalysisToolsConfig
#
# To run
# athena -l DEBUG -c "DIR='/afs/cern.ch/work/j/jolopezl/datasets/valid1.147406.PowhegPythia8_AZNLO_Zee.recon.AOD.e3099_s2578_r6220_tid05203475_00'" 
#                 -c "NOV=50" test_ZeeElectronLowPtSupportingTrigAnalysis.py
# where NOV is the number of events to run

from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
from RecExConfig.RecFlags import rec
from RecExConfig.RecAlgsFlags import recAlgs
from AthenaCommon.AppMgr import ToolSvc

import os

print 'e.g: athena -c "DIR=path" -c "NOV=50"  testTrigEgammaExpertAnalysisTools.py'


doEmulation=False

#print 'Set some variables for job'
dirtouse = str()
finallist=[]
grllist=[]

if 'FILE' in dir() :
     finallist.append(FILE)

if 'DIR' in dir() :
     dirtouse=DIR      
     print 'DIR = ',dirtouse
     while( dirtouse.endswith('/') ) :
          dirtouse= dirtouse.rstrip('/')
     listfiles=os.listdir(dirtouse)
     for ll in listfiles:
          finallist.append(dirtouse+'/'+ll)

if 'NOV' in dir():
    nov=NOV
else :
    nov=200

if 'GRL' in dir():
  grllist.append(GRL)
else:
  #grllist.append('/afs/cern.ch/work/j/jodafons/public/data/data15_13TeV.periodAllYear_DetStatus-v79-repro20-02_DQDefects-00-02-02_PHYS_StandardGRL_All_Good_25ns.xml')
  grllist.append('data15_13TeV.periodAllYear_DetStatus-v79-repro20-02_DQDefects-00-02-02_PHYS_StandardGRL_All_Good_25ns.xml')
  #grllist.append('/afs/cern.ch/work/j/jodafons/public/data/data16_13TeV.periodAllYear_DetStatus-v81-pro20-10_DQDefects-00-02-02_PHYS_StandardGRL_All_Good_25ns.xml')
  grllist.append('data16_13TeV.periodAllYear_DetStatus-v81-pro20-10_DQDefects-00-02-02_PHYS_StandardGRL_All_Good_25ns.xml')


print  finallist 
athenaCommonFlags.FilesInput=finallist
athenaCommonFlags.EvtMax=nov
rec.readAOD=True
# switch off detectors
rec.doForwardDet=False
rec.doInDet=False
rec.doCalo=False
rec.doMuon=False
rec.doEgamma=False
rec.doTrigger = True; recAlgs.doTrigger=False # disable trigger (maybe necessary if detectors switched off)
rec.doMuon=False
rec.doMuonCombined=False
rec.doWriteAOD=True
rec.doWriteESD=False
rec.doDPD=False
rec.doTruth=False

# autoconfiguration might trigger undesired feature
rec.doESD.set_Value_and_Lock(False) # uncomment if do not run ESD making algorithms
rec.doWriteESD.set_Value_and_Lock(False) # uncomment if do not write ESD
rec.doAOD.set_Value_and_Lock(True) # uncomment if do not run AOD making algorithms
rec.doWriteAOD.set_Value_and_Lock(False) # uncomment if do not write AOD
rec.doWriteTAG.set_Value_and_Lock(False) # uncomment if do not write TAG

# main jobOption
include ("RecExCommon/RecExCommon_topOptions.py")
MessageSvc.debugLimit = 20000000
MessageSvc.infoLimit  = 20000000
# TDT
from TrigDecisionTool.TrigDecisionToolConf import Trig__TrigDecisionTool
ToolSvc += Trig__TrigDecisionTool( "TrigDecisionTool" )
ToolSvc.TrigDecisionTool.TrigDecisionKey='xTrigDecision'


from AthenaCommon.AlgSequence import AlgSequence, AthSequencer
topSequence = AlgSequence()


##################################### GRL Tools ##########################################
# Good Run List (GRL)
#from RecExConfig.InputFilePeeker import inputFileSummary
#if inputFileSummary['evt_type'][0] == "IS_DATA":
#  print 'IS_DATA! doGRL'
#  from GoodRunsLists.GoodRunsListsConf import *
#  ToolSvc += GoodRunsListSelectorTool()
#  GoodRunsListSelectorTool.GoodRunsListVec = grllist 
#  from GoodRunsListsUser.GoodRunsListsUserConf import *
#  seq = AthSequencer("AthFilterSeq")
#  seq += GRLTriggerSelectorAlg('GRLTriggerAlg1')
#  seq.GRLTriggerAlg1.GoodRunsListArray = ['PHYS_StandardGRL_All_Good_25ns']  




from AthenaMonitoring.AthenaMonitoringConf import AthenaMonManager
topSequence += AthenaMonManager( "HLTMonManager")
HLTMonManager = topSequence.HLTMonManager

################ Mon Tools #################
#Global HLTMonTool

from TrigHLTMonitoring.TrigHLTMonitoringConf import HLTMonTool
HLTMon = HLTMonTool(name  = 'HLTMon', histoPathBase = "HLT");

ToolSvc += HLTMon;
HLTMonManager.AthenaMonTools += [ "HLTMonTool/HLTMon" ];
    
from TrigEgammaAnalysisTools.TrigEgammaAnalysisToolsConfig import TrigEgammaNavTPNtuple, TrigEgammaPlotTool
from TrigEgammaAnalysisTools.TrigEgammaProbelist           import monitoring_mam, monitoring_electron, monitoring_photon 
from TrigEgammaAnalysisTools.TrigEgammaProbelist           import monitoringTP_electron_extra,  triggerTags,\
    probeListLowMidPtSupportingTriggers,probeListHighPtSupportingTriggers
#Define the base path for all histograms
basePath = '/HLT/Egamma'

#Configure the TrigEgammaPlotTool
PlotTool = TrigEgammaPlotTool.copy( name="TrigEgammaPlotTool",
                                    DirectoryPath=basePath,
                                    MaM=monitoring_mam,
                                    Efficiency=["eff_et","eff_eta","eff_mu"],
                                    Distribution=["et","eta","d0","d0sig"],
                                    Resolution=["res_et","res_eta","res_Rhad","res_Rphi","res_Reta"])

triggerList = ['HLT_e24_lhmedium_nod0_iloose',
               'HLT_e24_lhmedium_nod0_ringer_iloose',
               'HLT_e28_lhtight_nod0_iloose',
               'HLT_e29_lhtight_nod0_ringer_iloose']


#from TrigEgammaEmulationTool.TrigEgammaEmulationToolConfig import TrigEgammaEmulationTool
#EmulationElectronTool = TrigEgammaEmulationTool( name="TrigEgammaEmulationTool",
#                                                 TriggerList = triggerList,
#                                                 OutputLevel=0)

Tool = TrigEgammaNavTPNtuple( name='NavTPNtuple',
                              Analysis='Probes',
                              PlotTool=PlotTool,
                              File="",
                              OutputLevel=0  ,
                              DetailedHistograms=True,
                              isEMResultNames=["Tight","Medium","Loose"],
                              LHResultNames=["LHTight","LHMedium","LHLoose"],
                              ZeeLowerMass=80,
                              ZeeUpperMass=100,
                              OfflineTagSelector='Tight', # 1=tight, 2=medium, 3=loose
                              OfflineProbeSelector='Loose', 
                              ForceProbePid=False, 
                              OppositeCharge=True,
                              OfflineTagMinEt=25,
                              OfflineProbeMinEt=24,
                              TagTriggerList=triggerTags,
                              TriggerList=triggerList,
                              )

Tools=['TrigEgammaNavTPNtuple/NavTPNtuple']

from TrigEgammaAnalysisTools.TrigEgammaAnalysisToolsConf import TrigEgammaMonTool
TrigEgammaMonTool = TrigEgammaMonTool( name = "HLTEgammaMon", 
                                       histoPathBase=basePath,
                                       Tools=Tools)
ToolSvc += TrigEgammaMonTool

#TrigEgammaMonToolConfig.TrigEgammaMonTool()
HLTMonManager.AthenaMonTools += [ "TrigEgammaMonTool/HLTEgammaMon" ]
HLTMonManager.FileKey = "GLOBAL"


    
