
__all__ = ['EDM']

from RingerCore import Logger
from TrigEgammaDevelopments.StatusCode    import StatusCode
from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum

class EDM(Logger):

  # set the default skimmed dataframe
  _dataframe = DataframeEnum.SkimmedNtuple
  
  def __init__(self):
    Logger.__init__(self)
    self._decoration = dict()
    self._tree  = {}
    self._event = {}
    self._containersSvc = {}

  def setSvc( self, c):
    self._containersSvc = c

  def initialize(self):
    return StatusCode.SUCCESS

  def execute(self):
    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS

  @property
  def dataframe(self):
    return self._dataframe

  @dataframe.setter
  def dataframe(self, v):
    self._dataframe=v

  @property
  def tree(self):
    self._tree

  @tree.setter
  def tree(self, v):
    self._tree = v

  @property
  def event(self):
    return self._event

  @event.setter 
  def event(self, v):
    self._event = v

  def setDecor(self, key, v):
    self._decoration[key] = v

  def getDecor(self,key):
    try:
      return self._decoration[key]
    except KeyError:
      self._logger.warning('Decoration %s not found',key)

  def clearDecorations(self):
    self._decoration = dict()

  def decorations(self):
    return self._decoration.keys()

  def setBranchAddress( self, tree, varname, holder ):
    " Set tree branch varname to holder "
    if not tree.GetBranchStatus(varname):
      tree.SetBranchStatus( varname, True )
      from ROOT import AddressOf
      tree.SetBranchAddress( varname, AddressOf(holder, varname) )
      self._debug("Set %s branch address on %s", varname, tree )
    else:
      self._debug("Already set %s branch address on %s", varname, tree)

  def retrieve(self, key):
    try:
      return self._containersSvc[key]
    except KeyError:
      self._logger.warning('Container %s not found',key)

