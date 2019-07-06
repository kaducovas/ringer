
__all__ = ["Efficiency", "EfficiencyParser", "profile"]

from RingerCore import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars, \
                       expandFolders, csvStr2List

from ROOT import kBlue, kBlack, kRed, kMagenta, kGreen 
from AtlasStyle import ATLASLabel, ATLASLumiLabel, SetAtlasStyle
from ROOT import kBlue, kBlack, kRed, kMagenta, kGreen 

class Profile(Logger):
  # default configurations
  _curve_color  = (kBlack, kBlue, kRed, kMagenta, kGreen)
  _marker_style = (22, 20, 21, 23,24,25)

  def __init__(self, logger = None):
    Logger.__init__(self, logger=logger)
    SetAtlasStyle()
    from ROOT import TFile, gROOT
    gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;");
    self._logger.info('create Profile instance..')

  def __call__(self, objList ,**kwargs):
    
    ylimits         = retrieve_kw( kwargs, 'ylimits'    , [(0.7, 1.1)]                 )
    legends         = retrieve_kw( kwargs, 'legends'    , None                         )
    hist_names      = retrieve_kw( kwargs, 'hist_names' , ['eff_et','eff_eta','eff_mu'])
    drawSame        = retrieve_kw( kwargs, 'drawSame'   , False                        )
    doEffLabel      = retrieve_kw( kwargs, 'doEffLabel' , True                         )


    if 'level' in kwargs: self.level = kw.pop('level')
    #checkForUnusedVars( kwargs, self._logger.warning )

    # protection for legends list parameter
    if not legends: 
      legends = []
      for o in objList:  legends.append(o['rawInfo']['algname'])
  
    llabel=objList[0]['rawInfo']['outputname'].split('/')[0]

    # fix y axis size
    # protection in axis
    if len(ylimits) == 1:  l = ylimits;  ylimits = [l for i in hist_names]
    # ready for plots...
    efficiencies_objects = self.__convert(objList)
    oname = kwargs.pop('oname')

    # TODO: make eff label for future
    eff=[]
    for index, e in enumerate(efficiencies_objects['eff']):
      passed=efficiencies_objects['passed'][index]
      total=efficiencies_objects['total'][index]
      s=('%s: %1.2f%% (%d/%d)')%(llabel,e,passed,total)
      eff.append(s)
    
    # Add efficiency label into the plot (only for ratio plots)
    if doEffLabel:
      kwargs['eff_label']=eff

    if drawSame:
      self.__plot_profiles_in_same_canvas( efficiencies_objects, hist_names, legends, ylimits, oname = oname, **kwargs)
      return [oname+'.pdf']
    else:
      figures=[]
      for i, eff in enumerate(hist_names):
        self.__plot_profiles( efficiencies_objects[eff], legends, ylimits[i], oname = oname+'_'+eff ,**kwargs)
        figures.append( oname+'_'+eff+'.pdf')
      return figures

  # Private method
  def __convert( self, objList ):
    obj = {'eff_et':list(),'eff_eta':list(),'eff_mu':list(),'eff_nvtx':list(),\
           'eff':list(),'passed':list(),'total':list()}
    for o in objList:
      obj['eff_et'].append( o['eff_et'] )
      obj['eff_eta'].append( o['eff_eta'] )
      obj['eff_mu'].append( o['eff_mu'] )
      obj['eff_nvtx'].append( o['eff_nvtx'] )
      obj['eff'].append(o['eff'])
      obj['passed'].append(o['passed'])
      obj['total'].append(o['total'])
    return obj

  def __plot_profiles_in_same_canvas( self, hist_objs, hist_names, legends, y_limits, **kwargs):

    legend_position = retrieve_kw( kwargs, 'legend_position', (0.36,0.20,0.66,0.36))
    legend_prefix   = retrieve_kw( kwargs, 'legend_prefix'  , 'Z#rightarrowee, '   )
    legend_header   = retrieve_kw( kwargs, 'legend_header'  , 'Trigger step'       )
    ylabel          = retrieve_kw( kwargs, 'ylabel'         , 'Trigger Efficiency' )
    title           = retrieve_kw( kwargs, 'title'          , 'Trigger Efficiency' )
    oname           = retrieve_kw( kwargs, 'oname'          , 'plot_efficiencys'   )
    column          = retrieve_kw( kwargs, 'column'         , 2                    )
    doRatio         = retrieve_kw( kwargs, 'doRatio'        , False                )
    canvas_size     = retrieve_kw( kwargs, 'canvas_size'    ,(1800,1500)           )
    # FIXME: This must be disable for now, there is some problem into the xaxis scale
    # The top and bot axis must be match! 
    tobject_collector=[]
    ratio_size_as_fraction=0.35
    
    
    from ROOT import TCanvas, TLegend, TProfile, TPad
    rows = int(round(len(hist_objs)/float(column)))
    canvas = TCanvas('canvas','canvas', canvas_size[0], canvas_size[1])
    canvas.Divide(rows,column)
    leg_holder = []
    for index, hist_str in enumerate(hist_names):
      hists = hist_objs[hist_str]
      pad = canvas.cd(index+1)
      # Force disable if != of 2
      if len(hists) != 2:
        doRatio=False

      if doRatio:
        drawopt='pE1'
        pad.cd()
        top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
        top.SetBottomMargin(0.0)
        top.SetBottomMargin(0.06/float(top.GetHNDC()))
        #top.SetTopMargin   (0.04/float(top.GetHNDC()))
        top.SetRightMargin (0.05 )
        top.SetLeftMargin  (0.16 )
        top.SetFillColor(0)
        top.Draw(drawopt)
        tobject_collector.append(top)
        pad.cd()
        bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
        bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
        #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
        bot.SetTopMargin   (0.0)
        bot.SetRightMargin (0.05)
        bot.SetLeftMargin  (0.16)
        bot.SetFillColor(0)
        bot.Draw(drawopt)
        tobject_collector.append(bot)

      if type(legend_prefix) is not list:
        legend_prefix = [legend_prefix]*len(legends)
    
      if doRatio:
        top.cd()

      leg    = TLegend(legend_position[0],legend_position[1],
                       legend_position[2],legend_position[3])

      from AtlasStyle import setLegend1, atlas_template
      setLegend1(leg)
      leg.SetHeader(legend_header)
 
      for i, eff in enumerate(hists):
        eff.SetLineColor( self._curve_color[i] )
        eff.SetMarkerColor( self._curve_color[i] )
        eff.SetMarkerStyle( self._marker_style[i])
        if type(eff) is TProfile:  eff.SetStats(0)
        leg.AddEntry(eff, legend_prefix[i]+legends[i],'p')
        if i is 0:   eff.Draw()
        else: eff.Draw('same')
  
      leg.SetTextSize(0.03)
      leg.SetBorderSize(0)
      leg.Draw()
      
      if doRatio:
        top.Modified()
        top.Update

      pad.Modified()
      pad.Update()

      from ROOT import TProfile,TEfficiency,kFALSE
      xmin=0; xmax=999

      if type(hists[0]) is TProfile:
        hists[0].GetYaxis().SetRangeUser(y_limits[index][0],y_limits[index][1]);
      elif type(hists[0]) is TEfficiency:
        hists[0].GetPaintedGraph().GetYaxis().SetRangeUser(y_limits[index][0],y_limits[index][1]);
        hists[0].GetPaintedGraph().GetYaxis().SetTitle('A');
        
        # Fix the X axis
        nbins = hists[0].GetTotalHistogram().GetNbinsX()
        xmin = hists[0].GetTotalHistogram().GetXaxis().GetBinLowEdge(1)
        xmax = hists[0].GetTotalHistogram().GetXaxis().GetBinLowEdge(nbins+1)
        hists[0].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax);
      else:
        hists[0].GetYaxis().SetRangeUser(y_limits[index][0],y_limits[index][1]);


      pad.Modified()
      pad.Update()
      tobject_collector.append(leg)
      
      if doRatio:
        atlas_template(top, **kwargs)
        top.Update()
        from ROOT import TH1
        divide=""
        drawopt='pE1'
        bot.cd()
        ref= hists[0].GetPassedHistogram().Clone()
        h  = hists[1].GetPassedHistogram().Clone()
        #ref = hists[0].Clone()
        #h = hists[1].Clone()
        ref.Sumw2()
        h.Sumw2()
        ref.Divide(hists[0].GetTotalHistogram().Clone())
        h.Divide(hists[1].GetTotalHistogram().Clone())
        #ratioplot = TEfficiency(h,ref)
        ratioplot = h.Clone()
        ratioplot.Sumw2()
        ratioplot.SetName(h.GetName()+'_ratio')
        ratioplot.Divide(h,ref,1.,1.,'')
        #ratioplot.Divide(ref)
        ratioplot.SetFillColor(0)
        ratioplot.SetFillStyle(0)
        ratioplot.SetMarkerColor(1)
        ratioplot.SetLineColor(kBlack)
        ratioplot.SetMarkerStyle(24)
        ratioplot.SetMarkerSize(1.2)
        ratioplot.GetYaxis().SetTitle('trigger / ref')
        ratioplot.GetYaxis().SetTitleSize(0.10)
        ratioplot.GetXaxis().SetTitleSize(0.10)
        ratioplot.GetXaxis().SetLabelSize(0.10)
        ratioplot.GetYaxis().SetLabelSize(0.10)
        ratioplot.GetYaxis().SetRangeUser(0.9,1.07)
        ratioplot.Draw(drawopt)
        tobject_collector.append(ratioplot)
        #atlas_template(bot, **kwargs)
        from ROOT import TLine
        l1 = TLine(xmin,1,xmax,1)
        l1.SetLineColor(kRed)
        l1.SetLineStyle(2)
        l1.Draw()
        tobject_collector.append(l1) 
        bot.Update()
      else:
        atlas_template(pad, **kwargs)
      pad.Update()

    canvas.SaveAs(oname+'.pdf')



  def __plot_profiles( self, hists, legends, y_limits, **kwargs):

    legend_position = retrieve_kw( kwargs, 'legend_position', (0.36,0.20,0.66,0.30))
    legend_prefix   = retrieve_kw( kwargs, 'legend_prefix'  , 'Z#rightarrowee, '   )
    legend_header   = retrieve_kw( kwargs, 'legend_header'  , 'Trigger step'       )
    ylabel          = retrieve_kw( kwargs, 'ylabel'         , 'Trigger Efficiency' )
    title           = retrieve_kw( kwargs, 'title'          , 'Trigger Efficiency' )
    oname           = retrieve_kw( kwargs, 'oname'          , 'plot_efficiencys'   )
    doRatio         = retrieve_kw( kwargs, 'doRatio'        , False                )
    canvas_size     = retrieve_kw( kwargs, 'canvas_size'    ,(800,600)             )
    eff_label       = retrieve_kw( kwargs, 'eff_label'      , None                 )

    # FIXME: This must be disable for now, there is some problem into the xaxis scale
    # The top and bot axis must be match! 
    tobject_collector=[]
    ratio_size_as_fraction=0.35
   
    yc = canvas_size[1]*1.3 if doRatio else canvas_size[1]
    
    from ROOT import TCanvas, TPad, TLegend, TProfile,gStyle
   

    if type(legend_prefix) is not list:
      legend_prefix = [legend_prefix]*len(legends)
  
    canvas = TCanvas('canvas','canvas', canvas_size[0], int(yc))
    leg    = TLegend(legend_position[0],legend_position[1],
                     legend_position[2],legend_position[3])

    from AtlasStyle import setLegend1, atlas_template
    setLegend1(leg)
    leg.SetHeader(legend_header)
    canvas.Update()
    canvas.cd()

    if len(hists) != 2:
      doRatio=False

    if doRatio:
      drawopt='pE1'
      top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
      top.SetBottomMargin(0.0)
      top.SetBottomMargin(0.06/float(top.GetHNDC()))
      #top.SetTopMargin   (0.04/float(top.GetHNDC()))
      top.SetRightMargin (0.05 )
      top.SetLeftMargin  (0.16 )
      top.SetFillColor(0)
      top.Draw(drawopt)
      tobject_collector.append(top)
      canvas.cd()
      bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
      bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
      #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
      bot.SetTopMargin   (0.0)
      bot.SetRightMargin (0.05)
      bot.SetLeftMargin  (0.16)
      bot.SetFillColor(0)
      bot.Draw(drawopt)
      tobject_collector.append(bot)
      top.cd()

    for i, eff in enumerate(hists):
      eff.SetLineColor( self._curve_color[i] )
      eff.SetMarkerColor( self._curve_color[i] )
      eff.SetMarkerStyle( self._marker_style[i])
      if type(eff) is TProfile:  eff.SetStats(0)
      leg.AddEntry(eff, legend_prefix[i]+legends[i],'p')
      if i is 0:   eff.Draw()
      else: eff.Draw('same')
  
    leg.SetTextSize(0.03)
    leg.SetBorderSize(0)
    leg.Draw()
    
    if doRatio:
      top.Modified()
      top.Update

    canvas.Modified()
    canvas.Update()

    from ROOT import TProfile, TEfficiency
    xmin=0; xmax=999

    if type(hists[0]) is TProfile:
      hists[0].GetYaxis().SetRangeUser(y_limits[0],y_limits[1]);
    elif type(hists[0]) is TEfficiency:
      hists[0].GetPaintedGraph().GetYaxis().SetRangeUser(y_limits[0],y_limits[1]);
      hists[0].GetPaintedGraph().GetYaxis().SetTitle('A');
      
      # Fix the X axis
      nbins = hists[0].GetTotalHistogram().GetNbinsX()
      xmin = hists[0].GetTotalHistogram().GetXaxis().GetBinLowEdge(1)
      xmax = hists[0].GetTotalHistogram().GetXaxis().GetBinLowEdge(nbins+1)
      hists[0].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax);
    else:
      hists[0].GetYaxis().SetRangeUser(y_limits[0],y_limits[1]);


    

    if doRatio:
      if eff_label:
        from ROOT import TLatex
        latex_eff = TLatex()
        latex_eff.SetTextSize(0.025);
        latex_eff.DrawLatexNDC(0.55,0.85, '#scale[2]{'+eff_label[0]+'}')
        latex_eff.DrawLatexNDC(0.55,0.78, '#scale[2]{#color[4]{'+eff_label[1]+'}}')
      top.Modified()
      top.Update

      atlas_template(top, **kwargs)
      top.Update()
      #top.SetGrid()
      #gStyle.SetGridStyle(3)
      from ROOT import TH1
      divide=""
      drawopt='pE1'
      bot.cd()
      ref= hists[0].GetPassedHistogram().Clone()
      h  = hists[1].GetPassedHistogram().Clone()
      #ref = hists[0].Clone()
      #h = hists[1].Clone()
      ref.Sumw2()
      h.Sumw2()
      ref.Divide(hists[0].GetTotalHistogram().Clone())
      h.Divide(hists[1].GetTotalHistogram().Clone())
      #ratioplot = TEfficiency(h,ref)
      ratioplot = h.Clone()
      ratioplot.Sumw2()
      ratioplot.SetName(h.GetName()+'_ratio')
      ratioplot.Divide(h,ref,1.,1.,'')
      #ratioplot.Divide(ref)
      ratioplot.SetFillColor(0)
      ratioplot.SetFillStyle(0)
      ratioplot.SetMarkerColor(1)
      ratioplot.SetLineColor(kBlack)
      ratioplot.SetMarkerStyle(24)
      ratioplot.SetMarkerSize(1.2)
      ratioplot.GetYaxis().SetTitle('trigger / ref')
      ratioplot.GetYaxis().SetTitleSize(0.10)
      ratioplot.GetXaxis().SetTitleSize(0.10)
      ratioplot.GetXaxis().SetLabelSize(0.10)
      ratioplot.GetYaxis().SetLabelSize(0.10)
      ratioplot.GetYaxis().SetRangeUser(0.9,1.07)
      ratioplot.Draw(drawopt)
      tobject_collector.append(ratioplot)
      #atlas_template(bot, **kwargs)
      from ROOT import TLine
      l1 = TLine(xmin,1,xmax,1)
      l1.SetLineColor(kRed)
      l1.SetLineStyle(2)
      l1.Draw()
      tobject_collector.append(l1) 
      bot.Update()
    else:
      atlas_template(canvas, **kwargs)
    
    canvas.Update()
    canvas.SaveAs(oname+'.pdf')


