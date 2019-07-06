
from TrigL2CaloRingerConstants import SignaturesMap

nDict   = {'version':1, 'type': ['Fex' ]  , 'date':0, 'metadata':dict(), 'tuning':dict(), 'name':['v3_v4_merge']}
thrDict = {'version':1, 'type': ['Hypo']  , 'date':0, 'metadata':dict(), 'tuning':dict(), 'name':['v3_v4_merge']}


metadata = {'UseLumiTool': False,
            'UseLumiVar' : False,
            'UseEtaVar'  : False,
            'LumiCut'    : 60,
            'DoPileupCorrecion':False,
            'UseNoActivationFunctionInTheLastLayer': False,
            }

# Hold the metadata default configuration
nDict['metadata'] = metadata
thrDict['metadata'] = metadata

tuning = SignaturesMap()

from copy import copy
for tkey in tuning.keys():
 
  discrs = dict()
  thresholds = dict()
 
  print tuning[tkey].keys()
  tuning[tkey].pop('metadata')

  for bkey in sorted(tuning[tkey].keys()):

    discr = {'discriminator':dict(),'configuration':dict()}
    cut   = {'configuration':dict()}

    discr['discriminator']['nodes']         = tuning[tkey][bkey]['discriminator']['nodes']
    discr['discriminator']['weights']       = tuning[tkey][bkey]['discriminator']['weights']
    discr['discriminator']['bias']          = tuning[tkey][bkey]['discriminator']['bias']
    discr['configuration']['etBin']         = tuning[tkey][bkey]['configuration']['etBin']
    discr['configuration']['etaBin']        = tuning[tkey][bkey]['configuration']['etaBin']
    #discr['configuration']['benchmarkName'] = tuning[tkey][bkey]['configuration']['benchmarkName']
    #discr['configuration']['datecode']      = tuning[tkey][bkey]['configuration']['datecode']


    cut['configuration']['etBin']     = tuning[tkey][bkey]['configuration']['etBin']
    cut['configuration']['etaBin']    = tuning[tkey][bkey]['configuration']['etaBin']
    #cut['configuration']['datecode'] = tuning[tkey][bkey]['configuration']['datecode']
    myThr = tuning[tkey][bkey]['discriminator']['threshold']
    
    #if not type(myThr) is (list,tuple):
    #  cut['threshold'] = (0, 0, myThr)
    #else:
    cut['threshold'] = myThr

    discrs[bkey] = discr
    thresholds[bkey] = cut

  nDict['tuning'][tkey]     = discrs
  thrDict['tuning'][tkey]  = thresholds


#import pickle
#pickle.dump(nDict, open('TrigL2CaloRingerConstants.pic' ,'wb'))
#pickle.dump(nDict, open('TrigL2CaloRingerThresholds.pic','wb'))

pyfile = open('TrigL2CaloRingerConstants.py','w')
pyfile.write('def SignaturesMap():\n')
pyfile.write('  s=dict()\n')
for key in nDict.keys():
  pyfile.write('  s["%s"]=%s\n' % (key, nDict[key]))
pyfile.write('  return s\n')


pyfile = open('TrigL2CaloRingerThresholds.py','w')
pyfile.write('def ThresholdsMap():\n')
pyfile.write('  s=dict()\n')
for key in thrDict.keys():
  pyfile.write('  s["%s"]=%s\n' % (key, thrDict[key]))
pyfile.write('  return s\n')




