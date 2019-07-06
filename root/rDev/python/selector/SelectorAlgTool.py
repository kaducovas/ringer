
__all__ = ['CaloRingerSelectorTool', 'egammaRingerPid']

from RingerCore import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars, \
                       expandFolders, csvStr2List, NotSet

from TrigEgammaDevelopments.dataframe import Electron, FastCalo
from TrigEgammaDevelopments.helper    import GeV
from TrigEgammaDevelopments.selector  import NeuralNetwork
from TrigEgammaDevelopments           import AlgBaseTool

import numpy as np

def get_pid_from_conf_name( pidname ):
  if 'Tight' in pidname:
    return 'tight'
  elif 'Medium' in pidname:
    return 'medium'
  elif 'VeryLoose' in pidname:
    return 'vloose'
  else:
    return 'loose'


class EgammaRingerPid(object):
  """
    Ringer Trigger Egamma pid names to acces all tuning containers
  """
  ElectronVeryLoose = 'ElectronHighEnergyVeryLooseConf' 
  ElectronLoose     = 'ElectronHighEnergyLooseConf' 
  ElectronMedium    = 'ElectronHighEnergyMediumConf' 
  ElectronTight     = 'ElectronHighEnergyTightConf'

# declare helpe objects
egammaRingerPid = EgammaRingerPid()


from TrigEgammaDevelopments.StatusCode import StatusCode

