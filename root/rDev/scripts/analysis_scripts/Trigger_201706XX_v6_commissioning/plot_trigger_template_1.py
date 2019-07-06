#!/usr/bin/env python


def match_template1( resume ):
  from pprint import pprint
  def remove_ringer_name(c):
    from copy import copy
    chain=copy(c)
    chain=chain.replace('ringer','')
    chain=chain.replace('__','_')
    if chain.endswith('_'):
      chain=chain[0:len(chain)-1]
    return chain
  
  pairs = []
  for idx, r in enumerate(resume):
    pairs.append((r[1],idx))
  keys=[]
  while len(pairs)>0:
    t2=None
    for idx, t in enumerate(pairs):
      if 'ringer' in t[0]:
        t2 = pairs.pop(idx)
        break
    if not t2:
      break
    for idx, t in enumerate(pairs):
      if remove_ringer_name(t2[0]) == t[0]:
        t1 = pairs.pop(idx)
        break
    keys.append( (t1,t2) )
  
  return keys


def match_template2(resume):
  pairs = []
  for idx, r in enumerate(resume):
    pairs.append((r[1],idx))
  keys=[]
  while len(pairs)>0:
    t1 = pairs.pop()
    keys.append( (t1,t1) )
  return keys


from TrigEgammaDevelopments.plots.Efficiency import EfficiencyParser
from RingerCore                        import Logger, LoggingLevel, BooleanStr
import argparse

mainLogger = Logger.getModuleLogger("PlotTool")

parser = argparse.ArgumentParser(description = '',
                                     add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFiles', action='store', 
    dest='inputFiles', required = True, nargs='+',
    help = "The input files that will be used to generate the plots")

parser.add_argument('-o','--outputDir', action='store', 
    dest='outputDir', required = False, default = 'plots',
    help = "The output directory name.")

parser.add_argument('-k','--key', action='store', 
    dest='key_template', required = False, default = 'EFF:0:%s,EFF:0:%s',
    help = "the key template")

parser.add_argument('-l','--atlaslabel', action='store', 
    dest='atlaslabel', required = False, default  = 'Internal',
    help = "The Atlas label")

parser.add_argument('-b','--isBkg', action='store_true', 
    dest='bkg', required = False, 
    help = "Use this to switch the scale to background mode")

parser.add_argument('-e','--doEffLabel', action='store_true', 
    dest='doEffLabel', required = False, 
    help = "Add an efficiency label. This will works only for two curves plot.")

parser.add_argument('-p','--doPDF', action='store_true', 
    dest='doPDF', required = False, 
    help = "Do PDF presentation..")

parser.add_argument('--PDF_title', action='store', 
    dest='pdftitle', required = False, default  = 'Efficiency plots for all triggers',
    help = "The PDF title")

parser.add_argument('--PDF_output', action='store', 
    dest='pdfoutput', required = False, default  = 'efficiency_plots',
    help = "The PDF output name")





import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
efficiencyParser = EfficiencyParser( args.inputFiles ) 
resume = efficiencyParser.getResume()[0]['Efficiency']

figures=[]; keys=[]
resume_pairs = match_template1( resume )
for p in resume_pairs:
  keys.append( (args.key_template) % (p[0][1],p[1][1]) )
 


for key in keys:
  cmd=('python ../../standalone/plot_eff.py -i %s %s -k %s -o %s -l %s')%(args.inputFiles[0], \
      args.inputFiles[0], key, args.outputDir,args.atlaslabel)
  if args.doEffLabel:
    cmd+=' -e'
  if args.bkg:
    cmd+=' -b'
  print cmd
  os.system(cmd)
  #f = efficiencyParser(key = key,  atlaslabel = args.atlaslabel, outputdir=args.outputDir, isbackground=args.bkg)
  #figures.extend(f)


from RingerCore.tex.BeamerAPI import BeamerTexReportTemplate2,BeamerSection,BeamerSubSection,\
                                     BeamerMultiFigureSlide,BeamerFigureSlide,BeamerTexReport


pdftitle=args.pdftitle
pdfoutput=args.pdfoutput
trigger=['L1Calo','L2Calo','L2','EFCalo','HLT']
plot_names = ['eff_et','eff_eta','eff_mu']
# apply beamer
import os
localpath = os.getcwd()+'/'+args.outputDir

if args.doPDF:
  with BeamerTexReportTemplate2( theme = 'Berlin'
                               , _toPDF = True
                               , title = pdftitle
                               , outputFile = pdfoutput
                               , font = 'structurebold' ):
    for info in resume_pairs: 
      t1=info[0]; t2=info[1]
      oname=t1[0]+'_'+t2[0]
      section = (t1[0]+' and '+t2[0]).replace('_','\_')
      paths=[]
      for plot in plot_names:
        for t in trigger:
          abspath = localpath+'/'+t+'_'+oname+'_'+plot+'.pdf'
          paths.append( abspath )
      with BeamerSection( name = section ): 
        BeamerMultiFigureSlide( title = 'Efficiency Plots'
                      , paths = paths
                      , nDivWidth = 5 # x
                      , nDivHeight = 3 # y
                      , texts=None
                      , fortran = False
                      , usedHeight = 0.7
                      , usedWidth = 0.95
                      )
  
  
  














