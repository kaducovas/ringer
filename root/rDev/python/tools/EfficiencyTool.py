
__all__ = ['EfficiencyTool']

from TrigEgammaDevelopments.dataframe   import ElectronCandidate
from TrigEgammaDevelopments.tools       import EgammaBaseTool
from TrigEgammaDevelopments             import AlgBaseTool
from TrigEgammaDevelopments             import StatusCode

from RingerCore import retrieve_kw


class EfficiencyTool( EgammaBaseTool ):
  _monList = []

  def __init__(self, name, **kw):
    EgammaBaseTool.__init__(self, name)
    # Default directory
    self._basepath = 'Event/EfficiencyTool'
    self._applyPid = True
    
  def set_monitoring( self, mon ):
    self._monList = mon

  @property
  def applyPid(self):
    return self._applyPid

  @applyPid.setter
  def applyPid(self, v):
    self._applyPid = v


  def initialize(self):
    
    from TrigEgammaDevelopments.helper import zee_etbins, default_etabins, nvtx_bins
    from ROOT import TH1F, TProfile
    import numpy as np
    
    et_bins = zee_etbins
    eta_bins = default_etabins

    for name in self._monList:
      self.storeSvc().mkdir( self._basepath+'/'+name+'/Efficiency' )
      self.storeSvc().addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', len(et_bins)-1, np.array(et_bins)))
      self.storeSvc().addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(eta_bins)-1, np.array(eta_bins)))
      self.storeSvc().addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", 20, -3.2, 3.2));
      self.storeSvc().addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', 16, 0, 80))
      self.storeSvc().addHistogram(TH1F('nvtx' ,'N_{vtx} distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
      self.storeSvc().addHistogram(TH1F('match_et','E_{T} matched distribution;E_{T};Count', len(et_bins)-1, np.array(et_bins)))
      self.storeSvc().addHistogram(TH1F('match_eta','#eta matched distribution;#eta;Count', len(eta_bins)-1, np.array(eta_bins)))
      self.storeSvc().addHistogram(TH1F("match_phi", "#phi matched distribution; #phi ; Count", 20, -3.2, 3.2));
      self.storeSvc().addHistogram(TH1F('match_mu' ,'<#mu> matched distribution;<#mu>;Count', 16, 0, 80))
      self.storeSvc().addHistogram(TH1F('match_nvtx' ,'N_{vtx} matched distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
      self.storeSvc().addHistogram(TProfile("eff_et", "#epsilon(E_{T}); E_{T} ; Efficiency" , len(et_bins)-1, np.array(et_bins)))
      self.storeSvc().addHistogram(TProfile("eff_eta", "#epsilon(#eta); #eta ; Efficiency"  , len(eta_bins)-1,np.array(eta_bins)))
      self.storeSvc().addHistogram(TProfile("eff_phi", "#epsilon(#phi); #phi ; Efficiency", 20, -3.2, 3.2));
      self.storeSvc().addHistogram(TProfile("eff_mu", "#epsilon(<#mu>); <#mu> ; Efficiency", 16, 0, 80));	
      self.storeSvc().addHistogram(TProfile("eff_nvtx", "#epsilon(N_{vtx}); N_{vtx} ; Efficiency", len(nvtx_bins)-1, np.array(nvtx_bins)));	

    self.init_lock()
    return StatusCode.SUCCESS 


  def execute(self):
    
    from TrigEgammaDevelopments.helper import GeV
    # Retrieve Electron container
    el = self.retrieve( "Electron" )
    fc = self.retrieve( "FastCalo" )
    eventInfo = self.retrieve( "EventInfo" )
    et = el.et/GeV
    nvtx = eventInfo.nvtx
    avgmu = eventInfo.avgmu

    if el.execute().isFailure():
      self._logger.warning("Impossible to execute all Electron services.")

    for name in self._monList:

      pid = self.getPidName(name); isGood=True
      if self._applyPid:  isGood = el.getDecor('is'+pid)

      if isGood:
        dirname = self._basepath+'/'+name+'/Efficiency'
        self.storeSvc().histogram(dirname+'/et').Fill(et)
        self.storeSvc().histogram(dirname+'/eta').Fill(el.eta)
        self.storeSvc().histogram(dirname+'/phi').Fill(el.phi)
        self.storeSvc().histogram(dirname+'/nvtx').Fill(nvtx)
        self.storeSvc().histogram(dirname+'/mu').Fill(avgmu)
        passed = self.ApplyElectronSelection( name )

        if passed:
          self.storeSvc().histogram(dirname+'/match_et').Fill(et)
          self.storeSvc().histogram(dirname+'/match_eta').Fill(el.eta)
          self.storeSvc().histogram(dirname+'/match_phi').Fill(el.phi)
          self.storeSvc().histogram(dirname+'/match_nvtx').Fill(nvtx)
          self.storeSvc().histogram(dirname+'/match_mu').Fill(avgmu)
        
        self.storeSvc().histogram(dirname+'/eff_et').Fill(et,passed)
        self.storeSvc().histogram(dirname+'/eff_eta').Fill(el.eta,passed)
        self.storeSvc().histogram(dirname+'/eff_phi').Fill(el.phi,passed)
        self.storeSvc().histogram(dirname+'/eff_nvtx').Fill(nvtx,passed)
        self.storeSvc().histogram(dirname+'/eff_mu').Fill(avgmu,passed)

    return StatusCode.SUCCESS 

  def finalize(self):
   
    self._logger.info('{:-^108}'.format((' %s ')%(self._basepath)))
    for name in self._monList:
      dirname = self._basepath+'/'+name+'/Efficiency'
      total  = self.storeSvc().histogram( dirname+'/et' ).GetEntries()
      passed = self.storeSvc().histogram( dirname+'/match_et' ).GetEntries()
      eff = passed/float(total) * 100. if total>0 else 0
      eff=('%1.2f')%(eff); passed=('%d')%(passed); total=('%d')%(total)
      stroutput = '| {0:<80} | {1:<5} ({2:<5}, {3:<5}) |'.format(name,eff,passed,total)
      self._logger.info(stroutput)

    self._logger.info('{:-^108}'.format((' %s ')%('-')))
    self.fina_lock()
    return StatusCode.SUCCESS 