profile = Profile()


####################################################################################


class Efficiency(Logger):

  # default configurations
  _curve_color  = (kBlue, kBlack, kRed, kMagenta)
  _marker_style = (22, 20, 21, 23)

  def __init__(self, logger = None):
    Logger.__init__(self, logger=logger)
    from ROOT import  gROOT
    gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;");
    # reading root file

  def __call__(self, store, algname, **kwargs):
    
    basepath        = retrieve_kw( kwargs, 'basepath'   , 'HLT/Egamma/Expert' )
    dirname         = retrieve_kw( kwargs, 'dirname'    , 'Efficiency'        )
    input_name      = retrieve_kw( kwargs, 'inputname'  , 'HLT/'              )
    output_name     = retrieve_kw( kwargs, 'outputname' , 'HLT/match_'        )

    if 'level' in kwargs: self.level = kw.pop('level')
    checkForUnusedVars( kwargs, self._logger.warning )
    input_name = input_name.replace('//','/')
    output_name = output_name.replace('//','/')

    # some info to hold
    rawInfo = {'inputname': input_name,\
               'outputname' : output_name,\
               'basepath': basepath,\
               'dirname':dirname,\
               'algname':algname}

    # This can be:
    # Egamma/algname/Efficiency/L1Calo/match_eta
    path = (basepath+'/'+algname+'/'+dirname).replace('//','/')

    try:# protection
      self._logger.debug('Extracting efficiencies information for %s from %s',algname,path)
      obj, eff, passed, total = self.__retrieve_efficiencies(store, path,\
                                input_name, output_name)
    except RuntimeError:
      self._logger.error(('Can not extract the efficiencies for this path %s')%(path))
      raise RuntimeError('loop error in retrieve_efficiencies private method')

    # hold efficiencies values
    eobj = {'eff_et':obj['eff_et'], 'eff_eta':obj['eff_eta'], 'eff_mu':obj['eff_mu'],'eff_nvtx':obj['eff_nvtx'], \
        'eff':eff, 'passed':passed, 'total':total, 'rawInfo':rawInfo}
    self._logger.debug(('%s with efficiency: %1.2f  (%d/%d)')%\
                      (algname, eff, passed, total))
    return eobj


  def __retrieve_efficiencies( self, store, path, inname, outname ):

    rawobj = dict()
    inname = (path+'/'+inname).replace('//','/')
    outname = (path+'/'+outname).replace('//','/')

    rawobj['et']        = store.histogram( inname+'et'    ) 
    rawobj['eta']       = store.histogram( inname+'eta'   ) 
    rawobj['mu']        = store.histogram( inname+'mu'   ) 
    rawobj['nvtx']      = store.histogram( inname+'nvtx'  ) 
    rawobj['match_et']  = store.histogram( outname+'et'   ) 
    rawobj['match_eta'] = store.histogram( outname+'eta'  ) 
    rawobj['match_mu']  = store.histogram( outname+'mu'   ) 
    rawobj['match_nvtx']= store.histogram( outname+'nvtx' ) 
   
    from ROOT import TProfile,TEfficiency,TH1F
    if not rawobj['nvtx']:
      rawobj['nvtx']=TH1F()
    if not rawobj['match_nvtx']:
      rawobj['match_nvtx']=TH1F()

    passed_eta = rawobj['match_eta'].GetEntries()
    passed_eta = rawobj['match_et'].GetEntries()
    total_eta  = rawobj['eta'].GetEntries()
    total_eta  = rawobj['et'].GetEntries()
    if total_eta != 0:
      eff_eta    = passed_eta/float(total_eta) * 100
    else:
      eff_eta = 0 
    
    # create output dictionary
    obj=dict()
    obj['eff_et' ]   = TEfficiency(rawobj['match_et'] ,rawobj['et'] )
    obj['eff_eta']   = TEfficiency(rawobj['match_eta'],rawobj['eta'])
    obj['eff_mu' ]   = TEfficiency(rawobj['match_mu'] ,rawobj['mu'] )
    obj['eff_nvtx' ] = TEfficiency(rawobj['match_nvtx'] ,rawobj['nvtx'] )
    obj['eff_et' ].SetTitle('#epsilon(E_{T}); E_{T}[GeV] ; #epsilon(E_{T})')
    obj['eff_eta'].SetTitle('#epsilon(#eta); #eta ; #epsilon(#eta)')
    obj['eff_mu' ].SetTitle('#epsilon(#mu); #mu ; #epsilon(#mu)')
    obj['eff_nvtx' ].SetTitle('#epsilon(N_{vtx}); N_{vtx} ; #epsilon(N_{vtx})')
 
    return obj, eff_eta, passed_eta, total_eta
  
  
  def gen_table(self, store, algname, subdirs, **kwargs):

    basepath        = retrieve_kw( kwargs, 'basepath'   , 'HLT/Egamma/Expert' )
    dirname         = retrieve_kw( kwargs, 'dirname'    , 'Efficiency'        )
    
    path = basepath+'/'+algname+'/'+dirname
    self._logger.info('{:-^79}'.format((' %s ')%(algname)))
    for dir in subdirs:
      obj, eff, passed, total = self.__retrieve_efficiencies(store ,path,dir+'/', dir+'/match_')
      eff=('%1.2f')%(eff); passed=('%d')%(passed); total=('%d')%(total)
      stroutput = '| {0:<40} |{1:<10}| {2:<5} ({3:<5}, {4:<5}) |'.format(algname,dir,eff,passed,total)

      self._logger.info( stroutput )
    self._logger.info('{:-^79}'.format(''))

