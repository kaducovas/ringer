
__all__ = ['EventLooper']

from RingerCore                           import  checkForUnusedVars, retrieve_kw, progressbar, LoggingLevel
from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.EventBase     import EventBase
from TrigEgammaDevelopments.AlgBaseTool   import StatusTool, StatusWatchDog
import ROOT


class EventLooper( EventBase ):

  def __init__(self, **kw):
    EventBase.__init__(self, **kw)
    self._algTools = list()
    self._level = retrieve_kw(kw, 'level', LoggingLevel.INFO)
    #checkForUnusedVars(kw)
    del kw
    self._initialized = StatusTool.NOT_INITIALIZED
    self._finalized = StatusTool.NOT_FINALIZED
    self._logger.info('Created with id (%d)',self._id)


  def setTools( self, tools ):
    self._algTools = tools

  def getTools( self ):
    return self._algTools

  def initialize( self ):
    
    self._logger.info('Initializing all tools...')
    # initialize base class
    if super(EventLooper,self).initialize().isFailure():
      self._logger.fatal("Impossible to initialize the EventLooper services.")

    for alg in self._algTools:
     # Retrieve all services
      c,s = self.getSvc()
      alg.level = self._level
      alg.setSvc( c, s )
      if alg.isInitialized():
        continue
      if alg.initialize().isFailure():
        self._logger.fatal("Impossible to initialize the tool name: %s",alg.name)

    self._init_lock()

  def execute( self ):

    # retrieve values 
    entries = self.getEntries()
    step = int(entries/100) if int(entries/100) > 0 else 1
    
    ### Loop over entries
    for entry in progressbar(range(self._entries), self._entries, 
                 step = step, logger = self._logger,
                 prefix = "Looping over entries "):
      # the number of events is max
      if self.nov < entry:
        break
      # retrieve all values from the branches
      self.getEntry(entry)
      
      for alg in self._algTools:
        if alg.status is StatusTool.DISABLE:
          continue
        if alg.execute().isFailure():
          self._logger.error('The tool %s return status code different of SUCCESS',alg.name)
        if alg.wtd is StatusWatchDog.ENABLE:
          self._logger.debug('Watchdog is true in %s. Skipp events',alg.name)
          # reset the watchdog since this was used
          alg.wtd = StatusWatchDog.DISABLE
          break



  def finalize( self ):
    self._logger.info('Finalizing all tools...')
    if super(EventLooper,self).finalize().isFailure():
      self._logger.fatal('Impossible to finalize the EventLooper services.')

    for alg in self._algTools:
      if alg.isFinalized():
        continue
      if alg.finalize().isFailure():
        self._logger.error('The tool %s return status code different of SUCCESS',alg.name)

  def push_back( self, alg ):
    self._algTools.append( alg )

  def __add__(self, alg):
    self._algTools.append( alg )

  def clear(self):
    self._algTools = list()

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

  def _init_lock(self):
    self._initialized = StatusTool.IS_INITIALIZED

  def _fina_lock(self):
    self._finalized = StatusTool.IS_FINALIZED


  
