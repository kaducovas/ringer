

__all__ = ['EgammaBaseTool','ExpertProperties']

from RingerCore import  Logger
from TrigEgammaDevelopments            import AlgBaseTool, StatusTool, StatusWatchDog
from TrigEgammaDevelopments            import StatusCode
from TrigEgammaDevelopments.dataframe  import EgammaPid, EgammaPidEnum

class ExpertProperties(object):
  def __init__(self):
    self._egammaPid = EgammaPid.Likelihood
    self._doTrigger = False

  @property
  def egammaPid(self):
    return self._egammaPid

  @egammaPid.setter
  def egammaPid(seflf, v):
    self._egammaPid = v



class EgammaBaseTool( AlgBaseTool ):

  def __init__(self, name):
    AlgBaseTool.__init__(self,name)
    self._doTrigger = False
    self._expertProperties = ExpertProperties() 

  def ExperimentalAndExpertMethods(self):
    return self._expertProperties

  @property
  def doTrigger(self):
    return self._doTrigger

  @doTrigger.setter
  def doTrigger(self, v):
    self._doTrigger = v


  # Event selection method
  def ApplyElectronSelection( self, pidname ):
    """
      Apply the electron event selection using fastcalo or electron features.
      The pidname will be a string that can be one or more pidnames algorithms.
      If there is EFCalo or HLT in pidname, the selection uses fastcalo features.
      otherwise electron offline features. You can define the pidname as:
      EFCalo_isMedium&HLT_isMedium, here the selection will apply an AND in the
      final selection. You can uses || (OR) to apply this conditional.
    """
    doAnd=False; doOr=False
    fc = self.retrieve("FastCalo"); el = self.retrieve("Electron")
    # remove spaces if exist
    pidname = pidname.replace(' ','')
    # Check conditions strings
    if '&' in pidname:
      pidname = pidname.split('&')
      doAnd=True; isPassed=True
    elif '||' in pidname:
      pidname = pidname.split('||')
      doOr=True; isPassed=False
    else:
      pidname = [pidname]; isPassed=False

    for pid in pidname:
      # Apply on trigger features
      if ('L2Calo' in pid) or ('L2' in pid) or ('EFCalo' in pid) or ('HLT' in pid):
        passed=fc.ApplyElectronSelection(pid)
      else: # Apply on Offline electron features
        passed=el.ApplyElectronSelection(pid)
      
      if doAnd: # Apply answer concatenation
        isPassed=isPassed and passed
      elif doOr:
        isPassed=isPassed or passed
      else:
        isPassed=passed
      
    # return the final answer
    return isPassed

  # Get the correct pid from the string name
  def getPidName( self, name ):
    _name = name.lower()
    if self.ExperimentalAndExpertMethods().egammaPid is EgammaPid.Likelihood:
      if EgammaPidEnum.VeryLoose in _name:
        return 'LHVLoose'
      if EgammaPidEnum.Loose in _name:
        return 'LHLoose'
      if EgammaPidEnum.Medium in _name:
        return 'LHMedium'
      if EgammaPidEnum.Tight in _name:
        return 'LHTight'
    elif self.ExperimentalAndExpertMethods().egammaPid is EgammaPid.IsEm:
      if EgammaPidEnum.VeryLoose in _name:
        return 'VLoose'
      if EgammaPidEnum.Loose in _name:
        return 'Loose'
      if EgammaPidEnum.Medium in _name:
        return 'Medium'
      if EgammaPidEnum.Tight in _name:
        return 'Tight'
    else:
      self._logger.warning('There is no pidname criteria in this alg name %s',name)









