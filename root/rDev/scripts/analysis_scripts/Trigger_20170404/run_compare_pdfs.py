
mcpath = 'data/mc15_13TeV.ZeeLHLoose.JF17Truth.correction.root'
pppath = 'data/data16_13TeV.periodAtoK.physicsMain.ZeeLHLoose.correction.root'
mcBasepath = 'Event/Correction'
ppBasepath = 'Event/Correction'
nEtBins = 5
nEtaBins = 4


from RingerCore import restoreStoreGate
from TrigEgammaDevelopments.plots.AtlasStyle     import *
from ROOT import TCanvas, TLegend, kBlack, kBlue, kRed, kGreen, kAzure

SetAtlasStyle()
storeMC = restoreStoreGate( mcpath )
storePP = restoreStoreGate( pppath )

pidnames   = ['Tight' , 'Medium', 'Loose', 'VeryLoose']

for pid in pidnames:

  for etBinIdx in range(nEtBins):
  
    canvas = TCanvas('canvas','canvas', 1800, 1000 )
    canvas.Divide(nEtaBins, 2)
    objHolder = []
    ringerName = ('EFCalo_isRinger%s_v5') % (pid.replace('Very','V'))


    # for windows X 2 lines
    for etaBinIdx in range(nEtaBins):

      binname = ('et%d_eta%d')%(etBinIdx,etaBinIdx)
      
      path = mcBasepath+'/probes/'+pid+'/'+ringerName+'/'+binname
      h1 = storeMC.histogram(path+'/discriminantVsMu').ProjectionX().Clone()
      path = ppBasepath+'/probes/'+pid+'/'+ringerName+'/'+binname
      h2 = storePP.histogram(path+'/discriminantVsMu').ProjectionX().Clone()

      objHolder.append(canvas.cd( etaBinIdx+1 ))
      h1.SetTitle(('; Neural Network (Discriminant); Signal Counts (%s)')%(binname.replace('_',',')))
      h1.SetFillColor(kAzure+6)
      h1.SetLineColor(kAzure+6)
      h1.Rebin(10)
      h2.SetLineColor(kBlack)
      h2.Rebin(10)
      h1.Scale( 1./h1.GetMaximum() )
      h2.Scale( 1./h2.GetMaximum() )
      h1.Draw()
      h2.Draw('same')
      leg1 = TLegend(0.2,0.75,0.5,0.95)
      setLegend1(leg1)
      leg1.AddEntry(h1,'MC')
      leg1.AddEntry(h2,'Data')
      leg1.Draw()
      objHolder[-1].Update()

      path = mcBasepath+'/fakes/'+pid+'/'+ringerName+'/'+binname
      h3 = storeMC.histogram(path+'/discriminantVsMu').ProjectionX().Clone()
      path = ppBasepath+'/fakes/'+pid+'/'+ringerName+'/'+binname
      h4 = storePP.histogram(path+'/discriminantVsMu').ProjectionX().Clone()

      objHolder.append(canvas.cd( etaBinIdx+1 + nEtaBins ))
      h3.SetTitle(('; Neural Network (Discriminant); Background Counts (%s)')%(binname.replace('_',',')))
      h3.SetFillColor(kRed-7)
      h3.SetLineColor(kRed-7)
      h3.Rebin(10)
      h4.SetLineColor(kBlack)
      h4.Rebin(10)
      h3.Scale( 1./h3.GetMaximum() )
      h4.Scale( 1./h4.GetMaximum() )
      h3.Draw()
      h4.Draw('same')
      leg2 = TLegend(0.8,0.70,0.95,0.95)
      setLegend1(leg2)
      leg2.AddEntry(h3,'MC')
      leg2.AddEntry(h4,'Data')
      leg2.Draw()
 
      objHolder[-1].Update()
      objHolder.append(h1)
      objHolder.append(h2)
      objHolder.append(h3)
      objHolder.append(h4)
      objHolder.append(leg1)
      objHolder.append(leg2)

    canvas.SaveAs( ('nnOutput_distribution_%s__mcAndData_et%d_allEta.pdf')%(pid,etBinIdx) )
    del canvas





