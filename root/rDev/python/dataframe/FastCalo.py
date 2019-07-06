
__all__ = ['FastCalo']

from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.dataframe.EDM import EDM
from TrigEgammaDevelopments.StatusCode    import StatusCode
from RingerCore import stdvector_to_list

class FastCalo(EDM):

  __eventBranches = { 'SkimmedNtuple': 
                    [ 'match',
                      'eta',
                      'phi',
                      'et',
                      'ethad1',
                      'wtots1',
                      'e237',
                      'e277',
                      'ringerMatch',
                      ],
                      'PhysVal':
                    [
                      'trig_L1_emClus',
                      #'trig_L1_thrNames',
                      'trig_L2_calo_et',
                      'trig_L2_calo_eta',
                      'trig_L2_calo_phi',
                      'trig_L2_calo_e237',
                      'trig_L2_calo_e277',
                      'trig_L2_calo_weta2',
                      'trig_L2_calo_ehad1',
                      'trig_L2_calo_wstot',
                      'trig_L2_calo_rings',
                      #'trig_L2_calo_rgtight_rnnOutput',
                      #'trig_L2_calo_rgmedium_rnnOutput',
                      #'trig_L2_calo_rgloose_rnnOutput',
                      #'trig_L2_calo_rgvloose_rnnOutput',
                    ]
                      }

  __selectors = [
                  'L2Calo_isEMTight',
                  'L2Calo_isEMMedium',
                  'L2Calo_isEMLoose',
                  'L2_isEMTight',
                  'L2_isEMMedium',
                  'L2_isEMLoose',
                  'EFCalo_isLHTightCaloOnly_rel21_20170214',
                  'EFCalo_isLHMediumCaloOnly_rel21_20170214',
                  'EFCalo_isLHLooseCaloOnly_rel21_20170214',
                  'EFCalo_isLHVLooseCaloOnly_rel21_20170214',
                  'EFCalo_isLHTightCaloOnly_rel21_20170217',
                  'EFCalo_isLHMediumCaloOnly_rel21_20170217',
                  'EFCalo_isLHLooseCaloOnly_rel21_20170217',
                  'EFCalo_isLHVLooseCaloOnly_rel21_20170217',
                  'EFCalo_isLHTightCaloOnly_rel21_20170217_mc16a',
                  'EFCalo_isLHMediumCaloOnly_rel21_20170217_mc16a',
                  'EFCalo_isLHLooseCaloOnly_rel21_20170217_mc16a',
                  'EFCalo_isLHVLooseCaloOnly_rel21_20170217_mc16a',
                  'HLT_isLHVLoose_rel21_20170217',
                  'HLT_isLHLoose_rel21_20170217',
                  'HLT_isLHMedium_rel21_20170217',
                  'HLT_isLHTight_rel21_20170217',
                  'HLT_isLHTight_rel21_20170217_mc16a',
                ]

  def __init__(self):
    EDM.__init__(self)
    # this is use only for SkimmedNtuple
    self._fcCand = 2 # Default is probe
    self.__eventBranches['PhysVal'].extend(self.__selectors)
 
  @property
  def candidate(self, v):
    return self._fcCand

  # Use this only for skimmed ntuple dataframe
  # Default is 2 (probes)
  @candidate.setter
  def candidate(self, v):
    self._fcCand = v


  def initialize(self):
    try:
      if self._dataframe is DataframeEnum.SkimmedNtuple:
        # Link all branches 
        for branch in self.__eventBranches["SkimmedNtuple"]:
      	  self.setBranchAddress( self._tree, ('fcCand%d_%s')%(self._fcCand,branch), self._event)
      elif self._dataframe is DataframeEnum.PhysVal:
        for branch in self.__eventBranches["PhysVal"]:
          self.setBranchAddress( self._tree, branch , self._event)
      else:
        self._logger.warning( "FastCalo object can''t retrieved" )
        return StatusCode.FAILURE
      
      return StatusCode.SUCCESS
    except:
      self._logger.warning("Impossible to create the FastCalo Container")
      return StatusCode.SUCCESS

  def L1EmClus(self):
    """
      Retrieve the L1 EmClus information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return 
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.trig_L1_emClus
    else:
      self._logger.warning("Impossible to retrieve the value of L1 EmClus. Unknow dataframe")

  def L1ThrName(self, thrname):
    """
      Retrieve the L1 ThrNames information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return 
    elif self._dataframe is DataframeEnum.PhysVal:
      from RingerCore import stdvector_to_list
      thrNames = stdvector_to_list(self._event.trig_L1_thrNames)
      return True if thrname in thrNames else False
    else:
      self._logger.warning("Impossible to retrieve the value of L1 thrNames. Unknow dataframe")

  @property
  def ringer_rings(self):
    """
      Retrieve the L2Calo Ringer Rins information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return 
    elif self._dataframe is DataframeEnum.PhysVal:
      return stdvector_to_list(self._event.trig_L2_calo_rings)
    else:
      self._logger.warning("Impossible to retrieve the value of L2Calo Ringer Rings. Unknow dataframe")

  # Check if this object has rings
  def isGoodRinger(self):
    from RingerCore import stdvector_to_list
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      rings = stdvector_to_list(getattr(self._event, ('fcCand%d_ringer_rings')%(self._elCand)))
      return True if len(rings)!=0 else False
    elif self._dataframe is DataframeEnum.PhysVal:
      rings = stdvector_to_list(self._event.trig_L2_calo_rings)
      return True if len(rings)!=0 else False
    else:
      self._logger.warning("Impossible to retrieve the value of ringer rings. Unknow dataframe.")



  @property
  def et(self):
    """
      Retrieve the et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return 
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.trig_L2_calo_et
    else:
      self._logger.warning("Impossible to retrieve the value of et. Unknow dataframe")
  
  @property
  def eta(self):
    """
      Retrieve the eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return 
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.trig_L2_calo_eta
    else:
      self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")

  @property
  def phi(self):
    """
      Retrieve the phi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return 
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.trig_L2_calo_phi
    else:
      self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")




  def getAvgMu(self):
    """
      Retrieve the rphi information from Physval or SkimmedNtuple
    """
    # Retrieve event info to get the pileup information
    eventInfo  = self.retrieve('EventInfo')

    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return eventInfo.nvtx
    elif self._dataframe is DataframeEnum.PhysVal:
      return eventInfo.avgmu
    else:
      self._logger.warning("Impossible to retrieve the value of pileup. Unknow dataframe")




  def ApplyElectronSelection( self,  pidname ):
    """
      Retrieve the pid selection from electron dataframe.
      There is two possibility,
      From SkimmedNtuple:
        see: https://github.com/wsfreund/TuningTools/blob/master/TuningTools/SkimmedNtuple.h#L41
      From PhysVal:
        see TrigEgammaEventSelection
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return False
    elif self._dataframe is DataframeEnum.PhysVal:
      if pidname in self.__eventBranches['PhysVal']:
        return bool(getattr(self._event,pidname))
      # Dictionary to acess the physval dataframe
      elif pidname in self.decorations():
        return bool(self.getDecor(pidname))
      else:
        return False
    else:
      self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")



  def execute(self):
    #el = self.retrieve( "Electron" )
    #if el:
    #  if self._dataframe is DataframeEnum.PhysVal:
    #    self.setDecor('isLHTight' , el.ApplyElectronSelection( "el_lhTight"  ) )
    #    self.setDecor('isLHMedium', el.ApplyElectronSelection( "el_lhMedium" ) )
    #    self.setDecor('isLHLoose' , el.ApplyElectronSelection( "el_lhLoose"  ) )
    #    self.setDecor('isLHVLoose', el.ApplyElectronSelection( "el_lhLoose"  ) )
    #    self.setDecor('isTight'   , el.ApplyElectronSelection( "el_tight"    ) )
    #    self.setDecor('isMedium'  , el.ApplyElectronSelection( "el_medium"   ) )
    #    self.setDecor('isLoose'   , el.ApplyElectronSelection( "el_loose"    ) )
    #    self.setDecor('isVLoose'  , el.ApplyElectronSelection( "el_loose"    ) ) 

    #  elif self._dataframe is DataframeEnum.SkimmedNtuple:
    #    #self.setDecor('isTight' , self.self.ApplyElectronSelection( "" )  )
    #    #self.setDecor('isMedium', self.self.ApplyElectronSelection( "" ) )
    #    #self.setDecor('isLoose' , self.self.ApplyElectronSelection( "" )  )
    #    #self.setDecor('isVLoose', self.self.ApplyElectronSelection( "" )  )
    #    pass
    #  else:
    #    self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")
    #    return StatusCode.FAILURE
    #else:
    #  self._logger.warning("Impossible to retrieve the Electron inside of the store")


    return StatusCode.SUCCESS

  #TODO: Use this for future
  def getRnnOutput(self, pidname):
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return -999
    elif self._dataframe is DataframeEnum.PhysVal:
      return getattr(self._event, ('trig_L2_calo_rg%s_rnnOutput')%(pidname) )
    else:
      self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")



