#!/usr/bin/python
# vim: set fileencoding=utf-8 :

doCaloRinger = False #Ringer Offline

########################### SOME RINGER CONFIG ##########################
#########################################################################
if doCaloRinger:
  from CaloRingerAlgs.CaloRingerFlags import jobproperties
  CaloRingerFlags = jobproperties.CaloRingerFlags
  CaloRingerFlags.useAsymBuilder.set_Value_and_Lock(False)
  CaloRingerFlags.doElectronIdentification.set_Value_and_Lock(False)
  CaloRingerFlags.doPhotonIdentification.set_Value_and_Lock(False)
  #CaloRingerFlags.OutputLevel.set_Value_and_Lock(DEBUG)
#########################################################################

####################### CHANGE CONFIGURATION HERE  ######################
#########################################################################
localRunOnFolder = 'mc14_13TeV.147406.PowhegPythia8_AZNLO_Zee.recon.RDO.e3059_s1982_s2008_r5993_tid05320067_00/'
doDumpStoreGate = False
#ManualDetDescrVersion = 'ATLAS-R2-2015-03-00-00' # Set to False or empty if you want it to be automatically set.
ManualDetDescrVersion = 'ATLAS-R2-2015-01-01-00' # Set to False or empty if you want it to be automatically set.
#ManualDetDescrVersion = ''
ConditionsTag = "OFLCOND-RUN12-SDR-14"
numEvt = 20
from AtlasGeoModel.SetGeometryVersion import GeoModelSvc
GeoModelSvc.IgnoreTagSupport = True
GeoModelSvc.AtlasVersion = ManualDetDescrVersion
print GeoModelSvc
###########################  REC FLAGS  #################################
from RecExConfig.RecFlags import rec
from RecExConfig.RecAlgsFlags import recAlgs
rec.OutputLevel.set_Value_and_Lock(INFO)
rec.doWriteTAG.set_Value_and_Lock(False)
#rec.doTruth.set_Value_and_Lock(True)
rec.doCBNT.set_Value_and_Lock(False)
#rec.readESD.set_Value_and_Lock(True)
rec.doESD.set_Value_and_Lock(True)
rec.doWriteESD.set_Value_and_Lock(False)
rec.doAOD.set_Value_and_Lock(True)
rec.doWriteAOD.set_Value_and_Lock(True)
rec.doTrigger.set_Value_and_Lock(True)
rec.doJetMissingETTag.set_Value_and_Lock(True) # Needed by T&P
recAlgs.doMissingET.set_Value_and_Lock(True)   # Needed by T&P
#rec.doMuon.set_Value_and_Lock(False)
#rec.doMuonCombined.set_Value_and_Lock(False)
#rec.doTau.set_Value_and_Lock(False)
rec.doPerfMon.set_Value_and_Lock(False)
rec.doDetailedPerfMon.set_Value_and_Lock(False)
rec.doHist.set_Value_and_Lock(False)
rec.doPyDump.set_Value_and_Lock(False)
from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
athenaCommonFlags.AllowIgnoreConfigError = False
#########################################################################

#########################################################################
####################### Some autoconfiguration: #########################
# Add files to input picker if running on local:
if localRunOnFolder:
  import os
  # Put dir for your data here:
  f = os.popen('ls '+localRunOnFolder)
  files = []
  for j in f:
    i = j[0:-1]
    files += [localRunOnFolder+i]
  files.sort()
  from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
  athenaCommonFlags.EvtMax = numEvt
  athenaCommonFlags.FilesInput = files
  athenaCommonFlags.PoolAODOutput = 'AOD.pool.root'
from AthenaCommon.GlobalFlags import globalflags
globalflags.DetGeo = 'atlas'
#here is an example of the inputFilePeeker to autoconfigure the flags
from RecExConfig.InputFilePeeker import inputFileSummary
globalflags.DataSource = 'data' if inputFileSummary['evt_type'][0] == "IS_DATA" else 'geant4'
if not ManualDetDescrVersion:
  globalflags.DetDescrVersion.set_Value_and_Lock(inputFileSummary['geometry'])
else:
  globalflags.DetDescrVersion.set_Value_and_Lock(ManualDetDescrVersion)
globalflags.ConditionsTag.set_Value_and_Lock(ConditionsTag)
#from AthenaCommon.DetFlags import DetFlags
#DetFlags.detdescr.all_setOff() # skip this line out to leave everything on. But this will take longer
#DetFlags.detdescr.Calo_setOn() # e.g. if I am accessing CaloCellContainer, I need the calo detector description
#include("RecExCond/AllDet_detDescr.py")
#########################################################################

########################### PRE-INCLUDE #################################
#########################################################################
# Include Reconstruction pre-includes here.
include('SimulationJobOptions/preInclude.PileUpBunchTrainsUpgradeConfig1_25ns.py')
include('RunDependentSimData/configLumi_run222222.py')
#########################################################################

