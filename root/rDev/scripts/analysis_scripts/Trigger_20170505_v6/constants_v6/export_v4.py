#!/usr/bin/env python

from RingerCore import LoggingLevel, expandFolders, Logger
from TuningTools import CrossValidStatAnalysis, RingerOperation
from pprint import pprint
mainLogger = Logger.getModuleLogger( __name__ )

SP = 'SP'
Pd = 'Pd'
Pf = 'Pf'


####################### VeryLoose MC15 #########################
# 20 bins
VeryLooseConfigList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   16  ],
               [# Et 0, Eta 1
                   15 ],
               [# Et 0, Eta 2
                   5  ],
               [# Et 0, Eta 3
                   17  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   13  ],
               [# Et 1, Eta 1
                   12  ],
               [# Et 1, Eta 2
                   16 ],
               [# Et 1, Eta 3
                   13  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[   9  ],
               [# Et 2, Eta 1
                   5 ],
               [# Et 2, Eta 2
                   5  ],
               [# Et 2, Eta 3
                   12 ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   5 ],
               [# Et 3, Eta 1
                   7 ],
               [# Et 3, Eta 2
                   7  ],
               [# Et 3, Eta 3
                   6 ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   14 ],
               [# Et 4, Eta 1
                   5 ],
               [# Et 4, Eta 2
                   5  ],
               [# Et 4, Eta 3
                   5 ]]

            ]

VeryLooseRefBenchmarkList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   SP  ],
               [# Et 0, Eta 1
                   SP ],
               [# Et 0, Eta 2
                   SP  ],
               [# Et 0, Eta 3
                   Pd  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 1, Eta 1
                   SP  ],
               [# Et 1, Eta 2
                   Pd ],
               [# Et 1, Eta 3
                   SP  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 2, Eta 1
                   Pd ],
               [# Et 2, Eta 2
                   Pd  ],
               [# Et 2, Eta 3
                   Pd ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   Pd ],
               [# Et 3, Eta 1
                   SP ],
               [# Et 3, Eta 2
                   Pd  ],
               [# Et 3, Eta 3
                   SP ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   SP ],
               [# Et 4, Eta 1
                   Pd ],
               [# Et 4, Eta 2
                   Pd  ],
               [# Et 4, Eta 3
                   SP ]]

            ]

####################### Loose MC15 #########################
LooseConfigList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   9  ],
               [# Et 0, Eta 1
                   5 ],
               [# Et 0, Eta 2
                   10  ],
               [# Et 0, Eta 3
                   17  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   6  ],
               [# Et 1, Eta 1
                   17  ],
               [# Et 1, Eta 2
                   18 ],
               [# Et 1, Eta 3
                   19  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[   5  ],
               [# Et 2, Eta 1
                   5 ],
               [# Et 2, Eta 2
                   13  ],
               [# Et 2, Eta 3
                   5 ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   5 ],
               [# Et 3, Eta 1
                   5 ],
               [# Et 3, Eta 2
                   5  ],
               [# Et 3, Eta 3
                   7 ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   10 ],
               [# Et 4, Eta 1
                  11 ],
               [# Et 4, Eta 2
                   6  ],
               [# Et 4, Eta 3
                   5 ]]

            ]

LooseRefBenchmarkList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 0, Eta 1
                   Pd ],
               [# Et 0, Eta 2
                   Pd  ],
               [# Et 0, Eta 3
                   Pd  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 1, Eta 1
                   Pd  ],
               [# Et 1, Eta 2
                   Pd ],
               [# Et 1, Eta 3
                   Pd  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[  Pd  ],
               [# Et 2, Eta 1
                   Pd ],
               [# Et 2, Eta 2
                   Pd  ],
               [# Et 2, Eta 3
                   Pd ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   Pd ],
               [# Et 3, Eta 1
                   SP ],
               [# Et 3, Eta 2
                   Pd  ],
               [# Et 3, Eta 3
                   Pd ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   SP ],
               [# Et 4, Eta 1
                   Pd ],
               [# Et 4, Eta 2
                   Pd  ],
               [# Et 4, Eta 3
                   Pd ]]

            ]


####################### Medium MC15 #########################
# 20 bins
MediumConfigList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   12  ],
               [# Et 0, Eta 1
                   7 ],
               [# Et 0, Eta 2
                   12  ],
               [# Et 0, Eta 3
                   18  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   6  ],
               [# Et 1, Eta 1
                   17  ],
               [# Et 1, Eta 2
                   19 ],
               [# Et 1, Eta 3
                   19  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[   6  ],
               [# Et 2, Eta 1
                   5 ],
               [# Et 2, Eta 2
                   5  ],
               [# Et 2, Eta 3
                   16 ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   5 ],
               [# Et 3, Eta 1
                   5 ],
               [# Et 3, Eta 2
                   6  ],
               [# Et 3, Eta 3
                   15 ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   5 ],
               [# Et 4, Eta 1
                   7 ],
               [# Et 4, Eta 2
                   10  ],
               [# Et 4, Eta 3
                   5 ]]

            ]


