

from TrigL2CaloRingerConstants_v3 import SignaturesMap
v3 = SignaturesMap()['tuning']
from TrigL2CaloRingerConstants_v4 import SignaturesMap
v4 = SignaturesMap()['tuning']



pidnames = v3.keys()
from copy import copy
for pid in pidnames:
  print pid
  geonames = v3[pid].keys()
  for geo in geonames:
    if 'eta2' in geo:
      v3[pid][geo] = copy(v4[pid][geo])


pyfile = open('TrigL2CaloRingerConstants.py','w')
pyfile.write('def SignaturesMap():\n')
pyfile.write('  signatures=dict()\n')
for pidname in v3.keys():
  pyfile.write('  signatures["%s"]=%s\n' % (pidname, v3[pidname]))
pyfile.write('  return signatures\n')