class CaloRingerSelectorTool(AlgBaseTool):

  _version = 1
  _RNN_not_set = -999 # default value 

  def __init__(self, name):
    AlgBaseTool.__init__(self, name)
    self._pidname = egammaRingerPid.ElectronVeryLoose
    self._discriminant = self._RNN_not_set
    self._useRNNStored=False

  @property
  def calibPath(self):
    return self._calibPath

  @calibPath.setter
  def calibPath(self, v ):
    self._calibPath=v
  
  @property
  def pidname(self):
    return self._pidname

  @pidname.setter
  def pidname(self, v):
    self._pidname = v

  #TODO: Use this for future, still in validation...
  @property
  def useRNNStored(self):
    return self._useRNNStored

  #TODO: Use this for future, still in validation...
  @pidname.setter
  def useRNNStored(self, v):
    self._useRNNStored = v

 
  def initialize(self):

    path = self.calibPath+'/TrigL2CaloRingerConstants.py'
    tuningDict = self.__retrieve_py_module(path,'SignaturesMap').SignaturesMap()
    tuning     = NotSet
    if tuningDict['version'] is self._version:
      metadataFromTuning = tuningDict['metadata']
      self._useLumiVar = metadataFromTuning['UseLumiVar']
      self._useEtaVar  = metadataFromTuning['UseEtaVar']
      self._lumiCut    = metadataFromTuning['LumiCut']
      try:
        tuning = tuningDict['tuning'][self._pidname]
      except KeyError:
        self._logger.info('Can not retrieve the key %s', self._pidname)
    else:
      self._logger.error('Version not supported!')
      return StatusCode.FAILURE

    self._discrs = list()
    self._thresholds = dict()
    self._useNoActivationFunctionInTheLastLayer = False
    self._doPileupCorrection = False
    keyswanted = tuning.keys()
    
    for key in sorted(keyswanted):
      self._discrs.append( NeuralNetwork(tuning[key]) )

    path = self.calibPath+'/TrigL2CaloRingerThresholds.py'
    thresholdDict = self.__retrieve_py_module(path, 'ThresholdsMap').ThresholdsMap()
    threshold = None
    # Reading the thresholds
    if thresholdDict['version'] is self._version:
      metadataFromThreshold = thresholdDict['metadata']
      self._useNoActivationFunctionInTheLastLayer = metadataFromThreshold['UseNoActivationFunctionInTheLastLayer']
      self._doPileupCorrection = metadataFromThreshold['DoPileupCorrection']
      try:
        threshold = thresholdDict['tuning'][self._pidname]
      except KeyError:
        self._logger.info('Can not retrieve the key %s', self._pidname)
    else:
      self._logger.error('Version not supported!')
      return StatusCode.FAILURE

    from TrigEgammaDevelopments.selector.SelectorCore import Threshold
    for key in sorted(threshold.keys()):
      thr = Threshold(threshold[key])
      self._thresholds[key] = thr

    last_key = sorted(threshold.keys())[-1]
    self._etmax = self._thresholds[last_key].etmax
    self._etamax = self._thresholds[last_key].etamax


    if len(threshold.keys()) > len(tuning.keys()): 
      self._logger.info('the thresholds is higher than the networks')
    elif len(threshold.keys()) < len(tuning.keys()):
      self._logger.warning('The thresholds grid is lower than the number of neural networks')
    else:
      self._logger.info('The thresholds are equal than networks')
    
    self.init_lock()
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS
 
  def execute(self):
    return StatusCode.SUCCESS
   
  # Expert method to create a set of empty thrsholds
  def reset( self, etbins, etabins ):

    from TrigEgammaDevelopments.selector.SelectorCore import Threshold
    # clear threshold dict
    self._thresholds = dict()

    for etBinIdx in range(len(etbins)-1):
      for etaBinIdx in range(len(etabins)-1):
        thrObj = Threshold()
        thrObj.etmin = etbins[etBinIdx]
        thrObj.etmax = etbins[etBinIdx+1]
        thrObj.etamin = etabins[etaBinIdx]
        thrObj.etamax = etabins[etaBinIdx+1]
        self._logger.debug('Creating Threshold with et = [%1.3f, %1.3f] and eta = [%1.3f, %1.3f]',\
            thrObj.etmin,thrObj.etmax,thrObj.etamin,thrObj.etamax)
        self._thresholds[('et%d_eta%d')%(etBinIdx,etaBinIdx)] = thrObj

    last_key = self._thresholds.keys()[-1]
    self._etmax = self._thresholds[last_key].etmax
    self._etamax = self._thresholds[last_key].etamax

  def configureThresholdParam(self, key, a, b, b0):  
    try:
      # y(x) = b + ax
      self._thresholds[key].alpha = a
      self._thresholds[key].beta = b
      self._thresholds[key].thr = b0
    except KeyError:
      self._logger.fatal('Error to retrieve the Threshold. Maybe the key %s doesnt exist', key)


  def getThresholdParam(self, key):
    try:
      thrObj = self._thresholds[key]
      return thrObj.alpha, thrObj.beta, thrObj.thr
    except KeyError:
      self._logger.fatal('Error to retrieve the Threshold. Maybe the key %s doesnt exist', key)
      
     
  def __call__(self, el):

    #if not type(el) in [Electron, FastCalo]:
    #  self._logger.warning('Object type not supported.')
    #  return False
    et = el.et/GeV
    eta = abs(el.eta)
    avgmu = el.getAvgMu()
    # Fix eta and et ranges
    if eta > self._etamax:  eta = self._etamax
    if et > self._etmax:  et = self._etmax
    # Select the correct neural network range
    
    if self._useRNNStored:
      self._discriminant = el.getRnnOutput( get_pid_from_conf_name(self._pidname) )
    else:
      self._discriminant=self._RNN_not_set
    
    if self._discriminant == self._RNN_not_set:
      for obj in self._discrs:
        if obj.checkForCompatibleBinning(et,eta):
          self._discriminant = obj( self._normalize(el.ringer_rings) )
          if self._useNoActivationFunctionInTheLastLayer:
            self._discriminant = obj.getOutputBeforeTheActivationFunction()
      # Loop over all neural networks objects

    threshold = 0.0
    for _, obj in self._thresholds.iteritems():
      if obj.checkForCompatibleBinning(et,eta):
        if self._doPileupCorrection:
          threshold = obj.threshold(avgmu)
        else:
          threshold = obj.threshold()
    if self._discriminant <= threshold:
      return False
    
    return True

  def _normalize(self, rings):
    return (np.array([rings])/sum(rings))
  
  @property
  def useNoActivationFunctionInTheLastLayer(self):
    return self._useNoActivationFunctionInTheLastLayer

  @useNoActivationFunctionInTheLastLayer.setter
  def useNoActivationFunctionInTheLastLayer(self, value):
    self._useNoActivationFunctionInTheLastLayer=value

  @property
  def thresholds(self):
    return self._thresholds

  @property
  def doPileupCorrection(self):
    return self._doPileupCorrection
  
  @doPileupCorrection.setter
  def doPileupCorrection(self, value):
    self._doPileupCorrection=value

  @property
  def discriminant(self):
    return self._discriminant

  def __retrieve_py_module(self, pypath, classname):
    try:
      import imp
      obj__Module__ = imp.load_source(classname, pypath)
    except ImportError:
      self._logger.fatal('Can not import the discriminator %s',pypath)
    try: # Remove junk file created by the python reader
      import os
      #os.remove( pypath+'c')
    except:
      self._logger.warning('%sc not found',pypath)
    try:
      self._logger.info('PathResolver: %s',pypath)
      return obj__Module__
    except KeyError:
      self._logger.fatal('Key %s not found in this module. Abort')

