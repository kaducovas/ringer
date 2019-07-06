
__all__ = ['MonteCarlo']

from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.dataframe.EDM import EDM
from TrigEgammaDevelopments.dataframe.Electron import ElectronCandidate
from TrigEgammaDevelopments.StatusCode    import StatusCode

class MonteCarlo(EDM):

  __eventBranches = {
                    'SkimmedNtuple':[
                        'type',
                        'origin',
                        'originbkg',
                        'typebkg',
                        'isTruthElectronFromZ',
                        'TruthParticlePdgId',
                        'firstEgMotherPdgId',
                        'TruthParticleBarcode',
                        'firstEgMotherBarcode',
                        'MotherPdgId',
                        'MotherBarcode',
                        'FirstEgMotherTyp',
                        'FirstEgMotherOrigin',
                        'dRPdgId',
                       ],
                    'PhysVal':[
                      'mc_hasMC',
                      'mc_isElectron',
                      'mc_hasZMother',
                      'mc_hasWMother',
                      ]
                    }


  def __init__(self):
    EDM.__init__(self)
    # this is use only for SkimmedNtuple
    self._elCand = ElectronCandidate.Probe  # Default is probe
 
  
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
      	  self.setBranchAddress( self._tree, ('%s')%(branch)  , self._event)
      else:
        self._logger.warning( "Electron object can''t retrieved" )
        return StatusCode.FAILURE
        # Success
      return StatusCode.SUCCESS
    except:
      self._logger.warning("Impossible to create the MonteCarlo Container")
      return StatusCode.FAILURE


  def isEfromZ(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return getattr(self._event, 'isTruthElectronFromZ')
    elif self._dataframe is DataframeEnum.PhysVal:
      return (self._event.mc_isElectron and self._event.mc_hasZMother)
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")


  def isMC(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return False
      #return getattr(self._event, 'isTruthElectronFromZ')
    elif self._dataframe is DataframeEnum.PhysVal:
      return bool(self._event.mc_hasMC)
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")





