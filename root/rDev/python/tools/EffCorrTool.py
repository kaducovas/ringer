__all__ = ["EffCorrTool"]

from RingerCore import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars, \
                       expandFolders, csvStr2List, progressbar

from TrigEgammaDevelopments.helper.constants     import *
from TrigEgammaDevelopments.helper.util          import *
from TrigEgammaDevelopments.plots.AtlasStyle     import *
from TrigEgammaDevelopments.tools                import EgammaBaseTool
from TrigEgammaDevelopments                      import StatusCode
import numpy as np

class EffCorrTool( EgammaBaseTool ):

  def __init__(self, name):
    
    EgammaBaseTool.__init__(self, name)
    # create all variables
    self._basepath = 'Event/EffCorrTool'
    self._thresholdEtBins   = ringer_tuning_etbins
    self._thresholdEtaBins  = ringer_tuning_etabins
    self._algDictNames = {}
    self._percentage = {}
    self._metadata = {}
    self._probesId = []
    self._fakesId = []
    self._limits = []

  def setProbesId(self, id):
    self._probesId.append(id)
    self.setId(id)

  def setFakesId(self, id):
    self._fakesId.append(id)
    self.setId(id)

  # Must be: setTagets( "tight", "el_lhTight", "EFCalo_*", 0.2 )
  def setTargets( self, pidname ,alg, tgt, percentage = 0.0 ):
    self._algDictNames[pidname] = (alg,tgt)
    if percentage>1: # fix the range if higher than 1
      percentage=percentage/100.
    self._percentage[pidname] =percentage

  def setEtBinningValues( self, etbins ):
    self._thresholdEtBins = etbins
  
  def setEtaBinningValues( self, etabins ):
    self._thresholdEtaBins = etabins

  def setLimits( self, limits ):
    self._limits = limits

  def setMetadata(self, metadata):
    self._metadata = metadata

  def setAlias( self, v):
    self._alias=v


  def initialize(self):
   
    from ROOT import TH2F, TH1F, TProfile
    keyWanted = ['probes','fakes']

    for dirname in keyWanted:
      for pidname, pair in self._algDictNames.iteritems():
        for etBinIdx in range( len(self._thresholdEtBins)-1 ):
          for etaBinIdx in range( len(self._thresholdEtaBins)-1 ):
            
            binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
            algname = pair[0]
            tgtname = pair[1]
            mumax   = 100
            mumin   = 0
            nmubins = (mumax-mumin)-1
            etbins  = zee_etbins
            etabins = default_etabins
          
 
            # create neural network histograms
            self.storeSvc().mkdir( self._basepath+'/'+dirname+'/'+pidname+'/'+algname+'/'+binningname )
            self.storeSvc().addHistogram(TH2F('discriminantVsEt'  , 'Et Vs discriminant' , 1000, -12, 7, len(etbins)-1 , np.array(etbins) ) )
            self.storeSvc().addHistogram(TH2F('discriminantVsEta' , 'Eta Vs discriminant', 1000, -12, 7, len(etabins)-1, np.array(etabins) ) )
            self.storeSvc().addHistogram(TH2F('discriminantVsNvtx', 'Offline Pileup as function of the discriminant;discriminant;nvtx;Count', \
                                         1000, -12,7,len(nvtx_bins)-1,np.array(nvtx_bins)) ) 
            self.storeSvc().addHistogram(TH2F('discriminantVsMu'  , 'Online Pileup as function of the discriminant;discriminant;nvtx;Count' , \
                                         1000, -12,7,nmubins,mumin,mumax) ) 
          
            # create efficienci target histograms
            self.storeSvc().mkdir( self._basepath+'/'+dirname+'/'+pidname+'/'+tgtname+'/'+binningname )
            self.storeSvc().addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', len(etbins)-1, np.array(etbins)))
            self.storeSvc().addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(etabins)-1, np.array(etabins)))
            self.storeSvc().addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", 20, -3.2, 3.2));
            self.storeSvc().addHistogram(TH1F('nvtx' ,'N_{vtx} distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
            self.storeSvc().addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', 16, 0, 80))
            self.storeSvc().addHistogram(TH1F('match_et','E_{T} matched distribution;E_{T};Count', len(etbins)-1, np.array(etbins)))
            self.storeSvc().addHistogram(TH1F('match_eta','#eta matched distribution;#eta;Count', len(etabins)-1, np.array(etabins)))
            self.storeSvc().addHistogram(TH1F("match_phi", "#phi matched distribution; #phi ; Count", 20, -3.2, 3.2));
            self.storeSvc().addHistogram(TH1F('match_nvtx' ,'N_{vtx} matched distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
            self.storeSvc().addHistogram(TH1F('match_mu' ,'<#mu> matched distribution;<#mu>;Count', 16, 0, 80))
            self.storeSvc().addHistogram(TProfile("eff_et", "#epsilon(E_{T}); E_{T} ; Efficiency" , len(etbins)-1, np.array(etbins)))
            self.storeSvc().addHistogram(TProfile("eff_eta", "#epsilon(#eta); #eta ; Efficiency"  , len(etabins)-1,np.array(etabins)))
            self.storeSvc().addHistogram(TProfile("eff_phi", "#epsilon(#phi); #phi ; Efficiency", 20, -3.2, 3.2));
            self.storeSvc().addHistogram(TProfile("eff_nvtx", "#epsilon(N_{vtx}); N_{vtx} ; Efficiency", len(nvtx_bins)-1, np.array(nvtx_bins)));	
            self.storeSvc().addHistogram(TProfile("eff_mu", "#epsilon(<#mu>); <#mu> ; Efficiency", 16, 0, 80));	


    self.init_lock()
    return StatusCode.SUCCESS 

  def execute(self):

    el = self.retrieve( "Electron" )
    el.execute()
    if el.execute().isFailure():
      self._logger.warning("Impossible to execute all Electron services.")

    from TrigEgammaDevelopments.helper import GeV
    # retrive the correct et/eta information
    if self._doTrigger: # Online
      obj = self.retrieve( "FastCalo" ); et = obj.et/GeV; eta = obj.eta; phi = obj.phi
    else: # Offline
      obj = el; et = el.et/GeV; eta = el.eta; phi = el.phi

    # TODO: This should be a property for future?
    # Remove events after 2.47 in eta. This region its not good for calo cells. (Fat cells)
    if abs(eta)>2.47:
      return StatusCode.SUCCESS 

    # retrieve the pileup event information
    eventInfo = self.retrieve( "EventInfo" )
    nvtx = eventInfo.nvtx
    avgmu = eventInfo.avgmu

    # check if the current event looper contains the list
    # if id to fill all histograms.
    if eventInfo.id() in self._probesId:
      dirname = 'probes'
    elif eventInfo.id() in self._fakesId:
      dirname = 'fakes'
    else: # skipp run
      return StatusCode.SUCCESS 
    
    # Get the correct binning to fill the histogram later...
    etBinIdx, etaBinIdx = self.__retrieveBinningIdx( et, abs(eta) )
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
    
    for pidname, pair in self._algDictNames.iteritems():
       
      algname = pair[0]
      tgtname = pair[1]

      # Each criteria must be passed by your offline 
      #if eventInfo.id() in self._probesId and self._doTrigger:
      #  pid = self.getPidName( tgtname )
      #  isGood = el.getDecor('is'+pid)
      #else:
      #  isGood = True

      # get the target answer
      passed = self.ApplyElectronSelection( tgtname )
      # get the ringer RNN discriminant
      discriminant = obj.getDecor(algname+'_discriminant')
      path = self._basepath+'/'+dirname+'/'+pidname+'/'+tgtname+'/'+binningname
      
      isGood=True
      # Fill all target histograms
      if isGood:
        self.storeSvc().histogram(path+'/et').Fill(et)
        self.storeSvc().histogram(path+'/eta').Fill(eta)
        self.storeSvc().histogram(path+'/phi').Fill(phi)
        self.storeSvc().histogram(path+'/nvtx').Fill(nvtx)
        self.storeSvc().histogram(path+'/mu').Fill(avgmu)
        if passed: # If approved by the selector
          self.storeSvc().histogram(path+'/match_et').Fill(et)
          self.storeSvc().histogram(path+'/match_eta').Fill(eta)
          self.storeSvc().histogram(path+'/match_phi').Fill(phi)
          self.storeSvc().histogram(path+'/match_nvtx').Fill(nvtx)
          self.storeSvc().histogram(path+'/match_mu').Fill(avgmu)
        self.storeSvc().histogram(path+'/eff_et').Fill(et,passed)
        self.storeSvc().histogram(path+'/eff_eta').Fill(eta,passed)
        self.storeSvc().histogram(path+'/eff_phi').Fill(phi,passed)
        self.storeSvc().histogram(path+'/eff_nvtx').Fill(nvtx,passed)
        self.storeSvc().histogram(path+'/eff_mu').Fill(avgmu,passed)
      
      # Fill RNN distributions
      path = self._basepath+'/'+dirname+'/'+pidname+'/'+algname+'/'+binningname
      
      # Each criteria must be passed by your offline 
      #if eventInfo.id() in self._probesId and self._doTrigger:
      #  """
      #     Use this to clean up all T&P event to fill the neuron 
      #  """
      #  isGood = el.getDecor('isLHVLoose')
      #else:
      #  isGood = True

      isGood=True
      if isGood:
        self.storeSvc().histogram(path+'/discriminantVsEt').Fill(discriminant, et)
        self.storeSvc().histogram(path+'/discriminantVsEta').Fill(discriminant, eta)
        self.storeSvc().histogram(path+'/discriminantVsMu').Fill(discriminant, avgmu)
        self.storeSvc().histogram(path+'/discriminantVsNvtx').Fill(discriminant, nvtx)

    # loop over selectors pairs

    return StatusCode.SUCCESS 

  def finalize(self):
    #self.plot()
    self.fina_lock()
    return StatusCode.SUCCESS 


  def plot(self, **kw):

    dirname      = retrieve_kw(kw, 'dirname'     , 'correction'   )
    pdftitle     = retrieve_kw(kw, 'pdftitle'    , 'Distributions')
    pdfoutput    = retrieve_kw(kw, 'pdfoutput'   , 'distributions')
    atlaslabel   = retrieve_kw(kw, 'atlaslabel'  , 'Internal'     )
    selectorDict = retrieve_kw(kw, 'selectorDict', None           )
    dovertical   = retrieve_kw(kw, 'dovertical'  , False          )

    import os
    # Organize outputs (.py and .pdf)
    from datetime import datetime
    localpath = os.getcwd()+'/'+dirname
    
    try:
      if not os.path.exists(localpath):
        os.makedirs(localpath)
    except:
      self._logger.warning('The director %s exist.', localpath)

    # create skeleton
    thrDict = {'version':1, 'type': ['Hypo']  , 'date':0, 'metadata':dict(), 'tuning':dict(), 'name':[self._alias]}
    thrDict['metadata'] = self._metadata

    self._logger.info('Applying correction...')
    for pidname, pair in self._algDictNames.iteritems():
      # get the real reference values
      refValues = self.__retrieveTargetValues(pidname)
      algname = pair[0]
      tgtname = pair[1]
      # retrive the correct et/eta information

      if selectorDict: # retrieve from the expert input
        try:
          selector = selectorDict[algname]
        except KeyError:
          self._logger.fatal('Can not retrieve the algname %s',algname)
      else: # Retrieve from the framework
        if self._doTrigger: # Online
          obj = self.retrieve( "FastCalo" ); selector=obj.getDecor(algname+'_selector')
        else: # Offline
          obj = self.retrieve( "Electron" ); selector=obj.getDecor(algname+'_selector')
      
      # create new grid of thresholds objects
      selector.reset( self._thresholdEtBins, self._thresholdEtaBins )
      useNoActivationFunctionInTheLastLayer=selector.useNoActivationFunctionInTheLastLayer
      
      for etBinIdx in range( len(self._thresholdEtBins)-1 ):
        for etaBinIdx in range( len(self._thresholdEtaBins)-1 ):
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          ref = refValues[etBinIdx][etaBinIdx]
          # relax detection if needed
          ref = ref + ((1-ref)*self._percentage[pidname])
          # Retrive histograms
          if self._doTrigger:
          	path = self._basepath+'/probes/'+pidname+'/'+algname+'/'+binningname
          	sgnHist2D = self.storeSvc().histogram(path+'/discriminantVsMu')
          	path = self._basepath+'/fakes/'+pidname+'/'+algname+'/'+binningname
          	bkgHist2D = self.storeSvc().histogram(path+'/discriminantVsMu')
          else:					
          	path = self._basepath+'/probes/'+pidname+'/'+algname+'/'+binningname
          	sgnHist2D = self.storeSvc().histogram(path+'/discriminantVsNvtx')
          	path = self._basepath+'/fakes/'+pidname+'/'+algname+'/'+binningname
          	bkgHist2D = self.storeSvc().histogram(path+'/discriminantVsNvtx')
   
          plotname = localpath+'/eff_corr_'+algname+'_'+binningname
          b, a , b0 = self.__applyThresholdCorrection(ref,sgnHist2D.Clone(),bkgHist2D.Clone(),binningname, plotname, 
                                                      draw=True , 
                                                      xname = '<#mu>' if self._doTrigger else 'N_{vtx}',
                                                      useNoActivationFunctionInTheLastLayer=useNoActivationFunctionInTheLastLayer,
                                                      limits = self._limits, dolumi=False, 
                                                      # FIXME: need to add spaces here. Fix in AtlasStyle for future
                                                      atlaslabel = '      '+atlaslabel,
                                                      dovertical = dovertical
                                                      )
          selector.configureThresholdParam(binningname, a, b, b0) 
      # Hold the thresholds objects
      thrDict['tuning'][selector.pidname] = {}
      thresholds = selector.thresholds
      for key in sorted(thresholds.keys()):
        thrDict['tuning'][selector.pidname][key] = thresholds[key].toRaw()

    # Create the athena/python conf file
    name=localpath+'/TrigL2CaloRingerThresholds.py'
    pyfile = open(name,'w')
    pyfile.write('def ThresholdsMap():\n')
    pyfile.write('  s=dict()\n')
    for key in thrDict.keys():
      pyfile.write('  s["%s"]=%s\n' % (key, thrDict[key]))
    pyfile.write('  return s\n')


    from RingerCore.tex.BeamerAPI import BeamerTexReportTemplate1,BeamerSection,BeamerMultiFigureSlide,BeamerFigureSlide
   
    if not dovertical:
      self._logger.info('Do pdf maker...')
      # Slide maker
      with BeamerTexReportTemplate1( theme = 'Berlin'
                                   , _toPDF = True
                                   , title = pdftitle
                                   , outputFile = pdfoutput
                                   , font = 'structurebold' ):

   
        for pidname, pair in self._algDictNames.iteritems():
          factor = self._percentage[pidname]
          with BeamerSection( name = pidname ):
            # get the real reference values
            refValues = self.__retrieveTargetValues(pidname)
            algname = pair[0]
            tgtname = pair[1]
            for etBinIdx in range( len(self._thresholdEtBins)-1 ):
              for etaBinIdx in range( len(self._thresholdEtaBins)-1 ):
                binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
                plotname = localpath+'/eff_corr_'+algname+'_'+binningname+'.pdf'
                BeamerMultiFigureSlide( title = ("%s, factor = %1.2f, (%s)")%(algname.replace('_','\_'), 
                                                factor ,binningname.replace('_','\_') )
                              , paths = [plotname]
                              , nDivWidth = 1 # x
                              , nDivHeight = 1 # y
                              , texts=None
                              , fortran = False
                              , usedHeight = 0.8
                              , usedWidth = 1.1
                              )
 



    return StatusCode.SUCCESS 



  def __retrieveTargetValues(self, pidname):
    # create values (Et X Eta)
    values = [[0.0 for _ in range(len(self._thresholdEtaBins)-1)] for _ in range(len(self._thresholdEtBins)-1)]
    pair = self._algDictNames[pidname]
    for etBinIdx in range( len(self._thresholdEtBins)-1 ):
      for etaBinIdx in range( len(self._thresholdEtaBins)-1 ):
        tgtname = pair[1];  binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
        path    = self._basepath+'/probes/'+pidname+'/'+tgtname+'/'+binningname
        total   = self.storeSvc().histogram(path+'/eta').GetEntries()
        passed  = self.storeSvc().histogram(path+'/match_eta').GetEntries()
        values[etBinIdx][etaBinIdx] = passed/float(total) if total>0 else 0
    return values

  # (Private method) retrieve the correct binning range
  def __retrieveBinningIdx(self,et, eta):
    # Fix eta value if > 2.5
    if eta > self._thresholdEtaBins[-1]:
      eta = self._thresholdEtaBins[-1]
    if et > self._thresholdEtBins[-1]:
      et = self._thresholdEtBins[-1]

    for etBinIdx in range(len(self._thresholdEtBins)-1):
      for etaBinIdx in range(len(self._thresholdEtaBins)-1):
        if et >= self._thresholdEtBins[etBinIdx] and  et < self._thresholdEtBins[etBinIdx+1]:
          if eta >= self._thresholdEtaBins[etaBinIdx] and eta <= self._thresholdEtaBins[etaBinIdx+1]:
            return etBinIdx, etaBinIdx
    self._logger.fatal('Can not retrieve the correct et (%1.3f)/eta (%1.3f) idx.',et,eta)




  def __applyThresholdCorrection( self, refValue, sgn_hist2D, bkg_hist2D, partition_name, output_name, **kwargs):

    legend_position = retrieve_kw( kwargs, 'legend_position', (0.36,0.20,0.66,0.40))
    useNoActivationFunctionInTheLastLayer=retrieve_kw(kwargs,'useNoActivationFunctionInTheLastLayer',False)
    xname           = retrieve_kw( kwargs, 'xname', 'n_{vtx}' )
    draw            = retrieve_kw( kwargs, 'draw', False)
    limits          = retrieve_kw( kwargs, 'limits', [0,10,20])
    dovertical      = retrieve_kw( kwargs, 'dovertical'  , False)
    
    mumin = limits[0]; mumax=limits[-1]
    mubins = mumax-mumin
    from TrigEgammaDevelopments.helper.util import *
    sgn_hist2D = copy2DRegion(sgn_hist2D,1000,-12,7,mubins,mumin,mumax)
    bkg_hist2D = copy2DRegion(bkg_hist2D,1000,-12,7,mubins,mumin,mumax)



    from copy import deepcopy
    refValue_requested = refValue 
    false_alarm = 1.0
    false_alarm_limit = 0.20
    while false_alarm > false_alarm_limit:
      # Calculate the original threshold
      b0, error = find_threshold(sgn_hist2D.ProjectionX(), refValue )
      # Take eff points using uncorrection threshold
      discr_points, nvtx_points, error_points = calculate_dependent_discr_points(sgn_hist2D , refValue )
      # Calculate eff without correction
      sgn_histNum, sgn_histDen, sgn_histEff, det0   = calculate_efficiency(sgn_hist2D, refValue, b0, 0,  doCorrection=False)
      # Generate correction parameters and produce fixed plots
      sgn_histNum_corr, sgn_histDen_corr, sgn_histEff_corr, detection ,b, a = calculate_efficiency( sgn_hist2D, 
                                                          refValue, b0, 0, limits = limits, doCorretion=True)
      
      # Calculate eff without correction
      bkg_histNum, bkg_histDen, bkg_histEff, _  = calculate_efficiency(bkg_hist2D, refValue, b0, 0,  doCorrection=False)
      # Calculate eff using the correction from signal
      bkg_histNum_corr, bkg_histDen_corr, bkg_histEff_corr, false_alarm = calculate_efficiency(bkg_hist2D, refValue, b, a,  doCorrection=False)

      if false_alarm > false_alarm_limit:
        refValue-=0.025

    # To np.array
    discr_points = np.array(discr_points)

    # Plot correction 
    if draw:
      # Retrieve some usefull information
      y_max = sgn_hist2D.GetYaxis().GetXmax()
      y_min = sgn_hist2D.GetYaxis().GetXmin()
      x_min = y_min; x_max = y_max

      from ROOT import TCanvas, gStyle, TLegend, kRed, kBlue, kBlack,TLine
      from ROOT import TGraphErrors,TF1
      gStyle.SetPalette(107)
      if dovertical:
        canvas = TCanvas('canvas','canvas',1600,2000)
        canvas.Divide(2,3)
      else:
        canvas = TCanvas('canvas','canvas',2800,1600)
        canvas.Divide(3,2)

      pad1= canvas.cd(1)
      sgn_histEff.SetTitle('Signal Efficiency in: '+partition_name)
      sgn_histEff.SetLineColor(kRed)
      sgn_histEff.SetMarkerColor(kRed)
      sgn_histEff.GetYaxis().SetTitle('#epsilon('+xname+')')
      sgn_histEff.GetXaxis().SetTitle(xname)
      sgn_histEff.GetYaxis().SetRangeUser( 0.6, 1.1 ) 
      sgn_histEff.Draw()
      sgn_histEff_corr.SetLineColor(kBlack)
      sgn_histEff_corr.SetMarkerColor(kBlack)
      sgn_histEff_corr.Draw('sames')


      l0 = TLine(x_min,refValue_requested,x_max,refValue_requested)
      l0.SetLineColor(kBlack)
      l0.Draw()
 
      l1 = TLine(x_min,refValue,x_max,refValue)
      l1.SetLineColor(kBlack)
      l1.SetLineStyle(9)
      l1.Draw()
      
      leg1 = TLegend(legend_position[0],legend_position[1], legend_position[2],legend_position[3])
      setLegend1(leg1)
      leg1.SetHeader('Signal efficiency in '+partition_name)
      leg1.AddEntry(sgn_histEff,('Old: d = %1.3f')%(b0),'p' )
      lg1 = leg1.AddEntry(sgn_histEff_corr,('New: d = %1.3f + %s %1.3f')%(b,xname,a),'p' )
      lg1.SetTextColor(kRed)
      leg1.AddEntry(l1,('Reference: %1.3f')%(refValue) ,'l')

      leg1.SetTextSize(0.03)
      leg1.SetBorderSize(0)
      leg1.Draw()
      atlas_template(pad1,**kwargs)

      pad2 = canvas.cd(2) if dovertical else canvas.cd(4)

      bkg_histEff.SetTitle('Background rejection in: '+partition_name)
      bkg_histEff.SetLineColor(kRed)
      bkg_histEff.SetMarkerColor(kRed)
      bkg_histEff.GetYaxis().SetTitle('#epsilon('+xname+')')
      bkg_histEff.GetXaxis().SetTitle(xname)
      bkg_histEff.Draw()
      bkg_histEff_corr.SetLineColor(kBlack)
      bkg_histEff_corr.SetMarkerColor(kBlack)
      bkg_histEff_corr.Draw('sames')
      l0.Draw()
      l1.Draw()
      leg2 = TLegend(legend_position[0],legend_position[1]+0.4, legend_position[2],legend_position[3]+0.4)
      setLegend1(leg2)
      leg2.SetHeader('Background rejection in '+partition_name)
      leg2.AddEntry(sgn_histEff,('Old: d = %1.3f')%(b0),'p' )
      lg2 = leg2.AddEntry(sgn_histEff_corr,('New: d = %1.3f + %s %1.3f')%(b,xname,a),'p' )
      lg2.SetTextColor(kRed)
      leg2.SetTextSize(0.03)
      leg2.SetBorderSize(0)
      leg2.Draw()
      atlas_template(pad2,**kwargs)

      pad3 = canvas.cd(3) if dovertical else canvas.cd(2)
      sgn_hist2D.SetTitle('Neural Network output as a function fo nvtx, '+partition_name)
      sgn_hist2D.GetXaxis().SetTitle('Neural Network output (Discriminant)')
      sgn_hist2D.GetYaxis().SetTitle(xname)
      sgn_hist2D.GetZaxis().SetTitle('')
      if not useNoActivationFunctionInTheLastLayer: sgn_hist2D.SetAxisRange(-1,1, 'X' )
      sgn_hist2D.Draw('colz')
      pad3.SetLogz()
      # Add points

      
      g1 = TGraphErrors(len(discr_points), discr_points, np.array(nvtx_points)+limits[0], np.array(error_points), np.zeros(discr_points.shape))
      g1.SetLineWidth(1)
      g1.SetLineColor(kBlue)
      g1.SetMarkerColor(kBlue) 
      g1.Draw("P same")
      # Old threshold line
      l2 = TLine(b0,y_min,b0,y_max)
      l2.SetLineColor(kRed)
      l2.SetLineWidth(2)
      l2.Draw()
      # New threshold line
      l3 = TLine(b,y_min, a*y_max+b, y_max)
      l3.SetLineColor(kBlack)
      l3.SetLineWidth(2)
      l3.Draw()

      atlas_template(pad3,**kwargs)

      pad4 = canvas.cd(4) if dovertical else canvas.cd(5)
      bkg_hist2D.SetTitle('Neural Network output as a function fo nvtx, '+partition_name)
      bkg_hist2D.GetXaxis().SetTitle('Neural Network output (Discriminant)')
      bkg_hist2D.GetYaxis().SetTitle(xname)
      bkg_hist2D.GetZaxis().SetTitle('')
      if not useNoActivationFunctionInTheLastLayer: bkg_hist2D.SetAxisRange(-1,1, 'X' )
      #sgn_hist2D.SetAxisRange(b+y_max*a-0.2,1, 'X' )
      bkg_hist2D.Draw('colz')
      pad4.SetLogz()
      # Add points
      g2 = TGraphErrors(len(discr_points), discr_points, np.array(nvtx_points)+limits[0], np.array(error_points), np.zeros(discr_points.shape))
      g2.SetLineWidth(1)
      g2.SetLineColor(kBlue)
      g2.SetMarkerColor(kBlue) 
      g2.Draw("P same")
      # Old threshold line
      l4 = TLine(b0,y_min,b0,y_max)
      l4.SetLineColor(kRed)
      l4.SetLineWidth(2)
      l4.Draw()
      # New threshold line
      l5 = TLine(b,y_min, a*y_max+b, y_max)
      l5.SetLineColor(kBlack)
      l5.SetLineWidth(2)
      l5.Draw()
      atlas_template(pad4,**kwargs)
      from ROOT import TH1D, kAzure
      from TrigEgammaDevelopments.plots import AutoFixAxes
      pad5 = canvas.cd(5) if dovertical else canvas.cd(3)
      #pad5.SetLogy()
      h5 = TH1D(sgn_hist2D.ProjectionX())
      h6 = TH1D(bkg_hist2D.ProjectionX())
      if max(h5.GetMaximum(),h6.GetMaximum()) > 10*(min(h5.GetMaximum(),h6.GetMaximum())):
        pad5.SetLogy()

      h5.Rebin(10)
      h6.Rebin(10)
      h5.SetLineColor(kAzure+6)
      h5.SetFillColor(kAzure+6)
      h6.SetLineColor(kRed-7)
      h5.Draw()
      h6.Draw('sames')
      AutoFixAxes(pad5,False,False,1.5)
      atlas_template(pad5,**kwargs)

      pad6 = canvas.cd(6)
      #pad6.SetLogy()
      h7 = TH1D(bkg_hist2D.ProjectionX())
      h8 = TH1D(sgn_hist2D.ProjectionX())
      if max(h7.GetMaximum(),h8.GetMaximum()) > 10*(min(h7.GetMaximum(),h8.GetMaximum())):
        pad6.SetLogy()
      
      h7.Rebin(10)
      h8.Rebin(10)
      h7.SetLineColor(kRed-7)
      h7.SetFillColor(kRed-7)
      h8.SetLineColor(kAzure+6)
      h7.Draw()
      h8.Draw('sames')
      AutoFixAxes(pad6,False,False,1.5)
      atlas_template(pad6,**kwargs)
      canvas.SaveAs(output_name+'.pdf')    

    return b,a,b0


