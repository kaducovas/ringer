
__all__ = ['Electron','ElectronCandidate', 'EgammaPid', 'EgammaPidEnum']

from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.dataframe.EDM import EDM
from TrigEgammaDevelopments.StatusCode    import StatusCode

class ElectronCandidate(object):
  Tag   = 1
  Probe = 2
  Fake  = 3

class EgammaPid(object):
  Likelihood = 0
  IsEM = 1
  Ringee = 2

class EgammaPidEnum(object):
  VeryLoose = 'vloose'
  Loose     = 'loose'
  Medium    = 'medium'
  Tight     = 'tight'


class Electron(EDM):

  # define all skimmed branches here.
  __eventBranches = {
      "SkimmedNtuple" : [ # default skimmed ntuple branches
                         'isTightLLHCaloMC14',
                         'isMediumLLHCaloMC14',
                         'isLooseLLHCaloMC14',
                         'isVeryLooseLLHCaloMC14',
                         'isTightLLHCaloMC14Truth',
                         'isMediumLLHCaloMC14Truth',
                         'isLooseLLHCaloMC14Truth',
                         'isVeryLooseLLHCaloMC14Truth',
                         'isTightLLHCalo_v11',
                         'isMediumLLHCalo_v11',
                         'isLooseLLHCalo_v11',
                         'isVeryLooseLLHCalo_v11',
                         'isEMTight2015', 
                         'isEMMedium2015',
                         'isEMLoose2015', 
                         'pt',
                         'et', 
                         'eta', 
                         'phi', 
                         'reta', 
                         'eratio' , 
                         'weta2', 
                         'rhad', 
                         'rphi' ,
                         'f1', 
                         'f3', 
                         'ringer_rings'],
      "PhysVal"       : ['el_lhTight',
                         'el_lhMedium', 
                         'el_lhLoose', 
                         'el_lhVLoose', 
                         'el_tight',
                         'el_medium',
                         'el_loose', 
                         'el_et',
                         'el_eta', 
                         'el_phi',
                         'el_f1',
                         'el_f3',
                         'el_weta2',
                         'el_Eratio',
                         'el_Reta',
                         'el_Rhad',
                         'el_Rphi',
                         'el_ringsE']
                }

  def __init__(self):

    EDM.__init__(self)
    # this is use only for SkimmedNtuple
    self._elCand = ElectronCandidate.Probe # Default is probe
  
  
  @property
  def candidate(self, v):
    return self._elCand

  # Use this only for skimmed ntuple dataframe
  # Default is 2 (probes)
  @candidate.setter
  def candidate(self, v):
    self._elCand = v

  def initialize(self):
    try:
      if self._dataframe is DataframeEnum.SkimmedNtuple:
        # Link all branches 
        for branch in self.__eventBranches["SkimmedNtuple"]:
      	  self.setBranchAddress( self._tree, ('elCand%d_%s')%(self._elCand, branch)  , self._event)
      elif self._dataframe is DataframeEnum.PhysVal:
        for branch in self.__eventBranches["PhysVal"]:
      	  self.setBranchAddress( self._tree, branch  , self._event)
      else:
      	self._logger.warning( "Electron object can''t retrieved" )
        return StatusCode.FAILURE
      # Success
      return StatusCode.SUCCESS
    except:
      self._logger.warning("Impossible to create the Electron Container")
      return StatusCode.FAILURE


  @property
  def et(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_et')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_et
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  @property
  def eta(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_eta')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_eta
    else:
      self._logger.warning("Impossible to retrieve the value of Eta. Unknow dataframe.")

  @property
  def phi(self):
    """
      Retrieve the Phi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_phi')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_phi
    else:
      self._logger.warning("Impossible to retrieve the value of Phi. Unknow dataframe.")


  @property
  def ringer_rings(self):
    """
      Retrieve the Ringer Rings information from Physval or SkimmedNtuple
    """
    from RingerCore import stdvector_to_list
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return stdvector_to_list(getattr(self._event, ('elCand%d_ringer_rings')%(self._elCand)))
    elif self._dataframe is DataframeEnum.PhysVal:
      return stdvector_to_list(self._event.el_ringsE)
    else:
      self._logger.warning("Impossible to retrieve the value of ringer rings. Unknow dataframe.")

  # Check if this object has rings
  def isGoodRinger(self):
    from RingerCore import stdvector_to_list
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      rings = stdvector_to_list(getattr(self._event, ('elCand%d_ringer_rings')%(self._elCand)))
      return True if len(rings)!=0 else False
    elif self._dataframe is DataframeEnum.PhysVal:
      rings = stdvector_to_list(self._event.el_ringsE)
      return True if len(rings)!=0 else False
    else:
      self._logger.warning("Impossible to retrieve the value of ringer rings. Unknow dataframe.")


  @property
  def reta(self):
    """
      Retrieve the Reta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_reta')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_Reta
    else:
      self._logger.warning("Impossible to retrieve the value of Reta. Unknow dataframe")

  @property
  def eratio(self):
    """
      Retrieve the eratio information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_eratio')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_Eratio
    else:
      self._logger.warning("Impossible to retrieve the value of eratio. Unknow dataframe")


  @property
  def weta2(self):
    """
      Retrieve the weta2 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_weta2')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_weta2
    else:
      self._logger.warning("Impossible to retrieve the value of weta2. Unknow dataframe")


  @property
  def rhad(self):
    """
      Retrieve the rhad information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_rhad')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_Rhad
    else:
      self._logger.warning("Impossible to retrieve the value of rhad. Unknow dataframe")

  @property
  def rphi(self):
    """
      Retrieve the rphi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_rphi')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_Rphi
    else:
      self._logger.warning("Impossible to retrieve the value of rphi. Unknow dataframe")


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



  @property
  def f1(self):
    """
      Retrieve the f1 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_f1')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_f1
    else:
      self._logger.warning("Impossible to retrieve the value of f1. Unknow dataframe")


  @property
  def f3(self):
    """
      Retrieve the f3 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, ('elCand%d_f3')%(self._elCand))
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_f3
    else:
      self._logger.warning("Impossible to retrieve the value of f3. Unknow dataframe")

    
  def ApplyElectronSelection( self,  pidname ):
    """
      Retrieve the pid selection from electron dataframe.
      There is two possibility,
      From SkimmedNtuple:
        see: https://github.com/wsfreund/TuningTools/blob/master/TuningTools/SkimmedNtuple.h#L41
      From PhysVal:
        Tight, Medium, Loose, LHTight, LHMedium and LHLoose
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      if pidname in self.__eventBranches["SkimmedNtuple"]:
        return bool(getattr(self._event, ('elCand%d_%s')%(self._elCand,pidname)))
      elif pidname in self.decorations():
        return bool(self.getDecor(pidname))
      else:
        return False
    elif self._dataframe is DataframeEnum.PhysVal:
      # Dictionary to acess the physval dataframe
      if pidname in self.__eventBranches['PhysVal']:
        return bool(getattr(self._event, pidname))
      elif pidname in self.decorations():
        return bool(self.getDecor(pidname))
      else:
        return False
    else:
      self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")


  def execute(self):
    if self._dataframe is DataframeEnum.PhysVal:
      self._logger.debug('Appling Electron decoration ')
      self.setDecor('isLHTight' , self.ApplyElectronSelection( "el_lhTight" )  )
      self.setDecor('isLHMedium', self.ApplyElectronSelection( "el_lhMedium" ) )
      self.setDecor('isLHLoose' , self.ApplyElectronSelection( "el_lhLoose" )  )
      self.setDecor('isLHVLoose', self.ApplyElectronSelection( "el_lhVLoose" )  )
      self.setDecor('isTight' ,   self.ApplyElectronSelection( "el_tight" )  )
      self.setDecor('isMedium',   self.ApplyElectronSelection( "el_medium" ) )
      self.setDecor('isLoose' ,   self.ApplyElectronSelection( "el_loose" )  )
      self.setDecor('isVLoose',   self.ApplyElectronSelection( "el_loose" )  )
    
    elif self._dataframe is DataframeEnum.SkimmedNtuple:
      #self.setDecor('isTight' , self.self.ApplyElectronSelection( "" )  )
      #self.setDecor('isMedium', self.self.ApplyElectronSelection( "" ) )
      #self.setDecor('isLoose' , self.self.ApplyElectronSelection( "" )  )
      #self.setDecor('isVLoose', self.self.ApplyElectronSelection( "" )  )
      pass
    else:
      self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")
      return StatusCode.FAILURE
    
    return StatusCode.SUCCESS










