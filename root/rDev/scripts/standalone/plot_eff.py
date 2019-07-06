#!/usr/bin/env python
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
    dest='key', required = False, default = None,
    help = "key generated to reproduce plots")

parser.add_argument('-l','--atlaslabel', action='store', 
    dest='atlaslabel', required = False, default  = 'Internal',
    help = "The Atlas label")

parser.add_argument('-b','--isBkg', action='store_true', 
    dest='bkg', required = False, 
    help = "Use this to switch the scale to background mode")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
efficiencyParser = EfficiencyParser( args.inputFiles ) 
efficiencyParser(key = args.key,  atlaslabel = args.atlaslabel, outputdir=args.outputDir, isbackground=args.bkg)



