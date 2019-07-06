
import time,os,math,sys,pprint,glob
import ROOT
from array import array
import warnings


def retrieveTH1( rfile, location ):
  from ROOT import TH1F
  obj = TH1F('','',1,0,1)
  try:
    rfile.GetObject(location,obj)
    return obj
  except:
    raise RuntimeError("Can not retrieve the TH1 object %s from root file",location)


def retrieveTH2( rfile, location ):
  from ROOT import TH2F
  obj = TH2F('','',1,0,1,1,0,1)
  rfile.GetObject(location,obj)
  try:
    rfile.GetObject(location,obj)
    return obj
  except:
    raise RuntimeError("Can not retrieve the TH2 object %s from root file",location)


def retrieveProfile( rfile, location ):
  from ROOT import TProfile
  obj = TProfile('','',1,0,1)
  try:
    rfile.GetObject(location,obj)
    return obj
  except:
    raise RuntimeError("Can not retrieve the TProfile object %s from root file",location)


def setBoxes(pad, hists):
  #pad.Update();
  x_begin = 1.
  x_size = .18
  x_dist = .03;
  histStatsList=[]
  from ROOT import TPaveStats
  for hist in hists:
    histStats = hist.GetListOfFunctions().FindObject("stats")
    histStats.__class__=TPaveStats
    histStats.SetX1NDC(x_begin-x_dist); histStats.SetX2NDC(x_begin-x_size-x_dist);
    histStats.SetTextColor(hist.GetLineColor())
    histStatsList.append(histStats)
    x_begin-=x_dist+x_size;
  return histStatsList
 



def get_equilibrium_line(hist,effref,a_1,limits) :
  """
  Takes a 2d hist (hist), the target efficiency (effref), the starting discr value (a_1),
  and the three numbers corresponding to the boundary lines in nvtx (i.e. [0,12,23] for
  nvtx = 0-11 and 12-22).
  """

  err_on_higher_eff = True
  dslope = hist.GetXaxis().GetBinWidth(1)/15. # *10
  #binwidth = 10*hist.GetXaxis().GetBinWidth(1)
  binwidth = 5*hist.GetXaxis().GetBinWidth(1)
  if hist.Integral() != 0:
    error = math.sqrt(effref*(1-effref)/hist.Integral())
  else:
    error = 1
  if error == 0 :
    error = 1.
  
  nIters = 0; a = a_1; b = 0; tmp = 0
  islo,ishi,isgt,islt,reset = False,False,False,False,False
  flipcounter = 0
  while (True) :
    if a < hist.GetXaxis().GetBinLowEdge(1) :
      #print('GetEquilibriumLine: discriminant is at low egdge of histo. Breaking.')
      a = a_1
      b = 0
      break
    if a > hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()+1) :
      #print('GetEquilibriumLine: discriminant is at high egdge of histo. Breaking.')
      a = a_1
      b = 0
      break
    if flipcounter == 10 :
      #print('GetEquilibriumLine: flipcounter maxed out. breaking.')
      break
    if islo and ishi :
      #print('GetEquilibriumLine: oscillating...')
      binwidth = binwidth*0.5
      flipcounter += 1
    if isgt and islt :
      #print('GetEquilibriumLine: slope oscillating...')
      dslope = 0.5*dslope
      flipcounter += 1
    reset = not reset
    if reset :
        islo,ishi,isgt,islt = False,False,False,False
    tmp+=1
    lower = get_efficiency_region(hist,limits[0],limits[1],a,b,err_on_higher_eff)
    upper = get_efficiency_region(hist,limits[1],limits[2],a,b,err_on_higher_eff)
    #print('GetEquilibriumLine: a %f b %f lower %f upper %f effref %f'%(a,b,lower,upper,effref))
    if (lower - effref > error) and (upper - effref > error) :
      #print('GetEquilibriumLine: both effs are larger')
      islo = True
      a += binwidth
    elif (lower - effref < error) and (upper - effref < error) :
      #print('GetEquilibriumLine: both effs are smaller')
      ishi = True
      a -= binwidth
    elif lower - upper < error :
      #print('GetEquilibriumLine: both effs are within error %f'%error)
      break
    elif lower > upper :
      isgt = True
      #print('GetEquilibriumLine: Lower eff >>>>> Upper eff')
      a = a - limits[1]*dslope
      b -= dslope
    elif upper > lower :
      islt = True
      #print('GetEquilibriumLine: Lower eff <<<<< Upper eff')
      a = a + limits[1]*dslope
      b += dslope

      

  lower = get_efficiency_region(hist,limits[0],limits[1],a,b,err_on_higher_eff)
  upper = get_efficiency_region(hist,limits[1],limits[2],a,b,err_on_higher_eff)
  if lower - upper > error :
    #print('GetEquilibriumLine Error! Results are not within error %f (%f,%f)'%(error,lower,upper))
    #print('GetEquilibriumLine a %f b %f'%(a,b))
    #print('GetEquilibriumLine end')
    pass
  #print "theSlope (GetEquilLine): %3.15f" % b    
  return a,b