########################### PRE-EXEC ####################################
#########################################################################
# Insert Reconstruction pre-execs here.
rec.Commissioning.set_Value_and_Lock(True)
from AthenaCommon.BeamFlags import jobproperties
jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(20.0)
jobproperties.Beam.bunchSpacing.set_Value_and_Lock(25)
from LArROD.LArRODFlags import larRODFlags
larRODFlags.doOFCPileupOptimization.set_Value_and_Lock(True)
larRODFlags.NumberOfCollisions.set_Value_and_Lock(20)
larRODFlags.nSamples.set_Value_and_Lock(4)
from CaloRec.CaloCellFlags import jobproperties
jobproperties.CaloCellFlags.doLArCellEmMisCalib=False
#########################################################################

########################### PRE-EXTRA ###################################
#########################################################################
# You may add you own extra stuff in here. An example that may be useful
# follows.
##from AthenaCommon.JobProperties import jobproperties
##jobproperties.Beam.energy.set_Value_and_Lock(7000*Units.GeV)
##jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(27.5)
##jobproperties.Beam.bunchSpacing.set_Value_and_Lock(25)

from TriggerJobOpts.TriggerFlags import TriggerFlags
TriggerFlags.triggerMenuSetup = 'default'
TriggerFlags.readHLTconfigFromXML=False
TriggerFlags.readLVL1configFromXML=False
TriggerFlags.triggerMenuSetup='MC_pp_v6'
TriggerFlags.doHLT=True
TriggerFlags.L1PrescaleSet  = ''
TriggerFlags.HLTPrescaleSet = ''
TriggerFlags.AODEDMSet='AODFULL'

#Custon egamma trigger menu
def egammaOnly():

  triggerTags = [ 
    'HLT_e24_lhmedium_iloose_L1EM18VH',
    'HLT_e24_lhmedium_iloose_L1EM20VH',
    'HLT_e24_lhtight_iloose',
    'HLT_e26_lhtight_iloose',
    'HLT_e24_medium_iloose_L1EM18VH',
    'HLT_e24_medium_iloose_L1EM20VH',
    'HLT_e24_tight_iloose',
    'HLT_e26_tight_iloose'
  ]

  # Lowest single electron triggers for TP analysis
  monitoringTP_electron =[
    'HLT_e24_lhmedium_L1EM18VH',
    'HLT_e24_lhmedium_nod0_L1EM18VH',
    'HLT_e24_lhmedium_nod0_L1EM20VH',
    'HLT_e24_medium_nod0_L1EM20VH',
    'HLT_e24_lhmedium_iloose',
    'HLT_e24_medium_iloose',
    'HLT_e24_lhmedium_nod0_iloose',
    'HLT_e24_lhtight_nod0_iloose',
    'HLT_e24_lhmedium_nod0_ivarloose',
    'HLT_e24_lhtight_nod0_ivarloose',
    'HLT_e24_lhtight_iloose',
    'HLT_e24_tight_iloose',
    'HLT_e26_lhtight_iloose',
    'HLT_e26_lhtight_nod0_iloose',
    'HLT_e26_lhtight_nod0_ivarloose',
    'HLT_e24_lhmedium_nod0_ringer_L1EM20VH',
    'HLT_e24_lhmedium_nod0_ringer_iloose',
    'HLT_e24_lhtight_nod0_ringer_iloose',
    'HLT_e24_lhmedium_nod0_ringer_ivarloose',
    'HLT_e24_lhtight_nod0_ringer_ivarloose',
    'HLT_e26_lhtight_nod0_ringer_iloose',
    'HLT_e26_lhtight_nod0_ringer_ivarloose',
    'HLT_e28_lhtight_nod0_iloose',
  ] 

  triggerList = list(set(monitoringTP_electron+triggerTags)) #Protection to duplicate chains
  current = TriggerFlags.EgammaSlice.signatures.get_Value()
  TriggerFlags.Slices_all_setOff()
  #Searching for: "Registered chain" into athena log file to check the chains
  TriggerFlags.EgammaSlice.signatures = [trig for trig in current if 'HLT_'+trig[0] in triggerList]
  


from TriggerMenu.menu.GenerateMenu import GenerateMenu
GenerateMenu.overwriteSignaturesWith(egammaOnly)
#########################################################################

################## MAIN REC JOBOPTION INCLUDE: ##########################
#########################################################################
include( "RecExCommon/RecExCommon_topOptions.py" )
#########################################################################

###########################  Ringer!!! ##################################
#########################################################################
if doCaloRinger:
  include('CaloRingerAlgs/CaloRinger_reconstruction.py') 
#########################################################################

########################### POST-INCLUDE ################################
#########################################################################
# Insert Reconstruction post-includes here.
include( "RecJobTransforms/UseFrontier.py")
#########################################################################

########################### POST-EXEC ###################################
#########################################################################
# Insert Reconstruction post-execs here.
CfgMgr.MessageSvc().setError+=["HepMcParticleLink"]
xAODMaker__xAODTruthCnvAlg("GEN_AOD2xAOD",WriteInTimePileUpTruth=True)
#########################################################################

########################### POST-EXTRA ##################################
#########################################################################
if doDumpStoreGate:
  StoreGateSvc = Service( "StoreGateSvc" )                     
  StoreGateSvc.Dump = True  #true will dump data store contents
  StoreGateSvc.OutputLevel = DEBUG
#########################################################################
