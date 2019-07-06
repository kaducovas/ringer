
__all__ = ['job']

from RingerCore                           import checkForUnusedVars, retrieve_kw, progressbar, LoggingLevel, Logger
from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.Event         import EventLooper
from TrigEgammaDevelopments.AlgBaseTool   import StatusTool, StatusWatchDog
import ROOT


class Job(Logger):

  def __init__(self):
    Logger.__init__(self)
    self._eventStack = []
    self._toolStack = []


  def push_back(self, obj):
    if type(obj) is EventLooper:
      self._eventStack.append( obj )
    else:
      self._toolStack.append( obj )

  
  def initialize(self):

    if not self._eventStack > 0:
      self._logger.fatal('There is no event added into the stack. Add Event() using push_back')
    if not self._toolStack > 0:
      self._logger.warning('There is any tools added into the stack.')

    # add all tool into the first event object
    for tool in self._toolStack:
      self._eventStack[0].push_back(tool)
    self._eventStack[0].initialize()


  def execute(self):

    for event in self._eventStack:
      for tool in self._toolStack:
        # check if the current tool is allow to run in this event
        if tool.checkId( event.id() ):
          tool.enable()
        else: # if not disable te tool
          tool.disable()
      if not event.isInitialized():
        event.setStoreSvc(self._eventStack[0].getStoreSvc())
        event.setTools(self._eventStack[0].getTools())
        event.initialize()
      
      # execute the event loop
      event.execute()
    # loop over event reader object

  def finalize(self):
    for tool in self._toolStack:
      tool.enable()
    self._eventStack[-1].finalize()


# intance Main object
job = Job()