def get_efficiency_region(hist,ylow,yhigh,a,b,err_on_higher_eff=False) : # yhigh is non-inclusive
  
  """
  Get the efficiency of a range of nvtx (ylow to yhigh) given discriminant parameters a and b
  (i.e. discr = a + bx where x is nvtx)
  """
  # inputs are nvtx (or TRT Track Occ)limits (i.e. ylow <= region < yhigh)
  yhigh = hist.GetYaxis().FindBin(yhigh) - 1
  ylow = hist.GetYaxis().FindBin(ylow) - 1
  yhigh = min(hist.GetNbinsY(),yhigh)
  den = float(hist.Integral(-99999,99999,int(ylow)+1,int(yhigh)))
  num = 0
  #for by in xrange(ylow,yhigh) :
  for by in xrange(int(ylow),int(yhigh)) :
    #print by, a, b
    discr = a + b*by
    dbin = hist.GetXaxis().FindBin(discr)
    num += hist.Integral(dbin+(0 if err_on_higher_eff else 1),99999,by+1,by+1)
  if den == 0 :
    return 1
  return num/den

def get_parameterized_discrNumerator_profile(hist,a,b) :
  
  """  
  Given a 2d hist, return the numerator of the efficiency vs nvtx (a 1d hist).
  """
  err_on_higher_eff = False
  nbinsy = hist.GetNbinsY()
  h1 = hist.ProjectionY(hist.GetName()+'_proj'+str(time.time()),1,1)
  h1.Reset("ICESM")
  Numerator=0
  for by in xrange(nbinsy) :
    xproj = hist.ProjectionX('xproj'+str(time.time()),by+1,by+1)
    discr = a + b*by

    dbin = xproj.FindBin(discr)
    num = xproj.Integral(dbin+(0 if err_on_higher_eff else 1),xproj.GetNbinsX()+1)
    h1.SetBinContent(by+1,num)
    Numerator+=num
  return h1, Numerator


def calculate_dependent_discr_points( hist2D , effref):
  nbinsy = hist2D.GetNbinsY()
  binwidth = hist2D.GetYaxis().GetBinWidth(1)
  x = list(); y = list(); errors = list()
  for by in xrange(nbinsy):
    xproj = hist2D.ProjectionX('xproj'+str(time.time()),by,by+1)
    discr, error = find_threshold(xproj,effref)
    dbin = xproj.FindBin(discr)
    x.append(discr); y.append(by*binwidth)
    errors.append( error )
  return x,y,errors


def find_threshold(hist,effref):
  nbins = hist.GetNbinsX()
  fullArea = hist.Integral(0,nbins+1)
  if fullArea == 0:
    return 0,1
  setEfficiency = effref
  eff = 100.0; i = 0
  while eff >= setEfficiency:
    cutArea = hist.Integral(i,nbins+1)
    i+=1
    eff = cutArea/fullArea
  threshold = hist.GetBinCenter(i)
  #error = math.sqrt(abs(threshold)*(1-abs(threshold))/fullArea)
  error = eff/math.sqrt(fullArea)
  return threshold, error


def get_passed( hist, threshold ):
  nbins = hist.GetNbinsX()
  fullArea = hist.Integral(0,nbins+1)
  cutBin = hist.FindBin( threshold )
  cutArea = hist.Integral(cutBin,nbins+1)
  return cutArea, fullArea, cutArea/fullArea
  



def find_threshold_best_sp(sgn_hist, noise_hist):

  from RingerCore import calcSP
  nbins = sgn_hist.GetNbinsX()
  det_total   = sgn_hist.Integral(0,nbins+1)
  noise_total =  noise_hist.Integral(0,nbins+1)

  sp_max = -999
  best_threshold = -999
  best_det = -999
  best_fa  = -999
  i = 0
  while i < nbins+1:
    # Detection
    det_passed = sgn_hist.Integral(i,nbins+1)
    # False alarm
    noise_passed = noise_hist.Integral(i,nbins+1)

    det = det_passed/det_total
    fa  = noise_passed/noise_total
    sp  = calcSP(det,1-fa)
    if sp > sp_max:
      sp_max   = sp
      best_det = det
      best_fa  = fa
      threshold = sgn_hist.GetBinCenter(i)
    i+=1

  return sp_max, best_det, best_fa, threshold
  


