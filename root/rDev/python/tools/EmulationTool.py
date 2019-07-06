
__all__ = ['EmulationTool']

from TrigEgammaDevelopments.AlgBaseTool import AlgBaseTool
from TrigEgammaDevelopments.StatusCode  import StatusCode
import numpy as np

class EmulationTool( AlgBaseTool ):

  _electronSelectors = {}
  _triggerSelectors = {}

  def __init__(self, name):
    AlgBaseTool.__init__(self, name)

  # Add selector
  def add_electron_selector( self, pidname, selector ):
    self._electronSelectors[pidname] = selector

  # Add selector
  def add_trigger_selector( self, pidname, selector ):
    self._triggerSelectors[pidname] = selector


  def initialize(self):

    # Initialize all selector for the offline
    for pidname, tool in self._electronSelectors.iteritems():
      if tool.isInitialized():
        continue
      self._logger.info('Initializing the selector %s', pidname)
      if tool.initialize().isFailure():
        self._logger.error('Can not initialize the selector %s',pidname)

    # Initialize all selector for the trigger
    for pidname, tool in self._triggerSelectors.iteritems():
      if tool.isInitialized():
        continue
      self._logger.info('Initializing the selector %s', pidname)
      if tool.initialize().isFailure():
        self._logger.error('Can not initialize the selector %s',pidname)
    
    return StatusCode.SUCCESS

  def execute(self):
    
    el = self.retrieve( "Electron" )
    for pidname, tool in self._electronSelectors.iteritems():
      passed = tool(el)
      el.setDecor(pidname + "_discriminant", tool.discriminant )
      el.setDecor(pidname, passed)

    fc = self.retrieve( "FastCalo" )
    for pidname, tool in self._triggerSelectors.iteritems():
      passed = tool(fc)
      fc.setDecor(pidname + "_discriminant", tool.discriminant )
      fc.setDecor(pidname + "_selector",tool )
      fc.setDecor(pidname, passed)
      

    return StatusCode.SUCCESS


  def finalize(self):
    #for name, tool in self._electronSelectors.iteritems():
    #  tool.finalize()
    return StatusCode.SUCCESS




      