MediumRefBenchmarkList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 0, Eta 1
                   Pd ],
               [# Et 0, Eta 2
                   Pd  ],
               [# Et 0, Eta 3
                   Pd  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 1, Eta 1
                   Pd  ],
               [# Et 1, Eta 2
                   Pd ],
               [# Et 1, Eta 3
                   Pd  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[  Pd  ],
               [# Et 2, Eta 1
                   Pd ],
               [# Et 2, Eta 2
                   Pd  ],
               [# Et 2, Eta 3
                   Pd ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   SP ],
               [# Et 3, Eta 1
                   Pd ],
               [# Et 3, Eta 2
                   Pd  ],
               [# Et 3, Eta 3
                   Pd ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   SP ],
               [# Et 4, Eta 1
                   SP ],
               [# Et 4, Eta 2
                   Pd  ],
               [# Et 4, Eta 3
                   Pd ]]

            ]



####################### Tight MC15 #########################
# 20 bins
TightConfigList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   11  ],
               [# Et 0, Eta 1
                   5 ],
               [# Et 0, Eta 2
                   5  ],
               [# Et 0, Eta 3
                   16  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   19  ],
               [# Et 1, Eta 1
                   6  ],
               [# Et 1, Eta 2
                   8 ],
               [# Et 1, Eta 3
                   19 ]], #15
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[   13  ],
               [# Et 2, Eta 1
                  13 ],
               [# Et 2, Eta 2
                   9  ],
               [# Et 2, Eta 3
                   19 ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   6 ],
               [# Et 3, Eta 1
                   7 ],
               [# Et 3, Eta 2
                   5  ],
               [# Et 3, Eta 3
                   7 ]],
                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   5 ],
               [# Et 4, Eta 1
                   19 ], #15
               [# Et 4, Eta 2
                   5  ],
               [# Et 4, Eta 3
                   7 ]]

            ]


TightRefBenchmarkList = [
                # EFCalo, Et 0, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 0, Eta 1
                   Pd ],
               [# Et 0, Eta 2
                   Pd  ],
               [# Et 0, Eta 3
                   Pd  ]],
                # EFCalo, Et 1, Eta 0
                #  Pd, SP, Pf
              [[   Pd  ],
               [# Et 1, Eta 1
                   Pd  ],
               [# Et 1, Eta 2
                   Pd ],
               [# Et 1, Eta 3
                   Pd  ]],
                # EFCalo, Et 2, Eta 0
                #  Pd, SP, Pf
              [[  Pd  ],
               [# Et 2, Eta 1
                   Pd ],
               [# Et 2, Eta 2
                   Pd  ],
               [# Et 2, Eta 3
                   Pd ]],
                # EFCalo, Et 3, Eta 0
                #  Pd, SP, Pf
              [[   Pd ],
               [# Et 3, Eta 1
                   Pd ],
               [# Et 3, Eta 2
                   Pd  ],
               [# Et 3, Eta 3
                   Pd ]],

                # EFCalo, Et 4, Eta 0
                #  Pd, SP, Pf
              [[   Pd ],
               [# Et 4, Eta 1
                   Pd ],
               [# Et 4, Eta 2
                   Pd  ],
               [# Et 4, Eta 3
                   Pd ]]

            ]



####################### Global Configuration #########################
basepath = '/home/jodafons/CERN-DATA/Online/tuning/mc15_201611XX_v4/nnstat'
veryLoosePath = 'user.hellen.nnstat.mc15_13TeV.361106.423300.sgn.LH.bkg.vtruth.trig.veryloose.mas-RNT-0000/'
loosePath     = 'user.hellen.nnstat.mc15_13TeV.361106.423300.sgn.LH.bkg.vtruth.trig.loose.mas-RNT-0000/'
mediumPath    = 'user.hellen.nnstat.mc15_13TeV.361106.423300.sgn.LH.bkg.vtruth.trig.medium.mas-RNT-0000/'
tightPath     = 'user.hellen.nnstat.mc15_13TeV.361106.423300.sgn.LH.bkg.vtruth.trig.tight.mas-RNT-0000/'

pathList = [tightPath, mediumPath, loosePath, veryLoosePath]



configList =  [
                TightConfigList,
                MediumConfigList,
                LooseConfigList,
                VeryLooseConfigList,
              ]

refBenchmarkList = [
                    TightRefBenchmarkList,
                    MediumRefBenchmarkList,
                    LooseRefBenchmarkList,
                    VeryLooseRefBenchmarkList,
                    ]

tuningNameList = [
                    'ElectronHighEnergyTightConf',
                    'ElectronHighEnergyMediumConf',
                    'ElectronHighEnergyLooseConf',
                    'ElectronHighEnergyVeryLooseConf',
                 ]