def calculate_efficiency(h2D, effref, b, a, **kwargs):

  from copy import deepcopy
  hist2D=deepcopy(h2D)
  fix_fraction = kwargs.pop('fix_fraction', 1)
  doCorrection = kwargs.pop('doCorrection', True)
  limits       = kwargs.pop('limits', [])

  if doCorrection:
    # Get the intercept and slope in disc vs. pileup plane: y = ax+b
    b,a = get_equilibrium_line(hist2D,effref,b,limits)
    # Now do some correction to give the efficiency a small slope 
    # (so backgrounds do not explode)
    pivotPoint = limits[1]
    b = b + pivotPoint*a*(1-fix_fraction)
    a = a*fix_fraction
  
  # Put into histograms
  histNum, passed = get_parameterized_discrNumerator_profile(hist2D,b,a)
  histDen = hist2D.ProjectionY()
  histEff = histNum.Clone()
  histEff.Divide(histDen)
  for bin in xrange(histEff.GetNbinsX()):
    if histDen.GetBinContent(bin+1) != 0 :
      Eff = histEff.GetBinContent(bin+1)
      try:
        dEff = math.sqrt(Eff*(1-Eff)/histDen.GetBinContent(bin+1))
      except:
        dEff=0
      histEff.SetBinError(bin+1,dEff)
    else:
      histEff.SetBinError(bin+1,0)
  
  eff=passed/float(histDen.GetEntries())
  if doCorrection:
    return histNum, histDen, histEff, eff, b, a
  else:
    return histNum, histDen, histEff,eff


def copy2DRegion(hist, xbins, xmin, xmax, ybins, ymin, ymax):
  from ROOT import TH2F
  h = TH2F(hist.GetName()+'_region',hist.GetTitle(),xbins,xmin,xmax,ybins,ymin,ymax)
  yhigh = hist.GetYaxis().FindBin(ymax) - 1
  ylow = hist.GetYaxis().FindBin(ymin) - 1
  yhigh = min(hist.GetNbinsY(),yhigh)

  xhigh = hist.GetXaxis().FindBin(xmax) - 1
  xlow = hist.GetXaxis().FindBin(xmin) - 1
  xhigh = min(hist.GetNbinsX(),xhigh)

  x=0; y=0
  for bx in xrange(int(xlow),int(xhigh)+1) :
    x+=1
    for by in xrange(int(ylow),int(yhigh)+1) :
      y+=1
      value = hist.GetBinContent(bx+1,by+1)
      h.SetBinContent(x-1,y-1,value)
    y=0
  return h


def get_line(x1,y1,x2,y2,color,style,width, text=''):
  from ROOT import TLine
  l = TLine(x1,y1,x2,y2)
  l.SetNDC(False)
  l.SetLineColor(color)
  l.SetLineWidth(width)
  l.SetLineStyle(style)
  return l


def GetBotPad(can) :
    return can.GetPrimitive('pad_bot')

def GetTopPad(can) :
    return can.GetPrimitive('pad_top')



