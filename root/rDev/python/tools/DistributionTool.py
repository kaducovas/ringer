__all__ = ['DistributionTool']

from TrigEgammaDevelopments.tools  import EgammaBaseTool
from TrigEgammaDevelopments        import StatusCode
from RingerCore                    import retrieve_kw
from TrigEgammaDevelopments.helper import ringer_tuning_etbins, ringer_tuning_etabins
 
class DistributionTool( EgammaBaseTool ):

  def __init__(self, name, **kw):
    
    EgammaBaseTool.__init__(self, name)
    self._basepath = 'Event/DistributionTool'
    self._etBins   = ringer_tuning_etbins
    self._etaBins  = ringer_tuning_etabins
    self._mcId     = []
    self._dataId   = []
    self._discrList= []
    self._dirname  = str()
    self._doZeros  = False

  def setEtBinningValues( self, etbins):
    self._etBins = etbins

  def setEtaBinningValues( self, etabins):
    self._etaBins = etabins

  def setDiscriminantList( self, d ):
    self._discrList = d

  def setMCId(self, id):
    self._mcId.append(id)

  def setDataId(self, id):
    self._dataId.append(id)

  def setDir(self, dname):
    self._dirname = dname

  def currentDir(self):
    return self._dirname

  @property
  def doZeros(self):
    self._doZeros

  @doZeros.setter
  def doZeros(self, v):
    self._doZeros=v


  def initialize(self):
    
    self.bookCaloRings()
    self.bookShowerShapes()
    self.bookDiscriminant()
    self.init_lock()
    return StatusCode.SUCCESS


  def execute(self):
    
    eventInfo = self.retrieve('EventInfo')

    # Get the correct directory
    if eventInfo.id() in self._mcId:
      self.setDir('MonteCarlo')
    elif eventInfo.id() in self._dataId:
      self.setDir('Data')
    else:
      return StatusCode.SUCCESS


    self.fillCaloRings()
    self.fillShowerShapes() 
    self.fillDiscriminant()

    return StatusCode.SUCCESS


  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS
    
  
  
  # (Private method) retrieve the correct binning range
  def __retrieveBinningIdx(self,et, eta):
    # Fix eta value if > 2.5
    if eta > self._etaBins[-1]:
      eta = self._etaBins[-1]
    if et > self._etBins[-1]:
      et = self._etBins[-1]
    for etBinIdx in range(len(self._etBins)-1):
      for etaBinIdx in range(len(self._etaBins)-1):
        if et >= self._etBins[etBinIdx] and  et <= self._etBins[etBinIdx+1]:
          if eta >= self._etaBins[etaBinIdx] and eta <= self._etaBins[etaBinIdx+1]:
            return etBinIdx, etaBinIdx
    self._logger.fatal('Can not retrieve the correct et (%1.3f)/eta (%1.3f) idx.',et,eta)


  def bookDiscriminant(self):
    # Fill all histograms needed
    dirnames = ['MonteCarlo', 'Data']
    # Loop over main dirs
    from ROOT import TH2F
    import numpy as np
    from TrigEgammaDevelopments.helper import nvtx_bins
    for dirname in dirnames:
      for etBinIdx in range(len(self._etBins)-1):
        for etaBinIdx in range(len(self._etaBins)-1):
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          # Loop over all calo rings
          for algname in self._discrList:
            path = self._basepath+'/'+dirname+'/'+binningname+'/'+algname
            self.storeSvc().mkdir( path )
            # create neural network histograms
            self.storeSvc().addHistogram(TH2F('discriminantVsNvtx', 
              'Offline Pileup as function of the discriminant;discriminant;nvtx;Count',
              1000, -12,7,len(nvtx_bins)-1,np.array(nvtx_bins)) ) 
            self.storeSvc().addHistogram(TH2F('discriminantVsMu'  , 
              'Online Pileup as function of the discriminant;discriminant;nvtx;Count' ,
              1000, -12,7,100 - 1,0,100) ) 


  def fillDiscriminant(self):
    if self._doTrigger: # Online
      obj = self.retrieve( "FastCalo" )
    else: # Offline
      obj = self.retrieve('Electron')

    from TrigEgammaDevelopments.helper import GeV
    etBinIdx, etaBinIdx = self.__retrieveBinningIdx( obj.et/GeV, abs(obj.eta) )
    # make the et/eta string path
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
    eventInfo = self.retrieve( "EventInfo" )
    nvtx = eventInfo.nvtx
    avgmu = eventInfo.avgmu
 
    for algname in self._discrList:
      path = self._basepath+'/'+self.currentDir()+'/'+binningname+'/'+algname
      try:
        discriminant = obj.getDecor(algname+'_discriminant')
        self.storeSvc().histogram(path+'/discriminantVsMu').Fill(discriminant,avgmu)
        self.storeSvc().histogram(path+'/discriminantVsNvtx').Fill(discriminant,nvtx)
      except:
        pass



  def bookCaloRings(self):
    # Fill all histograms needed
    dirnames = ['MonteCarlo', 'Data']
    # Loop over main dirs
    from ROOT import TH1F
    for dirname in dirnames:
      for etBinIdx in range(len(self._etBins)-1):
        for etaBinIdx in range(len(self._etaBins)-1):
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          # Loop over all calo rings
          for r in range( 100 ):
            path = self._basepath+'/'+dirname+'/'+binningname+'/rings'
            self.storeSvc().mkdir( path )
            self.storeSvc().addHistogram(TH1F('ring_'+str(r),'ring distribution;ring_{'+str(r)+'};Count', 21000, -1000, 20000))
          # loop over rings


  def fillCaloRings(self):

    if self._doTrigger: # Online
      obj = self.retrieve( "FastCalo" )
    else: # Offline
      obj = self.retrieve('Electron')

    from TrigEgammaDevelopments.helper import GeV
    etBinIdx, etaBinIdx = self.__retrieveBinningIdx( obj.et/GeV, abs(obj.eta) )
    # make the et/eta string path
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
    rings = obj.ringer_rings
    
    for r in range(len(rings)):
      path = self._basepath+'/'+ self.currentDir()+ '/'+binningname+'/rings'
      if self._doZeros:
        self.storeSvc().histogram( path+ ('/ring_%d')%(r) ).Fill( rings[r] )
      else:
        if rings[r] != 0.:
          self.storeSvc().histogram( path+ ('/ring_%d')%(r) ).Fill( rings[r] )
    # Loop over rings


  
  def bookShowerShapes(self):
    import numpy as np
    from ROOT import TH1F, TProfile
    from TrigEgammaDevelopments.helper.constants import default_etabins, nvtx_bins
    etabins = default_etabins

    dirnames = ['MonteCarlo', 'Data']
    
    # Fill all histograms needed
    for dirname in dirnames:
      
      for etBinIdx in range(len(self._etBins)-1):

        for etaBinIdx in range(len(self._etaBins)-1):

          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          path = self._basepath+'/'+dirname+'/'+binningname
          self.storeSvc().mkdir( path )
          self.storeSvc().addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', 150, 0, 150))
          self.storeSvc().addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(etabins)-1, np.array(etabins)))
          self.storeSvc().addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", 20, -3.2, 3.2));
          self.storeSvc().addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', 16, 0, 80))
          self.storeSvc().addHistogram(TH1F('nvtx' ,'N_{vtx} distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
          self.storeSvc().addHistogram(TH1F('eratio','eratio distribution;eratio;Count', 100, 0, 1))
          self.storeSvc().addHistogram(TH1F('reta','reta distribution;reta;Count', 100, 0.6, 1.4))
          self.storeSvc().addHistogram(TH1F('rphi','rphi distribution;rphi;Count', 100, 0.5, 1.0))
          self.storeSvc().addHistogram(TH1F('rhad','rhad distribution;rhad;Count', 100, -0.02, 0.05))
          self.storeSvc().addHistogram(TH1F('weta2','weta2 distribution;weta2;Count', 100, 0, 0.02))
          self.storeSvc().addHistogram(TH1F('f1','f1 distribution;f1;Count', 100, 0, 0.5))
          self.storeSvc().addHistogram(TH1F('f3','f3 distribution;f3;Count', 100, 0, 0.1))
 

  def fillShowerShapes(self):

    if self._doTrigger:
      obj = self.retrieve('FastCalo')
    else:
      obj = self.retrieve('Electron')

    # If is trigger, the position must use the trigger et/eta positions.
    from TrigEgammaDevelopments.helper import GeV
    etBinIdx, etaBinIdx = self.__retrieveBinningIdx( obj.et/GeV, abs(obj.eta) )

    # Force this to be the offline object
    el = self.retrieve('Electron')
    eventInfo = self.retrieve( "EventInfo" )
    nvtx = eventInfo.nvtx
    avgmu = eventInfo.avgmu
    
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
    path = self._basepath+'/'+ self.currentDir()+ '/'+binningname
    self.storeSvc().histogram(path+'/et').Fill(el.et/GeV)
    self.storeSvc().histogram(path+'/eta').Fill(el.eta)
    self.storeSvc().histogram(path+'/phi').Fill(el.phi)
    self.storeSvc().histogram(path+'/mu').Fill(avgmu)
    self.storeSvc().histogram(path+'/nvtx').Fill(nvtx)
    self.storeSvc().histogram(path+'/reta').Fill(el.reta)
    self.storeSvc().histogram(path+'/rphi').Fill(el.rphi)
    self.storeSvc().histogram(path+'/rhad').Fill(el.rhad)
    self.storeSvc().histogram(path+'/weta2').Fill(el.weta2)
   
    # Fill zeros values
    if self._doZeros:
      self.storeSvc().histogram(path+'/eratio').Fill(el.eratio)
      self.storeSvc().histogram(path+'/f1').Fill(el.f1)
      self.storeSvc().histogram(path+'/f3').Fill(el.f3)
    else:
      if el.eratio>0:   self.storeSvc().histogram(path+'/eratio').Fill(el.eratio)
      if el.f1>0:       self.storeSvc().histogram(path+'/f1').Fill(el.f1)
      if el.f3>0:       self.storeSvc().histogram(path+'/f3').Fill(el.f3)

 

  def plot(self, **kw):
    
    from ROOT import kRed
    dirname   = retrieve_kw(kw, 'dirname'  , 'Distribution' )
    basecolor = retrieve_kw(kw, 'basecolor', kRed-7         )  
    pdftitle  = retrieve_kw(kw, 'pdftitle' , 'Distributions')
    pdfoutput = retrieve_kw(kw, 'pdfoutput' , 'distributions')

    import os
    # Organize outputs (.py and .pdf)
    prefix = self._basepath.split('/')[-1]
    localpath = os.getcwd()+'/'+dirname+'/'+prefix
    
    try:
      if not os.path.exists(localpath):
        os.makedirs(localpath)
    except:
      self._logger.warning('The director %s exist.', localpath)

    hist_names = ['et','eta','mu','nvtx','reta','eratio','weta2','rhad','rphi','f1','f3']
    hist_labels = ['E_{T}',"#eta","<#mu>",'N_{vtx}','R_{eta}','E_{ratio}','W_{eta2}','R_{had}','R_{phi}','f_{1}','f_{3}']

    from ROOT import TCanvas, TH1F, gStyle, TLegend, TPad
    from ROOT import kGreen,kRed,kBlue,kBlack,kGray,gPad,kAzure
    from TrigEgammaDevelopments.plots.AtlasStyle import AtlasStyle, atlas_template, setLegend1
     
    canvas1 = TCanvas('canvas1','canvas1',2500,1600)
    canvas1.Divide(4,3)

    # Concatenate distributions for all regions
    def sumAllRegions(histname):
      h=None
      for etBinIdx in range(len(self._etBins)-1):
        for etaBinIdx in range(len(self._etaBins)-1):
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          path = self._basepath+'/'+ self.currentDir()+ '/'+binningname
          if h:
            h += self.storeSvc().histogram(path+'/'+histname)
          else:
            h  = self.storeSvc().histogram(path+'/'+histname).Clone()
      return h

     
    collector=[]
    figures = {'rings':[],'rnnOutput':[],'ringer_profile':str(), 'shower_shapes':str()}
    """
      Plot all shower shapes distributins
    """
    for idx, histname in enumerate(hist_names): 
      self.setDir('Data')
      h_data = sumAllRegions(histname)
      self.setDir('MonteCarlo')
      h_mc   = sumAllRegions(histname)
      #h_mc, h_data =  self.__scale_histograms(h_mc, h_data, 100, 0.01, 0.01)
      
      pad=canvas1.cd(idx+1)
      gStyle.SetOptStat(110011)
      collector.append(pad)
      
      h_mc.SetFillColor(basecolor)
      h_mc.SetLineColor(basecolor)
      h_data.SetLineColor(kBlack)
      h_mc.Scale( 1./h_mc.GetMaximum() )
      h_data.Scale( 1./h_data.GetMaximum() )
      h_mc.Draw()
      h_data.Draw('same')
      leg1 = TLegend(0.2,0.75,0.5,0.95)
      setLegend1(leg1)
      leg1.AddEntry(h_mc,'MC')
      leg1.AddEntry(h_data,'Data')
      leg1.Draw()
      collector[-1].Update()
      collector.append(h_mc)
      collector.append(h_data)
      collector.append(leg1)

    canvas1.SaveAs(localpath+'/shower_shapes_distributions.pdf') 
    figures['shower_shapes'] = localpath+'/shower_shapes_distributions.pdf'


    """
      Plot all shower ringer shapes for each ring
    """
    ratio_size_as_fraction=0.35
    from RingerCore import progressbar
    
    rings_localpath=[]

    for r in progressbar(range(100), 100, step = 1, logger = self._logger,
                         prefix = "Looping over rings (Plotting...) "):
      canvas2 = TCanvas('canvas2','canvas2',2500,1600)
      drawopt='pE1' 
      canvas2.cd()  
      top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
      top.SetBottomMargin(0.0)
      top.SetBottomMargin(0.06/float(top.GetHNDC()))
      #top.SetTopMargin   (0.04/float(top.GetHNDC()))
      top.SetRightMargin (0.05 )
      top.SetLeftMargin  (0.16 )
      top.SetFillColor(0)
      top.Draw(drawopt)
      
      canvas2.cd()
      bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
      bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
      #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
      bot.SetTopMargin   (0.0)
      bot.SetRightMargin (0.05)
      bot.SetLeftMargin  (0.16)
      bot.SetFillColor(0)
      bot.Draw(drawopt)

      self.setDir('MonteCarlo')
      h_mc = sumAllRegions('rings/ring_'+str(r))
      self.setDir('Data')
      h_data = sumAllRegions('rings/ring_'+str(r))
      gStyle.SetOptStat(000000)

      h_mc, h_data =  self.__scale_histograms(h_mc, h_data, 100, 0.0001, 0.025)
      h_mc.Scale( 1./h_mc.GetMaximum() )
      h_data.Scale( 1./h_data.GetMaximum() )
 
      from ROOT import TH1,kGray
      divide=""
      drawopt='pE1'
      bot.cd()
      ref= h_mc.Clone()
      h  = h_data.Clone()

      ref.Sumw2()
      h.Sumw2()
      ratioplot = h.Clone()
      ratioplot.Sumw2()
      ratioplot.SetName(h.GetName()+'_ratio')
      ratioplot.Divide(h,ref,1.,1.,'')
      ratioplot.SetFillColor(0)
      ratioplot.SetFillStyle(0)
      ratioplot.SetMarkerColor(1)
      ratioplot.SetLineColor(kGray)
      ratioplot.SetMarkerStyle(24)
      ratioplot.SetMarkerSize(1.2)
      ratioplot.GetYaxis().SetTitleSize(0.10)
      ratioplot.GetXaxis().SetTitleSize(0.10)
      ratioplot.GetXaxis().SetLabelSize(0.10)
      ratioplot.GetYaxis().SetLabelSize(0.10)
      ratioplot.GetYaxis().SetRangeUser(-1.6,3.7)
      ratioplot.GetYaxis().SetTitleOffset(0.7)
      ratioplot.GetYaxis().SetTitle('Data/MC')
      ratioplot.GetXaxis().SetTitle('Ring #'+str(r+1)+' [MeV]')
      ratioplot.Draw(drawopt)
      from ROOT import TLine
      
      nbins = h_data.GetNbinsX()
      xmin = h_data.GetXaxis().GetBinLowEdge(1)
      xmax = h_data.GetXaxis().GetBinLowEdge(nbins+1)
      l1 = TLine(xmin,1,xmax,1)
      l1.SetLineColor(kRed)
      l1.SetLineStyle(2)
      l1.Draw()
      bot.Update()
      
      top.cd()

      h_mc.SetFillColor(basecolor)
      h_mc.SetLineWidth(1)
      h_mc.SetLineColor(basecolor)
      h_data.SetLineColor(kBlack)
      h_data.SetLineWidth(1)
      h_mc.GetYaxis().SetTitle('Count')
      h_mc.Draw()
      h_data.Draw('same')

      leg1 = TLegend(0.8,0.70,0.95,0.95)
      setLegend1(leg1)
      leg1.AddEntry(h_mc,'MC')
      leg1.AddEntry(h_data,'Data')
      leg1.Draw()
      atlas_template(top)
      top.Update()
      canvas2.SaveAs(localpath+'/distribution_ring_'+str(r+1)+'.pdf') 
      figures['rings'].append(localpath+'/distribution_ring_'+str(r+1)+'.pdf') 

    
    """
      Plot ringer mean shapes
    """
    h_mean_data = TH1F('h_mean_data','',100, 0, 100)
    h_mean_mc = TH1F('h_mean_mc'    ,'',100  , 0, 100  )

    for bin in range(100):
      self.setDir('MonteCarlo')
      h_mc = sumAllRegions('rings/ring_'+str(bin))
      self.setDir('Data')
      h_data = sumAllRegions('rings/ring_'+str(bin))
      h_mean_data.SetBinContent(bin+1, h_data.GetMean())
      h_mean_mc.SetBinContent(bin+1, h_mc.GetMean())
    canvas3 = TCanvas('canvas3','canvas3',2500,1600)
    
    drawopt='pE1' 
    canvas3.cd()  
    top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
    top.SetBottomMargin(0.0)
    top.SetBottomMargin(0.06/float(top.GetHNDC()))
    #top.SetTopMargin   (0.04/float(top.GetHNDC()))
    top.SetRightMargin (0.05 )
    top.SetLeftMargin  (0.16 )
    top.SetFillColor(0)
    top.Draw(drawopt)
    
    canvas3.cd()
    bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
    bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
    #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
    bot.SetTopMargin   (0.0)
    bot.SetRightMargin (0.05)
    bot.SetLeftMargin  (0.16)
    bot.SetFillColor(0)
    bot.Draw(drawopt)


    gStyle.SetOptStat(000000)
    from ROOT import TH1,kGray
    divide=""
    drawopt='pE1'
    bot.cd()
    ref= h_mean_mc.Clone()
    h  = h_mean_data.Clone()
    ref.Sumw2()
    h.Sumw2()
    ratioplot = h.Clone()
    ratioplot.Sumw2()
    ratioplot.SetName(h.GetName()+'_ratio')
    ratioplot.Divide(h,ref,1.,1.,'')
    ratioplot.SetFillColor(0)
    ratioplot.SetFillStyle(0)
    ratioplot.SetMarkerColor(1)
    ratioplot.SetLineColor(kGray)
    ratioplot.SetMarkerStyle(24)
    ratioplot.SetMarkerSize(1.2)
    ratioplot.GetYaxis().SetTitleSize(0.10)
    ratioplot.GetXaxis().SetTitleSize(0.10)
    ratioplot.GetXaxis().SetLabelSize(0.10)
    ratioplot.GetYaxis().SetLabelSize(0.10)
    ratioplot.GetYaxis().SetRangeUser(-1.6,3.7)
    ratioplot.GetYaxis().SetTitleOffset(0.7)
    ratioplot.GetYaxis().SetTitle('Data/MC')
    ratioplot.GetXaxis().SetTitle('Rings')
    ratioplot.Draw(drawopt)
    from ROOT import TLine
    
    nbins = h_mean_data.GetNbinsX()
    xmin = h_mean_data.GetXaxis().GetBinLowEdge(1)
    xmax = h_mean_data.GetXaxis().GetBinLowEdge(nbins+1)
    l1 = TLine(xmin,1,xmax,1)
    l1.SetLineColor(kRed)
    l1.SetLineStyle(2)
    l1.Draw()
    bot.Update()
    
    top.cd()
    h_mean_mc.SetFillColor(basecolor)
    h_mean_mc.SetLineWidth(1)
    h_mean_mc.SetLineColor(basecolor)
    h_mean_data.SetLineColor(kBlack)
    h_mean_data.SetLineWidth(1)
    #h_mean_mc.Scale( 1./h_mean_mc.GetEntries() )
    #h_mean_data.Scale( 1./h_mean_data.GetEntries() )

    
    if h_mean_mc.GetMaximum()>h_mean_data.GetMaximum():
      ymin=h_mean_mc.GetMinimum()
      ymax=h_mean_mc.GetMaximum()
      h_mean_mc.Draw()
      h_mean_mc.GetYaxis().SetTitle('E[Ring] MeV')
      h_mean_data.Draw('same')
    else:
      ymin=h_mean_data.GetMinimum()
      ymax=h_mean_data.GetMaximum()
      h_mean_data.GetYaxis().SetTitle('E[Ring] MeV')
      h_mean_data.Draw()
      h_mean_mc.Draw('same')

    h_mean_data.Draw('same')
    # prepare ringer lines
    def gen_line_90(x , ymin,ymax,text):
      from ROOT import TLine,TLatex
      ymax=1.05*ymax
      l=TLine(x,ymin,x,ymax)
      l.SetLineStyle(2)
      l.Draw()
      txt = TLatex()
      txt.SetTextFont(12)
      txt.SetTextAngle( 90 )
      txt.SetTextSize(0.04)
      txt.DrawLatex(x-1, (ymax-ymin)/2., text)
      return l,txt

    l_ps,t_ps=gen_line_90(8, ymin,ymax, 'presampler')
    l_em1,t_em1=gen_line_90(72, ymin,ymax, 'EM.1')
    l_em2,t_em2=gen_line_90(80, ymin,ymax, 'EM.2')
    l_em3,t_em3=gen_line_90(88, ymin,ymax, 'EM.3')
    l_had1,t_had1=gen_line_90(92, ymin,ymax, 'Had.1')
    l_had2,t_had2=gen_line_90(96, ymin,ymax, 'Had.2')
    l_had3,t_had3=gen_line_90(100, ymin,ymax, 'Had.3')

    leg1 = TLegend(0.8,0.70,0.95,0.95)
    setLegend1(leg1)
    leg1.AddEntry(h_mean_mc,'MC')
    leg1.AddEntry(h_mean_data,'Data')
    leg1.Draw()
    atlas_template(top)
    top.Update()

    canvas3.SaveAs(localpath+'/ringer_profile.pdf') 
    figures['ringer_profile'] = localpath+'/ringer_profile.pdf'



    """
      Plot all NN distributions for each calo region
    """
    for algname in self._discrList:
      for etBinIdx in range(len(self._etBins)-1):
        for etaBinIdx in range(len(self._etaBins)-1):
        
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          path = self._basepath+'/MonteCarlo/'+binningname
          h_mc = self.storeSvc().histogram(path+'/'+algname+'/discriminantVsMu').ProjectionX().Clone() 
          path = self._basepath+'/Data/'+binningname
          h_data = self.storeSvc().histogram(path+'/'+algname+'/discriminantVsMu').ProjectionX().Clone()        
          h_mc.Rebin(10)
          h_data.Rebin(10)
          h_mc.Scale( 1./h_mc.GetMaximum() )
          h_data.Scale( 1./h_data.GetMaximum() )

 
          canvas4 = TCanvas('canvas4','canvas4',2500,1600)
          drawopt='pE1' 
          canvas4.cd()  
          top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
          top.SetBottomMargin(0.0)
          top.SetBottomMargin(0.06/float(top.GetHNDC()))
          #top.SetTopMargin   (0.04/float(top.GetHNDC()))
          top.SetRightMargin (0.05 )
          top.SetLeftMargin  (0.16 )
          top.SetFillColor(0)
          top.Draw(drawopt)
          
          canvas4.cd()
          bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
          bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
          bot.SetTopMargin   (0.0)
          bot.SetRightMargin (0.05)
          bot.SetLeftMargin  (0.16)
          bot.SetFillColor(0)
          bot.Draw(drawopt)


          gStyle.SetOptStat(000000)

          from ROOT import TH1, kGray
          divide=""
          drawopt='pE1'
          bot.cd()
          ref= h_mc.Clone()
          h  = h_data.Clone()
          ref.Sumw2()
          h.Sumw2()
          ratioplot = h.Clone()
          ratioplot.Sumw2()
          ratioplot.SetName(h.GetName()+'_ratio')
          ratioplot.Divide(h,ref,1.,1.,'')
          ratioplot.SetFillColor(0)
          ratioplot.SetFillStyle(0)
          ratioplot.SetMarkerColor(1)
          ratioplot.SetLineColor(kGray)
          ratioplot.SetMarkerStyle(24)
          ratioplot.SetMarkerSize(1.2)
          ratioplot.GetYaxis().SetTitleSize(0.10)
          ratioplot.GetXaxis().SetTitleSize(0.10)
          ratioplot.GetXaxis().SetLabelSize(0.10)
          ratioplot.GetYaxis().SetLabelSize(0.10)
          ratioplot.GetYaxis().SetRangeUser(-1.6,3.7)
          ratioplot.GetYaxis().SetTitleOffset(0.7)
          ratioplot.GetYaxis().SetTitle('Data/MC')
          ratioplot.GetXaxis().SetTitle('Neural Network (Discriminant)')
          ratioplot.Draw(drawopt)
          from ROOT import TLine
          
          nbins = h_data.GetNbinsX()
          xmin = h_data.GetXaxis().GetBinLowEdge(1)
          xmax = h_data.GetXaxis().GetBinLowEdge(nbins+1)
          l1 = TLine(xmin,1,xmax,1)
          l1.SetLineColor(kRed)
          l1.SetLineStyle(2)
          l1.Draw()
          bot.Update()
          
          top.cd()
          h_mc.SetFillColor(basecolor)
          h_mc.SetLineWidth(1)
          h_mc.SetLineColor(basecolor)
          h_data.SetLineColor(kBlack)
          h_data.SetLineWidth(1)
          h_mc.Scale( 1./h_mc.GetMaximum() )
          h_data.Scale( 1./h_data.GetMaximum() )
          h_mc.GetYaxis().SetTitle(('Counts (%s)')%(binningname.replace('_',',')))
          h_mc.Draw()
          h_data.Draw('same')

          leg1 = TLegend(0.8,0.70,0.95,0.95)
          setLegend1(leg1)
          leg1.AddEntry(h_mc,'MC')
          leg1.AddEntry(h_data,'Data')
          leg1.Draw()
          atlas_template(top)
          top.Update()
          canvas4.SaveAs(localpath+'/'+algname+'_rnnOutput_'+binningname+'.pdf') 
          figures['rnnOutput'].append(localpath+'/'+algname+'_rnnOutput_'+binningname+'.pdf') 


    #from RingerCore.tex.TexAPI import *
    from RingerCore.tex.BeamerAPI import BeamerTexReportTemplate1,BeamerSection,BeamerMultiFigureSlide,BeamerFigureSlide
    with BeamerTexReportTemplate1( theme = 'Berlin'
                                 , _toPDF = True
                                 , title = pdftitle
                                 , outputFile = pdfoutput
                                 , font = 'structurebold' ):

      with BeamerSection( name = 'Shower Shapes' ):
        BeamerMultiFigureSlide( title = 'Shower Shapes (MC and Data)'
                      , paths = [figures['shower_shapes']]
                      , nDivWidth = 1 # x
                      , nDivHeight = 1 # y
                      , texts=None
                      , fortran = False
                      , usedHeight = 0.8
                      , usedWidth = 1.1
                      )

      with BeamerSection( name = 'Ringer Shapes Profile' ):
        BeamerMultiFigureSlide( title = 'Ringer Profile (MC and Data)'
                      , paths = [figures['ringer_profile']]
                      , nDivWidth = 1 # x
                      , nDivHeight = 1 # y
                      , texts=None
                      , fortran = False
                      , usedHeight = 0.8
                      , usedWidth = 1.1
                      )
 
      with BeamerSection( name = 'Ringer Shapes' ):
        for s in range(4):
          paths1=[path for path in figures['rings'][ s*25:s*25+25]]
          BeamerMultiFigureSlide( title = 'Ringer Shapes (MC and Data)'
                        , paths = paths1
                        , nDivWidth = 5 # x
                        , nDivHeight = 5 # y
                        , texts=None
                        , fortran = False
                        , usedHeight = 0.8
                        , usedWidth = 1.1
                        )
          
      for algname in self._discrList:
        with BeamerSection( name = ('%s Neural Network Output')%(algname.replace('_','\_')) ):
          paths2 = []
          for etBinIdx in range(len(self._etBins)-1):
            for etaBinIdx in range(len(self._etaBins)-1):
              binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
              paths2.append(localpath+'/'+algname+'_rnnOutput_'+binningname+'.pdf') 
          BeamerMultiFigureSlide( title = algname.replace('_','\_')
                        , paths = paths2
                        , nDivWidth = len(self._etaBins) # x
                        , nDivHeight = len(self._etBins) # y
                        , texts=None
                        , fortran = False
                        , usedHeight = 1.0
                        , usedWidth = 1.1
                        )
          




    return StatusCode.SUCCESS

  
  def __scale_histograms(self, h_mc, h_data, nbins, percentage_left, percentage_right):

    # Internal method
    def getXrange(h,percentage_left, percentage_right):
      mean_bin = h.FindBin( h.GetMean() )
      firstValue=None; lastValue=None
      for bx in range(h.GetNbinsX()):
        if h.Integral(-1,bx+1)/float(h.GetEntries()) >= percentage_left :
          firstValue = h.GetBinCenter(bx) - 0.5
          xbin_min = bx
          break
      for bx in range(h.GetNbinsX(),-1,-1):
        if h.Integral(bx+1,h.GetNbinsX()+1)/float(h.GetEntries()) >= percentage_right :
          lastValue = h.GetBinCenter(bx) + 0.5
          xbin_max = bx
          break
      return firstValue, lastValue, xbin_min, xbin_max

    f1,l1,bx1_min, bx1_max = getXrange( h_mc , percentage_left, percentage_right)
    f2,l2,bx2_min, bx2_max = getXrange(h_data, percentage_left, percentage_right)
    f = min(f1,f2)
    l = max(l1,l2)
    bx_min = min(bx1_min,bx2_min)
    bx_max = max(bx1_max,bx2_max)
    bins = int(l-f)
    from ROOT import TH1F
    h_mc_scaled  = TH1F('h_mc_scaled','',bins,f,l)
    h_mc_scaled.SetTitle(h_mc.GetTitle())
    h_data_scaled  = TH1F('h_data_scaled','',bins,f,l)
    h_data_scaled.SetTitle(h_data.GetTitle())
    
    for idx, bx in enumerate(range(bx_min, bx_max)):
      h_mc_scaled.SetBinContent( idx+1, h_mc.GetBinContent(bx+1) )
      h_data_scaled.SetBinContent( idx+1, h_data.GetBinContent(bx+1) )

    scale=bins/nbins
    h_mc_scaled.Rebin(scale)
    h_data_scaled.Rebin(scale)
    return h_mc_scaled, h_data_scaled
 