# Et Bins
etBins       = [15, 20, 30, 40, 50, 500000 ]
# Eta bins
etaBins      = [0, 0.8 , 1.37, 1.54, 2.5]

# [Tight, Medium, Loose and VeryLoose]
#thrRelax     = [-0.1,-0.1,0,0]
#thrRelax     = [0,0,0,0]

outputDict    = {'version':1, 'type': ['Fex' ]  , 'date':0, 'metadata':dict(), 'tuning':dict(), 'name': ['v5']}
thresholdDict = {'version':1, 'type': ['Hypo']  , 'date':0, 'metadata':dict(), 'tuning':dict(), 'name': ['v5']}


metadata = {'UseLumiTool': False,
            'UseLumiVar' : True,
            'UseEtaVar'  : True,
            'LumiCut'    : 60,
            'UseNoActivationFunctionInTheLastLayer': False,
            'DoPileupCorrection': False,
            }

# Hold the metadata default configuration
outputDict['metadata'] = metadata
thresholdDict['metadata'] = metadata


def convert2list( l ):
  if not type(l) is list:
    return l.tolist()
  else:
    return l

####################### Extract Ringer Configuration #########################
import numpy as np

for idx, tuningName in enumerate(tuningNameList):
  files = expandFolders(basepath+'/'+pathList[idx])
  crossValGrid=[]
  for path in files:
    if path.endswith('.pic'):
      crossValGrid.append(path)
  
  pprint(crossValGrid)
  pprint(configList[idx])
  pprint(refBenchmarkList[idx])
  c = CrossValidStatAnalysis.exportDiscrFiles(crossValGrid,
                                              RingerOperation.L2,
                                              triggerChains=tuningName,
                                              refBenchCol=refBenchmarkList[idx],
                                              EtBins = etBins,
                                              EtaBins = etaBins,
                                              configCol=configList[idx])

  mainLogger.info('%d bins found in this tuning: %s',len(c[tuningName].keys()),tuningName)

  mainLogger.info('Dumping tuning with name: %s',tuningName)
  dDict = dict()
  tDict = dict()
  for etIdx in range(len(etBins)-1):
    for etaIdx in range(len(etaBins)-1):
      key = ('et%d_eta%d')%(etIdx,etaIdx)

      etBin = c[tuningName][key]['configuration']['etBin']
      etaBin= c[tuningName][key]['configuration']['etaBin']

      #mainLogger.info('[%s]: Tuning E_T Binning found [%d,%d] rewrite to [%d,%d]',key,oldEtBin[0],oldEtBin[1],etBin[0],etBin[1])
      #mainLogger.info('[%s]: Tuning eta Binning found [%d,%d] rewrite to [%d,%d]',key,oldEtaBin[0],oldEtaBin[1],etaBin[0],etaBin[1])

      discr     = {'discriminator':dict(),'configuration':dict()}
      threshold = {'configuration':dict()}
    
      discr['discriminator']['nodes']         = convert2list(c[tuningName][key]['discriminator']['nodes'])
      discr['discriminator']['weights']       = convert2list(c[tuningName][key]['discriminator']['weights'])
      discr['discriminator']['bias']          = convert2list(c[tuningName][key]['discriminator']['bias'])
      discr['configuration']['etBin']         = etBin
      discr['configuration']['etaBin']        = etaBin
      discr['configuration']['benchmarkName'] = c[tuningName][key]['configuration']['benchmarkName']


      threshold['configuration']['etBin']     = etBin
      threshold['configuration']['etaBin']    = etaBin
      myThr  = c[tuningName][key]['discriminator']['threshold']
    
      if not type(myThr) is list:
        threshold['threshold'] = (0, 0, myThr)
      else:
        threshold['threshold'] = myThr

      dDict[key] = discr
      tDict[key] = threshold

  outputDict['tuning'][tuningName] = dDict
  thresholdDict['tuning'][tuningName] = tDict

####################### Write Ringer Configuration #########################

pyfile = open('TrigL2CaloRingerConstants_v4.py','w')
pyfile.write('def SignaturesMap():\n')
pyfile.write('  s=dict()\n')
for key in outputDict.keys():
  pyfile.write('  s["%s"]=%s\n' % (key, outputDict[key]))
pyfile.write('  return s\n')


pyfile = open('TrigL2CaloRingerThresholds_v4.py','w')
pyfile.write('def ThresholdsMap():\n')
pyfile.write('  s=dict()\n')
for key in thresholdDict.keys():
  pyfile.write('  s["%s"]=%s\n' % (key, thresholdDict[key]))
pyfile.write('  return s\n')




#output = open('TrigL2CaloRingerConstants.py','w')
#output.write('def SignaturesMap():\n')
#output.write('  signatures=dict()\n')
#
#for key in tuningNameList:
#  output.write('  signatures["%s"]=%s\n' % (key, outputDict[key]))
#
#output.write('  return signatures\n')
#

###########################################################################