def AddBinLines(can,hist,useHistMax=False,horizotalLine=1.,lineStyle=2):
   tobject_collector = []
   from ROOT import TH1,TGraph,THStack,TColor, kGray, kBlue, TLine, kRed
   if can.GetPrimitive('pad_top'):
       tobject_collector.extend(AddBinLines(can.GetPrimitive('pad_top'), hist, useHistMax, horizotalLine))
       if can.GetPrimitive('pad_bot'):
           # TODO Move this to another function
           pad = GetBotPad(can)
           tobject_collector.extend(AddBinLines(pad, hist))
           if horizotalLine is not None and pad.GetUymax() > horizotalLine > pad.GetUymin():
               pad.cd()
               maxValue = pad.GetUxmax()
               minValue = pad.GetUxmin()
               l = TLine( minValue, horizotalLine, maxValue, horizotalLine )
               l.SetLineColor(kRed)
               l.SetLineStyle(2)
               l.Draw()
               tobject_collector.append(l)
       return tobject_collector
   can.cd()
   #listOfPlottedObjects = [o for o in can.GetListOfPrimitives() if isinstance(o,(TH1, THStack))]
   #listOfPlottedObjects += [o.GetHistogram() for o in can.GetListOfPrimitives() if isinstance(o,TGraph)]
   #if listOfPlottedObjects:
       #maxValue = max([o.GetBinContent(o.GetMaximumBin()) + o.GetBinError(o.GetMaximumBin()) for o in listOfPlottedObjects])
       #minValue = min([o.GetBinContent(o.GetMinimumBin()) - o.GetBinError(o.GetMinimumBin()) for o in listOfPlottedObjects])
   maxValue = hist.GetBinContent(hist.GetMaximumBin()) if useHistMax else can.GetUymax()
   minValue = can.GetUymin()

   for x in range(2, hist.GetXaxis().GetNbins()+1):
       xv = hist.GetBinLowEdge(x)
       line = TLine(xv, minValue, xv, maxValue)
       line.SetLineColor(17)
       line.SetLineStyle(lineStyle)
       line.Draw()
       tobject_collector.append(line)

   return tobject_collector







def AddShadedProfile(can,hist):
    tobject_collector=[]
    if can.GetPrimitive('pad_top') :
        GetTopPad(can).SetRightMargin (0.08)
        GetBotPad(can).SetRightMargin (0.08)
        tobject_collector.extend(AddShadedProfile(can.GetPrimitive('pad_top'), hist))
        GetBotPad(can).Modified()
        GetBotPad(can).Update()
        return tobject_collector
    from ROOT import TH1,TGraph,THStack,TColor, kGray, kBlue, TGaxis, TText
    listOfPlottedObjects = [o for o in can.GetListOfPrimitives() if isinstance(o,(TH1, THStack))]
    listOfPlottedObjects += [o.GetHistogram() for o in can.GetListOfPrimitives() if isinstance(o,TGraph)]
    #print listOfPlottedObjects
    minValue = 0; maxValue = 1
    if listOfPlottedObjects:
        #maxValue = max([o.GetBinContent(o.GetMaximumBin()) for o in listOfPlottedObjects])
        #minValue = min([o.GetBinContent(o.GetMinimumBin()) for o in listOfPlottedObjects])
        maxValue = max([o.GetBinContent(o.GetMaximumBin()) + o.GetBinError(o.GetMaximumBin()) for o in listOfPlottedObjects])
        minValue = min([o.GetBinContent(o.GetMinimumBin()) - o.GetBinError(o.GetMinimumBin()) for o in listOfPlottedObjects])
    #    #print [o.GetMaximum() for o in listOfPlottedObjects]
    #maxValue = can.GetUymax()
    #minValue = can.GetUymin()
    #print maxValue, minValue
    temp = hist.Clone()
    temp.SetName("ShadedProfile")
    temp.SetFillStyle(1001)
    lightgray = 1001
    #color = TColor(lightgray, 0.956, 0.956, 0.956)
    temp.SetFillColorAlpha(kGray, 0.15);
    temp.SetLineColor( kGray )
    #temp.Scale(1./16000)
    temp.SetStats(0)
    origMax = temp.GetMaximum()
    if origMax > 0:
        temp.Scale(1./origMax)
        minCanValue = can.GetUymin()
        temp.Scale(maxValue-minCanValue)
        # Get new min value
        for x in range(temp.GetNbinsX()+1):
            temp.AddBinContent(x, minCanValue)
        #temp.Scale(0.9*maxValue)
        #print maxValue
        #for (int x=1; x<=temp->GetXaxis()->GetNbins(); x++)
        #    temp->SetBinContent(x,temp->GetBinContent(x)+0.61)
        can.cd()
        temp.Draw("hist same")
        tobject_collector.append(temp)
        axis = TGaxis( can.GetUxmax(), can.GetUymin()
                     , can.GetUxmax(), maxValue
                     , 0, origMax
                     , 510, "+L")
        axis.SetLineColor(kGray)
        axis.SetLabelColor(kGray)
        #axis.SetTitle("count")
        axis.Draw()
        tobject_collector.append(axis)
        can.SetTicks( can.GetTickx(), 0 )
        can.Modified()
        can.Update()
        #text = TText(0,0, "count");
        #text.SetTextAlign(13)
        #text.SetTextAngle(90)
        #text.SetTextColor(kGray)
        #text.Draw()
        #tobject_collector.append(text)
    return tobject_collector








