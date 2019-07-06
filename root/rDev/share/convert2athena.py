 
def listToVector( l, vec ):
  vec.clear()
  for value in l:
    vec.push_back(value)

def createRootParameter( type_name, name, value):
  from ROOT import TParameter
  return TParameter(type_name)(name,value)

def __retrieve_py_module( pypath, classname):
   #try:
   import imp
   obj__Module__ = imp.load_source(classname, pypath)
   return obj__Module__


def clearName( key ):
  if 'Conf' in key:
    key=key.replace('Conf','')
  if 'High' in key:
    key=key.replace('High','')
  if 'Energy' in key:
    key=key.replace('Energy','')
  return key




########################################################################
 
import argparse


parser = argparse.ArgumentParser(description = '',
                                     add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-s','--signatures', action='store', 
    dest='sig', required = True,
    help = "The python discriminator path ")

parser.add_argument('-t','--thresholds', action='store', 
    dest='thr', required = True,
    help = "The python thresholds path ")

parser.add_argument('--name', action='store', 
    dest='name', required = True,
    help = "The name of the discriminadot ")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
name = args.name
signatures =  __retrieve_py_module( args.sig, 'SignaturesMap').SignaturesMap()


from ROOT import TFile, TEnv, TTree
from ROOT import std

for key in signatures['tuning'].keys():
 
  s = signatures['tuning'][key]
  m = signatures['metadata']
 
  key = clearName( key )
  f1 = TFile(('TrigL2CaloRinger%sConstants.root')%(key) ,'recreate')
  createRootParameter( 'int'   , '__version__', 2).Write()
  f1.mkdir('tuning')
  f1.cd('tuning')
 
  # t->GetEntry(0)  t->GetEntry(0);; Compile the neural network
  t          = TTree('discriminators','')
  n          = std.vector('unsigned int')()
  w          = std.vector('double')()
  b          = std.vector('double')()
  etbin      = std.vector('double')()
  etabin     = std.vector('double')()
 
  t.Branch( 'nodes'      , 'vector<unsigned int>', n      )
  t.Branch( 'weights'    , 'vector<double>', w      )
  t.Branch( 'bias'       , 'vector<double>', b      )
  t.Branch( 'etBin'      , 'vector<double>', etbin  )
  t.Branch( 'etaBin'     , 'vector<double>', etabin )
 
  for bkey in sorted(s.keys()):
    net = s[bkey]
    listToVector( net['discriminator']['weights'] , w      )
    listToVector( net['discriminator']['nodes']   , n      )
    listToVector( net['discriminator']['bias']    , b      )
    listToVector( net['configuration']['etBin']   , etbin  )
    listToVector( net['configuration']['etaBin']  , etabin )
    t.Fill()
  #t.Write()
 
  f1.mkdir('metadata')
  f1.cd('metadata')
 
  for key in m.keys():
    value = m[key]
    if type(value) is int:
      createRootParameter( 'int', key, value).Write()
    if type(value) is bool:
      createRootParameter( 'bool', key, value).Write()
 
  f1.Write()
  f1.Close()
 

thresholds =  __retrieve_py_module(args.thr, 'ThresholdsMap').ThresholdsMap()

for key in thresholds['tuning'].keys():
 
  s = thresholds['tuning'][key]
  m = thresholds['metadata']
 
  # Compile the thresholds
  key = clearName( key )
  f2 = TFile(('TrigL2CaloRinger%sThresholds.root')%(key),'recreate')

  createRootParameter( 'int', '__version__', 2).Write()
  f2.mkdir('tuning')
  f2.cd('tuning')
 
  t          = TTree('thresholds','')
  thr        = std.vector('double')()
  etbin      = std.vector('double')()
  etabin     = std.vector('double')()
 
  t.Branch( 'thresholds' , 'vector<double>', thr        )
  t.Branch( 'etBin'      , 'vector<double>', etbin      )
  t.Branch( 'etaBin'     , 'vector<double>', etabin     )
 
  for bkey in sorted(s.keys()):
    net = s[bkey]
    listToVector( net['threshold']                , thr    )
    listToVector( net['configuration']['etBin']   , etbin  )
    listToVector( net['configuration']['etaBin']  , etabin )
    t.Fill()
  #t.Write()
 
  f2.mkdir('metadata')
  f2.cd('metadata')
 
  for key in m.keys():
    value = m[key]
    if type(value) is int:
      createRootParameter( 'int', key, value).Write()
    if type(value) is bool:
      createRootParameter( 'bool', key, value).Write()
   
  f2.Write()
  f2.Close()
 
 




