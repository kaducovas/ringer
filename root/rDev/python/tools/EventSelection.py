
__all__ = ['EventSelection']

from RingerCore                         import NotSet
from TrigEgammaDevelopments             import AlgBaseTool, StatusWatchDog
from TrigEgammaDevelopments             import StatusCode
from TrigEgammaDevelopments.tools       import EgammaBaseTool
from TrigEgammaDevelopments.helper      import GeV
import numpy as np

class EventSelection( EgammaBaseTool ):

  _selectionZ = False
  _selectionFakes = False
  _pidname = NotSet
  _l2EtCut = NotSet
  _offEtCut = NotSet

  def __init__(self, name):
    EgammaBaseTool.__init__(self, name)

  def initialize(self):
    return StatusCode.SUCCESS

  def set_pidname(self, pidname):
    self._pidname = pidname

  @property
  def selectionFakes(self):
    return self._selectionFakes

  @property
  def selectionZ(self):
    return self._selectionZ
  
  @property
  def l2EtCut(self):
    return self._l2EtCut

  @property
  def offEtCut(self):
    return self._offEtCut

  @selectionFakes.setter
  def selectionFakes(self, v):
    self._selectionFakes = v

  @selectionZ.setter
  def selectionZ(self, v):
    self._selectionFakes = v

  @l2EtCut.setter
  def l2EtCut(self, v):
    self._l2EtCut = v

  @offEtCut.setter
  def offEtCut(self, v):
    self._offEtCut = v

  def execute(self):
    
    el = self.retrieve( "Electron"  )
    fc = self.retrieve( "FastCalo"  )
    mc = self.retrieve( "MonteCarlo")
    eventInfo = self.retrieve( "EventInfo" )

    if self._doTrigger:
      if not fc.isGoodRinger():
        self.wtd = StatusWatchDog.ENABLE
        self._logger.debug('fc.isGoodRinger')
        return StatusCode.SUCCESS
    else:
      if not el.isGoodRinger():
        self.wtd = StatusWatchDog.ENABLE
        self._logger.debug('el.isGoodRinger')
        return StatusCode.SUCCESS

    # Apply FastCalo Et cut
    if self._l2EtCut:
      if fc.et/GeV < self._l2EtCut:
        self.wtd = StatusWatchDog.ENABLE
        self._logger.debug('l2EtCut')
        return StatusCode.SUCCESS

    # Apply Offline Electron Et cut
    if self._offEtCut:
      if el.et/GeV < self._offEtCut:
        self.wtd = StatusWatchDog.ENABLE
        self._logger.debug('offEtCut')
        return StatusCode.SUCCESS

    if mc.isMC():
      isZ = mc.isEfromZ()
      if self.selectionFakes and isZ:
        self.wtd = StatusWatchDog.ENABLE
        self._logger.debug('Fakes: is Z! reject')
        return StatusCode.SUCCESS
    
      if self.selectionZ and not isZ:
        self.wtd = StatusWatchDog.ENABLE
        self._logger.debug('Z: is not Z! reject')
        return StatusCode.SUCCESS

    if self._pidname:
      self._logger.debug('Apply pid cut')
      # is this a veto criteria?
      isVeto = True if '!' in self._pidname else False
      if isVeto: # Fix the pidname
        pidname = self._pidname.replace('!','')
      else:
        pidname = self._pidname

      passed = el.ApplyElectronSelection(pidname)
      # Apply veto event selection
      if isVeto and passed:
        self.wtd = StatusWatchDog.ENABLE
        return StatusCode.SUCCESS
      if not isVeto and not passed:        
        self.wtd = StatusWatchDog.ENABLE
        return StatusCode.SUCCESS

    self.wtd = StatusWatchDog.DISABLE
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS




      





