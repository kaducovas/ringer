__all__ = ['QuadrantTool']

from TrigEgammaDevelopments.tools import EgammaBaseTool
from TrigEgammaDevelopments       import StatusCode
from RingerCore                   import retrieve_kw


class QuadrantTool( EgammaBaseTool ):

  def __init__(self, name, **kw):
    EgammaBaseTool.__init__(self, name)
    self._basepath = 'Event/QuadrantTool'
    self._quadrantNames = list()
    self._etBins  = [0, 100000]
    self._etaBins = [0, 2.5]
    

  def add_quadrant( self, branch_x, branch_y, **kwargs):

    dependence_item = retrieve_kw( kwargs, 'dependence_item', 1 )
    alias = retrieve_kw( kwargs, 'alias' , [] )
    # check correct value
    if dependence_item>1:
      self._logger.fatal('The third argument must be -1 (no NN dependence), 0 (first alg) or 1 (second alg)')
    self._quadrantNames.append( (branch_x, branch_y, dependence_item, alias) )

  def setEtBinningValues( self, etbins ):
    self._etBins = etbins
  
  def setEtaBinningValues( self, etabins ):
    self._etaBins = etabins

  def initialize(self):
    
    import numpy as np
    from TrigEgammaDevelopments.helper.constants import zee_etbins, default_etabins, nvtx_bins
    etbins  = zee_etbins
    etabins = default_etabins
 
    from ROOT import TH2F, TProfile
    # Fill all histograms needed
    for info in self._quadrantNames:
      name = info[0]+'_X_'+info[1] 

      for etBinIdx in range(len(self._etBins)-1):
        for etaBinIdx in range(len(self._etaBins)-1):
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          quadrant   = ['passed_passed','rejected_rejected','passed_rejected','rejected_passed']
          for q in quadrant:
            dirname = self._basepath+'/'+name+'/'+binningname+'/'+q  
            self.storeSvc().mkdir( dirname )
            self.storeSvc().addHistogram(TH2F('et','discriminant Vs E_{T} distribution;rnnOutput;E_{T};Count', 1000, -12, 7 ,140, 0, 140))
            self.storeSvc().addHistogram(TH2F('eta','discriminant Vs #eta distribution;rnnOutput;#eta;Count', 1000,-12,7, len(etabins)-1, np.array(etabins)))
            self.storeSvc().addHistogram(TH2F("phi", "discriminant Vs #phi distribution;rnnOutput;#phi;Count", 1000,-12,7,20, -3.2, 3.2))
            self.storeSvc().addHistogram(TH2F('mu' ,'discriminant Vs <#mu> distribution;rnnOutput;<#mu>;Count', 1000,-12,7,16, 0, 80))
            self.storeSvc().addHistogram(TH2F('nvtx' ,'discriminant Vs N_{vtx} distribution;rnnOutput;N_{vtx};Count', 1000,-12,7,len(nvtx_bins)-1, np.array(nvtx_bins)))
            self.storeSvc().addHistogram(TH2F('eratio','discriminant Vs eratio distribution;rnnOutput;eratio;Count',1000,-12,7, 20, 0, 1))
            self.storeSvc().addHistogram(TH2F('reta','discriminant Vs reta distribution;rnnOutput;reta;Count',1000,-12,7, 20, 0.6, 1.4))
            self.storeSvc().addHistogram(TH2F('rphi','discriminant Vs rphi distribution;rnnOutput;rphi;Count',1000,-12,7, 20, 0.5, 1.0))
            self.storeSvc().addHistogram(TH2F('rhad','discriminant Vs rhad distribution;rnnOutput;rhad;Count',1000,-12,7, 20, -0.02, 0.05))
            self.storeSvc().addHistogram(TH2F('weta2','discriminant Vs weta2 distribution;rnnOutput;weta2;Count',1000,-12,7, 20, 0, 0.02))
            self.storeSvc().addHistogram(TH2F('f1','discriminant Vs f1 distribution;rnnOutput;f1;Count',1000,-12,7, 20, 0, 0.5))
            self.storeSvc().addHistogram(TH2F('f3','discriminant Vs f3 distribution;rnnOutput;f3;Count',1000,-12,7, 20, 0, 0.1))
          # loop over quadrants
    # loop over pairs
    self.init_lock()
    return StatusCode.SUCCESS


  def __get_discriminat( self, pidname ):
    fc = self.retrieve("FastCalo"); el = self.retrieve("Electron")
    # remove spaces if exist
    pidname = pidname.replace(' ','')
    # Check conditions strings
    if '&' in pidname:
      pidname = pidname.split('&')
    elif '||' in pidname:
      pidname = pidname.split('||')
    else:
      pidname = [pidname]

    for pid in pidname:
      # Apply on trigger features
      if ('L2Calo' in pid) or ('L2' in pid) or ('EFCalo' in pid) or ('HLT' in pid):
        obj=fc
      else: # Apply on Offline electron features
        obj=el

      if pid+'_discriminant' in obj.decorations():
        return obj.getDecor(pid+'_discriminant')
    return 0

  def execute(self):

    from TrigEgammaDevelopments.helper.constants import GeV
    # Retrieve Electron container
    el = self.retrieve( "Electron" )
    el.execute()
    eventInfo = self.retrieve( "EventInfo" )
    et = el.et/GeV
    eta = abs(el.eta)
    nvtx = eventInfo.nvtx
    avgmu = eventInfo.avgmu
    eratio = el.eratio
    reta = el.reta
    # Retrieve the correct index
    etBinIdx, etaBinIdx = self.__retrieveBinningIdx(et,eta)
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)

    for info in self._quadrantNames:

      name     = info[0]+'_X_'+info[1] 
      dItem    = info[2]
      passed_x = self.ApplyElectronSelection( info[0] )
      passed_y = self.ApplyElectronSelection( info[1] )

      if dItem < 0: # check the dependence item t retrieve the NN value
        discriminant = 0
      else:# try to find the discriminant inside of this pidname
        discriminant = self.__get_discriminat( pair[dItem] )

      passed_x = 'passed' if passed_x else 'rejected'
      passed_y = 'passed' if passed_y else 'rejected'
      dirname = self._basepath+'/'+name+'/'+binningname+'/'+passed_x +'_'+ passed_y
      self.storeSvc().histogram(dirname+'/et').Fill(discriminant,et)
      self.storeSvc().histogram(dirname+'/eta').Fill(discriminant,el.eta)
      self.storeSvc().histogram(dirname+'/phi').Fill(discriminant,el.phi)
      self.storeSvc().histogram(dirname+'/mu').Fill(discriminant,avgmu)
      self.storeSvc().histogram(dirname+'/nvtx').Fill(discriminant,nvtx)
      self.storeSvc().histogram(dirname+'/reta').Fill(discriminant,el.reta)
      self.storeSvc().histogram(dirname+'/rphi').Fill(discriminant,el.rphi)
      self.storeSvc().histogram(dirname+'/rhad').Fill(discriminant,el.rhad)
      self.storeSvc().histogram(dirname+'/f1').Fill(discriminant,el.f1)
      self.storeSvc().histogram(dirname+'/f3').Fill(discriminant,el.f3)
      self.storeSvc().histogram(dirname+'/weta2').Fill(discriminant,el.weta2)
      self.storeSvc().histogram(dirname+'/eratio').Fill(discriminant,el.eratio)

    return StatusCode.SUCCESS


  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS
    

  def plot(self, **kw):

    dirname = retrieve_kw(kw, 'dirname', 'Quadrant')
    aliasMap = retrieve_kw(kw,'alias_map', {'xx':'BothPassed','oo':'BothReject','xo':'OnlyPassedLH','ox':'OnlyPassedRinger'})
    pdftitle  = retrieve_kw(kw, 'pdftitle' , 'Quadrant')
    pdfoutput = retrieve_kw(kw, 'pdfoutput' , 'quadrant')

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
 
    def sumAllRegions(histname):
      h=None
      for etBinIdx in range(len(self._etBins)-1):
        for etaBinIdx in range(len(self._etaBins)-1):
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          path = (histname)%(binningname)
          if h:
            h+= self.storeSvc().histogram(path).ProjectionY()
          else:
            h  = self.storeSvc().histogram(path).ProjectionY().Clone()
      return h

 

    collection=[]
   
    for info in self._quadrantNames:
      for idx, hist in enumerate(hist_names):
        name = info[0]+'_X_'+info[1] 
        dirname = self._basepath+'/'+name+'/%s'
        h_xx = sumAllRegions(dirname+'/passed_passed/'+hist)
        h_xo = sumAllRegions(dirname+'/passed_rejected/'+hist)
        h_ox = sumAllRegions(dirname+'/rejected_passed/'+hist)
        h_oo = sumAllRegions(dirname+'/rejected_rejected/'+hist) 
        # Loop over histograms
        plotname1 = localpath+'/'+prefix+'_'+name+'_'+hist+'.pdf'
        plotname2 = localpath+'/'+prefix+'_'+name+'_'+hist+'_logscale.pdf'
        plotname3 = localpath+'/'+prefix+'_'+name+'_'+hist+'_agreement.pdf'
        plotname4 = localpath+'/'+prefix+'_'+name+'_'+hist+'_agreement_logscale.pdf'
        #self.__plot_quadrant_template1(h_oo.Clone(),h_xo.Clone(),h_ox.Clone(),h_xx.Clone(),aliasMap,hist_labels[idx],plotname1,False)
        #self.__plot_quadrant_template1(h_oo.Clone(),h_xo.Clone(),h_ox.Clone(),h_xx.Clone(),aliasMap,hist_labels[idx],plotname2,True )
        #self.__plot_quadrant_template2(h_oo.Clone(),h_xo.Clone(),h_ox.Clone(),h_xx.Clone(),aliasMap,hist_labels[idx],plotname3,False )
        #self.__plot_quadrant_template2(h_oo.Clone(),h_xo.Clone(),h_ox.Clone(),h_xx.Clone(),aliasMap,hist_labels[idx],plotname4,True )
        collection.append((h_xx,h_xo,h_ox,h_oo) )


    #toPDF=False
    toPDF=True
    if toPDF:
      #from RingerCore.tex.TexAPI import *
      from RingerCore.tex.BeamerAPI import BeamerTexReportTemplate1,BeamerSection,BeamerSubSection,\
                                           BeamerMultiFigureSlide,BeamerFigureSlide
      # apply beamer
      with BeamerTexReportTemplate1( theme = 'Berlin'
                                   , _toPDF = True
                                   , title = pdftitle
                                   , outputFile = pdfoutput
                                   , font = 'structurebold' ):
        
        for info in self._quadrantNames: 

          name = info[0]+'_X_'+info[1]
          section_name = info[3][0].replace('_','\_')
          subsection_name = info[3][1].replace('_','\_')

          with BeamerSection( name = section_name ):
            with BeamerSubSection( name = subsection_name ):
              figures = {'linear':[],'log':[],'diff_linear':[],'diff_log':[]}
              for idx, hist in enumerate(hist_names):
                figures['linear'].append(localpath+'/'+prefix+'_'+name+'_'+hist+'.pdf')
                figures['log'].append(localpath+'/'+prefix+'_'+name+'_'+hist+'_logscale.pdf')
                figures['diff_linear'].append(localpath+'/'+prefix+'_'+name+'_'+hist+'_agreement.pdf')
                figures['diff_log'].append(localpath+'/'+prefix+'_'+name+'_'+hist+'_agreement_logscale.pdf')

              BeamerMultiFigureSlide( title = 'Offline Calo Variables'
                          , paths = figures['linear']
                          , nDivWidth = 4 # x
                          , nDivHeight = 3 # y
                          , texts=None
                          , fortran = False
                          , usedHeight = 0.6
                          , usedWidth = 0.9
                          )

              BeamerMultiFigureSlide( title = 'Offline Calo Variables (shown on log scale)'
                          , paths = figures['log']
                          , nDivWidth = 4 # x
                          , nDivHeight = 3 # y
                          , texts=None
                          , fortran = False
                          , usedHeight = 0.6
                          , usedWidth = 0.9
                          )
              
              BeamerMultiFigureSlide( title = 'Offline Calo Variables (Agreement and Disagrement)'
                          , paths = figures['diff_linear']
                          , nDivWidth = 4 # x
                          , nDivHeight = 3 # y
                          , texts=None
                          , fortran = False
                          , usedHeight = 0.6
                          , usedWidth = 0.9
                          )

              BeamerMultiFigureSlide( title = 'Offline Calo Variables (Agreement and Disagrement show on log scale)'
                          , paths = figures['diff_log']
                          , nDivWidth = 4 # x
                          , nDivHeight = 3 # y
                          , texts=None
                          , fortran = False
                          , usedHeight = 0.6
                          , usedWidth = 0.9
                          )


    return StatusCode.SUCCESS

  def __plot_quadrant_template1( self, h_oo, h_xo, h_ox, h_xx, alias, xlabel, plotname, doLogY):
    
    from TrigEgammaDevelopments.plots import AutoFixAxes
    from TrigEgammaDevelopments.helper.util import setBoxes
    from ROOT import TCanvas, gStyle, TLegend, kRed, kBlue, kGreen, kGray, kBlack,TLine,TPad, TLatex
    from TrigEgammaDevelopments.plots.AtlasStyle import AtlasStyle, atlas_template

    ratio_size_as_fraction=0.35

    # Internal method
    def sortHistograms( hists ):
      nevents = [o.GetEntries() for o in hists]
      from operator import itemgetter
      hist_sorted_index = sorted(enumerate(nevents), key=itemgetter(1))
      hist_sorted=list()
      for index in hist_sorted_index:
        hist_sorted.append(hists[index[0]])
      hist_sorted.reverse()
      return hist_sorted

    hsum =h_xx.Clone();hsum+=h_ox;hsum+=h_xo;hsum+=h_oo
    
    gStyle.SetOptStat(111111111)
    canvas = TCanvas('canvas','canvas',2500,1600)
    drawopt='pE1' 
    canvas.cd()  
    top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
    top.SetBottomMargin(0.0)
    top.SetBottomMargin(0.06/float(top.GetHNDC()))
    #top.SetTopMargin   (0.04/float(top.GetHNDC()))
    top.SetRightMargin (0.05 )
    top.SetLeftMargin  (0.16 )
    top.SetFillColor(0)
    top.Draw(drawopt)
    
    canvas.cd()
    bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
    bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
    #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
    bot.SetTopMargin   (0.0)
    bot.SetRightMargin (0.05)
    bot.SetLeftMargin  (0.16)
    bot.SetFillColor(0)
    bot.Draw(drawopt)

    top.cd()
    
    h_xx.SetLineWidth(1)
    h_xx.SetLineColor(kBlack)
    h_xx.SetMarkerColor(kBlack)

    h_xo.SetLineWidth(1)
    h_xo.SetLineColor(kRed)
    h_xo.SetMarkerColor(kRed)
    
    h_ox.SetLineWidth(1)
    h_ox.SetLineColor(kGreen+1)
    h_ox.SetMarkerColor(kGreen+1)
    
    h_oo.SetLineWidth(1)
    h_oo.SetLineColor(kGray+1)
    h_oo.SetMarkerColor(kGray+1)
    
    h_oo.SetName(alias['oo'])
    h_ox.SetName(alias['ox'])
    h_xo.SetName(alias['xo'])
    h_xx.SetName(alias['xx'])

    h_oo.SetStats(1)
    h_ox.SetStats(1)
    h_xo.SetStats(1)
    h_xx.SetStats(1)
    # top
    h1 = sortHistograms([h_oo,h_ox,h_xo,h_xx])
    # bot
    h2 = sortHistograms([h_oo.Clone(),h_ox.Clone(),h_xo.Clone(),h_xx.Clone()])
    
    h1[0].GetXaxis().SetTitle('')
    h1[0].GetYaxis().SetTitle('Counts')
    h1[0].GetYaxis().SetTitleOffset(1.0)
    h1[0].Draw()
    for i in range(1,len(h1)):
      h1[i].Draw('sames')

    top.Update()
    stats = setBoxes(top,h1)
    
    #TODO: Use this to add the eff line into the tpavestats
    #from ROOT import TPaveStats,TLatex
    #for s in stats:
    #  s.SetName('mystats')
    #  listOfLine = s.GetListOfLines()
    #  tex =TLatex(0,0,"Test = 10")
    #  listOfLine.Add(tex)
   
    #for h in h1:
    #  h.SetStats(0)

    if doLogY:
      top.SetLogy()
      AutoFixAxes(top,False,False,9000)
    else:
      AutoFixAxes(top,False,False,2)

    top.Update()
    
    bot.cd()
    if doLogY:  
      bot.SetLogy()

    hsum.Sumw2()
    for h in h2:
      h.SetStats(0)
      h.Sumw2()
      h.Divide(h,hsum,1.,1.)

    h2[0].GetYaxis().SetTitle('ratio')
    h2[0].GetXaxis().SetTitle(xlabel)
    h2[0].GetYaxis().SetTitleOffset(0.5)
    h2[0].GetYaxis().SetLabelSize(0.10)
    h2[0].GetYaxis().SetTitleSize(0.10)
    h2[0].GetXaxis().SetLabelSize(0.10)
    h2[0].GetXaxis().SetTitleSize(0.10)
    h2[0].Draw('ep1')
    for i in range(1,len(h2)):
      h2[i].Draw('sames')
    AutoFixAxes(bot,False,False,1.1)
    
    # Loop over histograms
    canvas.SaveAs(plotname)
    del canvas, h_oo,h_xo,h_ox,h_xx, h1, h2, hsum




  def __plot_quadrant_template2( self, h_oo, h_xo, h_ox, h_xx, alias, xlabel, plotname, doLogY):
    
    from TrigEgammaDevelopments.plots import AutoFixAxes
    from TrigEgammaDevelopments.helper.util import setBoxes
    from ROOT import TCanvas, gStyle, TLegend, kRed, kBlue, kGreen, kGray, kBlack,TLine,TPad, TLatex
    from TrigEgammaDevelopments.plots.AtlasStyle import AtlasStyle, atlas_template

    ratio_size_as_fraction=0.35

    # Internal method
    def sortHistograms( hists ):
      nevents = [o.GetEntries() for o in hists]
      from operator import itemgetter
      hist_sorted_index = sorted(enumerate(nevents), key=itemgetter(1))
      hist_sorted=list()
      for index in hist_sorted_index:
        hist_sorted.append(hists[index[0]])
      hist_sorted.reverse()
      return hist_sorted

    h_agree = h_xx+h_oo
    h_disagree = h_ox+h_xo
    hsum = h_agree+h_disagree
    
    gStyle.SetOptStat(111111)
    canvas = TCanvas('canvas','canvas',2500,1600)
    drawopt='pE1' 
    canvas.cd()  
    top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
    top.SetBottomMargin(0.0)
    top.SetBottomMargin(0.06/float(top.GetHNDC()))
    #top.SetTopMargin   (0.04/float(top.GetHNDC()))
    top.SetRightMargin (0.05 )
    top.SetLeftMargin  (0.16 )
    top.SetFillColor(0)
    top.Draw(drawopt)
    
    canvas.cd()
    bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
    bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
    #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
    bot.SetTopMargin   (0.0)
    bot.SetRightMargin (0.05)
    bot.SetLeftMargin  (0.16)
    bot.SetFillColor(0)
    bot.Draw(drawopt)

    top.cd()
    
    h_agree.SetLineWidth(1)
    h_agree.SetLineColor(kBlack)
    h_agree.SetMarkerColor(kBlack)

    h_disagree.SetLineWidth(1)
    h_disagree.SetLineColor(kRed)
    h_disagree.SetMarkerColor(kRed)
    
    h_agree.SetName('Agreement')
    h_disagree.SetName('Disagreement')

    h_agree.SetStats(1)
    h_disagree.SetStats(1)
    # top
    h1 = sortHistograms([h_agree, h_disagree])
    # bot
    h2 = sortHistograms([h_agree.Clone(),h_disagree.Clone()])
    
    h1[0].GetXaxis().SetTitle('')
    h1[0].GetYaxis().SetTitle('Counts')
  
    #h1[0].GetYaxis().SetTitleOffset(0.5)
    #h1[0].GetYaxis().SetLabelSize(0.10)
    #h1[0].GetYaxis().SetTitleSize(0.10)

    #h1[0].GetXaxis().SetLabelSize(0.10)
  
    
    h1[0].Draw()
    for i in range(1,len(h1)):
      h1[i].Draw('sames')

    top.Update()
    setBoxes(top,h1)
    if doLogY:
      top.SetLogy()
      AutoFixAxes(top,False,False,9000)
    else:
      AutoFixAxes(top,False,False,2)

    bot.cd()
    if doLogY:  
      bot.SetLogy()

    hsum.Sumw2()
    for h in h2:
      h.SetStats(0)
      h.Sumw2()
      h.Divide(h,hsum,1.,1.)

    h2[0].GetYaxis().SetTitle('ratio')
    h2[0].GetXaxis().SetTitle(xlabel)
    h2[0].GetYaxis().SetTitleOffset(0.5)
    h2[0].GetYaxis().SetLabelSize(0.10)
    h2[0].GetYaxis().SetTitleSize(0.10)
    h2[0].GetXaxis().SetLabelSize(0.10)
    h2[0].GetXaxis().SetTitleSize(0.10)
    
    if not doLogY:
      h2[0].GetYaxis().SetRangeUser(0,1.05);
    
    h2[0].Draw('ep1')
    for i in range(1,len(h2)):
      h2[i].Draw('sames')
    
    if doLogY:
      AutoFixAxes(bot,False,False,1.1)
    

    # Loop over histograms
    canvas.SaveAs(plotname)
 

  
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







    #for pair in self._quadrantNames:
    #  for etBinIdx in range(len(self._etBins)-1):
    #    for etaBinIdx in range(len(self._etaBins)-1):
    #      
    #      binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
    #      for idx, hist in enumerate(hist_names):
    #        name = pair[0]+'_X_'+pair[1] 
    #        canvas = TCanvas('canvas','canvas',2500,1600)
    #        canvas.Divide(3,2)

    #        gStyle.SetPalette(107)
    #        gStyle.SetOptStat(110011)
    #        dirname = self._basepath+'/'+name+'/'+binningname
    #        h4 = self.storeSvc().histogram(dirname+'/passed_passed/'+hist)
    #        h3 = self.storeSvc().histogram(dirname+'/passed_rejected/'+hist)
    #        h2 = self.storeSvc().histogram(dirname+'/rejected_passed/'+hist)
    #        h1 = self.storeSvc().histogram(dirname+'/rejected_rejected/'+hist)
    #        h1.SetStats(0);h2.SetStats(0);h3.SetStats(0);h4.SetStats(0)
    #        h1.ProjectionX().Rebin(10);h2.ProjectionX().Rebin(10)
    #        h3.ProjectionX().Rebin(10);h4.ProjectionX().Rebin(10) 
    #        
    #        pad1=canvas.cd(1)
    #        pad1.SetRightMargin(0.13)
    #        h1.GetXaxis().SetAxisColor(kGray)
    #        h1.GetYaxis().SetAxisColor(kGray)
    #        h1.Draw('colz')

    #        pad2=canvas.cd(2)
    #        h2.GetXaxis().SetAxisColor(kGreen)
    #        h2.GetYaxis().SetAxisColor(kGreen)
    #        pad2.SetRightMargin(0.13)
    #        h2.Draw('colz')

    #        pad4=canvas.cd(4)
    #        h3.GetXaxis().SetAxisColor(kRed)
    #        h3.GetYaxis().SetAxisColor(kRed)
    #        pad4.SetRightMargin(0.13)
    #        h3.Draw('colz')
    #        
    #        pad5=canvas.cd(5)
    #        pad5.SetRightMargin(0.13)
    #        h4.Draw('colz')
    #        
    #        pad3=canvas.cd(3)
    #        hy1=h1.ProjectionY().Clone()
    #        hy2=h2.ProjectionY().Clone()
    #        hy3=h3.ProjectionY().Clone()
    #        hy4=h4.ProjectionY().Clone()

    #        hy1.SetStats(1);hy2.SetStats(1);hy3.SetStats(1);hy4.SetStats(1)
    #        #normalize(h1,h2,h3,h4)
    #        hy4.SetTitle( ('%s; %s; Counts')%(dirname.split('/')[-1].replace('_X_',' X '),hist_labels[idx]) )
    #        hy4.GetXaxis().SetTitleOffset(0.9)
    #        hy4.GetYaxis().SetTitleOffset(0.9)
    #        hy4.SetLineColor(kBlack)
    #        #hy4.SetFillColor(kBlack)
    #        hy3.SetLineWidth(1)
    #        hy3.SetLineColor(kRed)
    #        #hy3.SetFillColor(kRed)
    #        hy2.SetLineWidth(1)
    #        hy2.SetLineColor(kGreen)
    #        #hy2.SetFillColor(kGreen)
    #        hy1.SetLineWidth(1)
    #        hy1.SetLineColor(kGray+1)
    #        #hy1.SetFillColor(kGray+1)
    #        
    #        hsum = hy1.Clone()
    #        hsum+=hy2
    #        hsum+=hy3
    #        hsum+=hy4
    #        hy1.Divide(hsum)
    #        hy2.Divide(hsum)
    #        hy3.Divide(hsum)
    #        hy4.Divide(hsum)
    #        
    #        # Put all hists in order
    #        h = sortHistograms([hy1,hy2,hy3,hy4])
    #        h[0].Draw()
    #        for index in range(1,len(h)):
    #          h[index].Draw('sames')
 
    #        pad3.Update()
    #        from TrigEgammaDevelopments.plots import AutoFixAxes
    #        from TrigEgammaDevelopments.helper.util import setBoxes
    #        setBoxes(pad3,h)
    #        # atlas_template(pad3, atlaslabel=False)
    #        pad3.SetLogy()
    #        AutoFixAxes(pad3,False,False,100)

    #        # Loop over histograms
    #        canvas.SaveAs(localpath+'/'+prefix+'_'+name+'_'+hist+'_'+binningname+'.pdf')
    #        del canvas