####################################################################################

class EfficiencyParser( Logger ):

  _dict_config = {
      'EMU':'Emulation',
      'EFF':'Efficiency',
      }
  _store         = list()
  _resume        = list()

  def __init__(self, fileList, logger=None):

    Logger.__init__(self, logger=logger)
    from RingerCore import StoreGate
    for f in fileList:
      self._store.append( StoreGate(f,restoreStoreGate=True) )
      paths=self._store[-1].getDirs()
     
      #TODO: this shold be a property
      # Only for egamma trigger staff 
      def check_egamma_paths(p):
        paths=[]
        for s in p:
          if 'Egamma' in s:
            if not 'icalomedium' in s:
              paths.append(s)
        return paths
      # filter egamma only
      paths=check_egamma_paths(paths)
      
      resume1 = self.resume(paths, 'Efficiency')
      try:
        resume2 = self.resume(paths, 'Emulation')
      except:
        resume2 = None
        self._logger.warning('There is no emulation dirname in this file.')
      # hold the resume paths
      self._resume.append( {'Efficiency':resume1, 'Emulation':resume2} )
    # display all chains
    self._effReader = Efficiency()


  def getResume(self):
    return self._resume


  def translate(self, configList ):
    cList = list()
    for arg in configList:
      arg_split = arg.split(':')
      config = dict()
      config['dirname']  = self._dict_config[arg_split[0]]
      config['file']     = int(arg_split[1]) 
      config['basepath'] = self._resume[config['file']][config['dirname']][int(arg_split[2])][0]
      config['algname']  = self._resume[config['file']][config['dirname']][int(arg_split[2])][1]
      config['subdirs']  = self._resume[config['file']][config['dirname']][int(arg_split[2])][2]
      try:
        config['legend'] = arg_split[3]+': '+config['algname'].replace('HLT_','')
      except:
        config['legend'] = config['algname'].replace('HLT_','')
      cList.append( config )
    return cList

  # print all algorithms and base paths found into the current file
  def display(self):
    self._logger.info('Display all information found...')
    for storeIdx, resume in enumerate(self._resume):
      self._logger.info('{:-^79}'.format((' File: %d ')%(storeIdx)))
      for idx,r in enumerate(resume['Efficiency']):
        self._logger.info(('[%1.2d] Efficiency: %s')%(idx,r[0]+'/'+r[1]) )
      if resume['Emulation']:
        self._logger.info('{:-^79}'.format(''))
        for idx,r in enumerate(resume['Efficiency']):
          self._logger.info(('[%1.2d] Emulation: %s')%(idx,r[0]+'/'+r[1]) )
      self._logger.info('{:-^79}'.format(''))


  def resume(self, paths, dirname):
    pathHolder = {}
    for path in paths:
      if dirname in path:
        p = path.split('/'+dirname+'/')[0]
        algname = p.split('/')[-1]
        basepath = p.replace('/'+algname,'')
        tmp = basepath+'+'+algname
        p = path.split('/'+dirname+'/')[1].split('/')
        if not tmp in pathHolder.keys():
          pathHolder[tmp] = []
        if len(p)>1:
          pathHolder[tmp].append(p[0])
          pathHolder[tmp] = list(set(pathHolder[tmp]))
    resume = []
    for key in pathHolder.keys():
      tkey = key.split('+')
      basepath = tkey[0]; algname = tkey[1]
      if len(pathHolder[key]) is 0:  pathHolder[key]=['']
      resume.append( (basepath, algname, pathHolder[key]) )
    return sorted(resume)


  def __call__(self, **kwargs):
    key             = retrieve_kw( kwargs, 'key'        , None                )
    outputdir       = retrieve_kw( kwargs, 'outputdir'  , 'plots'             )
    drawSame        = retrieve_kw( kwargs, 'drawsame'   , True                )
    atlaslabel      = retrieve_kw( kwargs, 'atlaslabel' , 'Internal'          )
    isBackground    = retrieve_kw( kwargs, 'isbackground', False              )
    doRatio         = retrieve_kw( kwargs, 'doRatio', False                   )
    doEffLabel      = retrieve_kw( kwargs, 'doEffLabel', True                 )
    checkForUnusedVars( kwargs, self._logger.warning )
   
    import os
    localpath = os.getcwd()+'/'+outputdir
    try:
      os.mkdir(localpath)
    except:
      self._logger.warning('The director %s exist.', localpath)
 
    import base64
    if key:
      if not ':' in key:
        key = base64.b64decode(key)
        self._logger.info('Translate key to: %s', key)
      key = key.split(',')
      cList = self.translate(key)
    else:
      self.display()
      key = input('Write the configuration: ')
      self._logger.info('Use this key %s if you want to reproduce this plot',base64.b64encode(key))
      key = key.split(',')
      cList = self.translate(key)

    # FIXME: The subdirs must be the same for all configuration
    subdirs = cList[0]['subdirs']

    figures=[]

    for subdir in subdirs:
      eff_list = list(); legends = list(); algnames = None
      for index, c in enumerate(cList):        
        effObj = self._effReader( self._store[c['file']], c['algname'], 
                                  basepath = c['basepath'],
                                  dirname  = c['dirname'],
                                  inputname = subdir+'/',
                                  outputname = subdir+'/match_'
                                  )
        eff_list.append(effObj)
        legends.append(c['legend'])
        if not algnames:
          algnames=c['algname']
        else:
          algnames+='_'+c['algname']

      
      f = profile( eff_list,
           ylimits          = [ (0.0, 1.4) , (0.0, 1.2), (0.0, 1.4), (0.0, 1.4) ] \
               if not isBackground else [(-0.3,0.1),(-0.3,0.4),(-0.3,0.4),(-0.3, 0.4)],
           ylabel           = 'Trigger Efficiency',
           hist_names       = ['eff_et','eff_eta','eff_mu'],
           legend_header    = '',
           legend_prefix    = '',
           legends          = legends,
           region_label     = '',
           oname            = localpath+'/'+subdir+'_'+ algnames,
           drawSame         = drawSame,
           doRatio          = doRatio,
           atlaslabel       = atlaslabel,
         )

      figures.extend(f)

      f = profile( eff_list,
           ylimits          = [ (0.0, 1.4) , (0.0, 1.4), (0.0, 1.4), (0.0, 1.4) ] \
               if not isBackground else [(-0.3,0.1),(-0.3,0.4),(-0.3,0.4),(-0.3, 0.4)],
           ylabel           = 'Trigger Efficiency',
           hist_names       = ['eff_et','eff_eta','eff_mu'],
           legend_header    = '',
           legend_prefix    = '',
           legends          = legends,
           region_label     = '',
           oname            = localpath+'/'+subdir+'_'+ algnames,
           drawSame         = False,
           doRatio          = True,
           doEffLabel       = doEffLabel,
           atlaslabel       = atlaslabel,
         )

      figures.extend(f)

    for c in cList:
      self._effReader.gen_table(self._store[c['file']], c['algname'], c['subdirs'], basepath = c['basepath'], dirname = c['dirname'])
    
    return figures


