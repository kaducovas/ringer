

__all__ = ['createEmulation_trigger_20170221_v6']


# Create emulation Ringer tool
def createEmulation_trigger_20170221_v6( ):

  import os
  basepath = os.environ['ROOTCOREBIN']
  # this cannot be modified
  calibPath = basepath+'/../TrigEgammaDevelopments/data/Online/mc15_20170221_v6'
  from TrigEgammaDevelopments.selector.SelectorAlgTool  import CaloRingerSelectorTool, egammaRingerPid 
  from TrigEgammaDevelopments.tools import EmulationTool
  # create emulation tool
  alg = EmulationTool( "EmulationTool_v6" )  
  pidnames  = ['Tight','Medium','Loose','VLoose']
  algSelectors={}
  # Loop over pids
  for pidname in pidnames:
    # create the selector tool
    selector = CaloRingerSelectorTool( ('EFCalo_isRinger%s_v6')%(pidname) )
    selector.pidname = getattr(egammaRingerPid,('Electron%s')%(pidname.replace('V','Very')))
    selector.calibPath = calibPath
    algname =  ('EFCalo_isRinger%s_v6')%(pidname)
    algSelectors[pidname] = (algname, selector)
    # add new selector tool into the emulation tool
    alg.add_trigger_selector( algname, selector )
  # return tool and algorithm names emulated
  return alg, algSelectors





