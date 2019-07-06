

def retrieve_py_module(logger, pypath, classname):
  try:
    import imp
    obj__Module__ = imp.load_source(classname, pypath)
  except ImportError:
    logger.fatal('Can not import the discriminator %s',pypath)
  try: # Remove junk file created by the python reader
    import os
    #os.remove( pypath+'c')
  except:
    logger.warning('%sc not found',pypath)
  try:
    logger.info('PathResolver: %s',pypath)
    return obj__Module__
  except KeyError:
    logger.fatal('Key %s not found in this module. Abort')





from RingerCore import Logger, LoggingLevel
import argparse

mainLogger = Logger.getModuleLogger("ConvertToPickle")

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFiles', action='store', 
    dest='inputFiles', required = True, nargs='+',
    help = "The input files that will be used to generate the pic")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

tuningName = args.inputFiles[0]+'/TrigL2CaloRingerConstants.py'
thresholdName = args.inputFiles[0]+'/TrigL2CaloRingerThresholds.py'


rawTuning    = retrieve_py_module(mainLogger, tuningName   , 'SignaturesMap').SignaturesMap()
rawThreshold = retrieve_py_module(mainLogger, thresholdName, 'ThresholdsMap').ThresholdsMap()

import pickle
pickle.dump(rawTuning, open('TrigL2CaloRingerConstants.pic','wb'))
pickle.dump(rawThreshold, open('TrigL2CaloRingerThresholds.pic','wb'))



