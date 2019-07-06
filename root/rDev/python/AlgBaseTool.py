
__all__ = ['AlgBaseTool', 'StatusTool', 'StatusWatchDog']

from RingerCore import  Logger
from TrigEgammaDevelopments.StatusCode import StatusCode

class StatusTool(object):
  """
    The status of the tool
  """
  IS_FINALIZED   = 1
  IS_INITIALIZED = 1 
  ENABLE  = 1,
  DISABLE = 0,
  NOT_INITIALIZED = 0
  NOT_FINALIZED = 0
 

class StatusWatchDog(object):
  """
    Use this to enable or disable the tool in execute call
  """
  ENABLE  = 1,
  DISABLE = 0



class AlgBaseTool( Logger ):

  def __init__(self, name):
    Logger.__init__(self)
    self._name = name
    self._basepath = str()
    self._wtd  = StatusWatchDog.DISABLE
    self._status = StatusTool.ENABLE
    self._initialized = StatusTool.NOT_INITIALIZED
    self._finalized = StatusTool.NOT_FINALIZED
    self._ids = []

  def setLvl( self, level ):
    self._level = level

  @property
  def name(self):
    return self._name
 
  @property
  def basepath(self):
    return self._basepath

  @basepath.setter
  def basepath(self, v):
    self._basepath = v

  def setSvc( self, c, s ):
    self._containersSvc = c
    self._storegateSvc  = s

  def retrieve(self, key):
    try:
      return self._containersSvc[key]
    except KeyError:
      self._logger.warning('Container %s not found',key)

  def storeSvc(self):
    return self._storegateSvc

  def setStoreSvc(self, s):
    self._storegateSvc=s

  def initialize(self):
    return StatusCode.SUCCESS

  def execute(self):
    self._wtd = StatusWatchDog.DISABLE
    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS

  @property
  def wtd(self):
    return self._wtd

  @wtd.setter
  def wtd(self, v):
    self._wtd = v

  @property
  def status(self):
    return self._status


  def disable(self):
    self._logger.info('Disable %s tool service.',self._name)
    self._status = StatusTool.DISABLE

  def enable(self):
    self._logger.info('Enable %s tool service.',self._name)
    self._status = StatusTool.ENABLE

  def init_lock(self):
    self._initialized = StatusTool.IS_INITIALIZED

  def fina_lock(self):
    self._finalized = StatusTool.IS_FINALIZED


  def plot(self):
    return StatusCode.SUCCESS


  def isInitialized(self):
    if self._initialized is StatusTool.IS_INITIALIZED:
      return True
    else:
      return False

  def isFinalized(self):
    if self._finalized is StatusTool.IS_FINALIZED:
      return True
    else:
      return False

  def setId(self, id):
    self._ids.append(id)

  def checkId(self, id):
    if id in self._ids:
      return True
    else:
      return False

