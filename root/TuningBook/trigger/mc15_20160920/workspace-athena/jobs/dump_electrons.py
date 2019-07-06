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


#print 'Set some variables for job'
dirtouse = str()
finallist=[]

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
    nov=-1

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
rec.doWriteAOD.set_Value_and_Lock(True) # uncomment if do not write AOD
rec.doWriteTAG.set_Value_and_Lock(False) # uncomment if do not write TAG

# main jobOption
include ("RecExCommon/RecExCommon_topOptions.py")
MessageSvc.debugLimit = 20000000
MessageSvc.infoLimit  = 20000000
# TDT
from TrigDecisionTool.TrigDecisionToolConf import Trig__TrigDecisionTool
ToolSvc += Trig__TrigDecisionTool( "TrigDecisionTool" )
ToolSvc.TrigDecisionTool.TrigDecisionKey='xTrigDecision'

from AthenaCommon.AlgSequence import AlgSequence
topSequence = AlgSequence()

from AthenaMonitoring.AthenaMonitoringConf import AthenaMonManager
topSequence += AthenaMonManager( "HLTMonManager")
HLTMonManager = topSequence.HLTMonManager

################ Mon Tools #################
#Global HLTMonTool

from TrigHLTMonitoring.TrigHLTMonitoringConf import HLTMonTool
HLTMon = HLTMonTool(name  = 'HLTMon', histoPathBase = "HLT");

ToolSvc += HLTMon;
HLTMonManager.AthenaMonTools += [ "HLTMonTool/HLTMon" ];
    
from TrigEgammaAnalysisTools.TrigEgammaAnalysisToolsConfig import TrigEgammaNavNtuple, \
                                                                  TrigEgammaPlotTool

from TrigEgammaAnalysisTools.TrigEgammaProbelist           import monitoring_mam, monitoring_electron, monitoring_photon 
from TrigEgammaAnalysisTools.TrigEgammaProbelist           import monitoringTP_electron_extra,  triggerTags 
#Define the base path for all histograms
basePath = '/HLT/Egamma'

#Configure the TrigEgammaPlotTool
PlotTool = TrigEgammaPlotTool.copy( name="TrigEgammaPlotTool",
                                    DirectoryPath=basePath,
                                    MaM=monitoring_mam,
                                    Efficiency=["eff_et","eff_eta","eff_mu"],
                                    Distribution=["et","eta","d0","d0sig"],
                                    Resolution=["res_et","res_eta","res_Rhad","res_Rphi","res_Reta"])

Tool = TrigEgammaNavNtuple( name ="NavNtuple",
                            Analysis='Electrons',
                            ElectronKey = 'Electrons',
                            PlotTool=PlotTool,
                            TriggerList=[],
                            DoOfflineDump=True,
                            ForcePidSelection=False,
                            ForceProbeIsolation=False,
                            ForceEtThreshold=False,
                            ForceMCEnhancedBias=False,
                            RemoveCrack=False)

Tools=['TrigEgammaNavNtuple/NavNtuple']

from TrigEgammaAnalysisTools.TrigEgammaAnalysisToolsConf import TrigEgammaMonTool
TrigEgammaMonTool = TrigEgammaMonTool( name = "HLTEgammaMon", 
                                       histoPathBase=basePath,
                                       Tools=Tools)
ToolSvc += TrigEgammaMonTool

#TrigEgammaMonToolConfig.TrigEgammaMonTool()
HLTMonManager.AthenaMonTools += [ "TrigEgammaMonTool/HLTEgammaMon" ]
HLTMonManager.FileKey = "GLOBAL"


    
