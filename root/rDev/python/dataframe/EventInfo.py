
__all__ = ['EventInfo']

from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.dataframe.EDM import EDM
from TrigEgammaDevelopments.StatusCode    import StatusCode


class EventInfo(EDM):

  __eventBranches = { 'SkimmedNtuple': 
                    [ 'EventNumber',
                      'RunNumber',
                      'RandomRunNumber',
                      'MCChannelNumber',
                      'RandomLumiBlockNumber',
                      'MCPileupWeight',
                      'VertexZPosition',
                      'Zcand_M',
                      'Zcand_pt',
                      'Zcand_eta',
                      'Zcand_phi',
                      'Zcand_y',
                      'isTagTag',
                      'Nvtx',
                      'averageIntPerXing'],
                      'PhysVal':
                     [ 'RunNumber',
                       'avgmu',
                       'el_nPileupPrimaryVtx'],
                      }

  def __init__(self):
    EDM.__init__(self)


  def initialize(self):
    try:
      if self._dataframe is DataframeEnum.SkimmedNtuple:
        # Link all branches 
        for branch in self.__eventBranches["SkimmedNtuple"]:
      	  self.setBranchAddress( self._tree, branch, self._event)
      elif self._dataframe is DataframeEnum.PhysVal:
        for branch in self.__eventBranches["PhysVal"]:
      	  self.setBranchAddress( self._tree, branch , self._event)
      else:
      	self._logger.warning( "Electron object can''t retrieved" )
        return StatusCode.FAILURE
      # Success
      return StatusCode.SUCCESS
    except:
      self._logger.warning("Impossible to create the EventInfo Container")
      return StatusCode.SUCCESS

  @property
  def nvtx(self):
    """
      Retrieve the Nvtx information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return self._event.Nvtx
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.el_nPileupPrimaryVtx
    else:
      self._logger.warning("Impossible to retrieve the value of nvtx. Unknow dataframe.")

  @property
  def avgmu(self):
    """
      Retrieve the avgmu information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return self._event.averageIntPerXing
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.avgmu
    else:
      self._logger.warning("Impossible to retrieve the value of avgmu. Unknow dataframe.")

  @property
  def RunNumber(self):
    """
      Retrieve the avgmu information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      return self._event.RunNumber
    elif self._dataframe is DataframeEnum.PhysVal:
      return self._event.RunNumber
    else:
      self._logger.warning("Impossible to retrieve the value of avgmu. Unknow dataframe.")

  def setId( self, id):
    self._id = id

  def id(self):
    return self._id





