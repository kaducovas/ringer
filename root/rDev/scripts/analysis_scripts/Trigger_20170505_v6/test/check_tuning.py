


import argparse


parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-r','--reference', action='store', 
    dest='reference', required = True,
    help = "The reference tuning file")

parser.add_argument('-t','--tuning', action='store', 
    dest='tuning', required = True,
    help = "The new tuning file")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


import os
#basepath = os.environ['ROOTCOREBIN']

def load_signatures(pypath, classname='SignaturesMap'):
  import imp
  obj__Module__ = imp.load_source(classname, pypath)
  return obj__Module__.SignaturesMap()






# get tuning dictionary
ref_tuning = load_signatures( args.reference )['tuning']
new_tuning = load_signatures( args.tuning )


for name, ref in ref_tuning.iteritems():
  
  new = new_tuning[name]
  
  for bin_key in sorted(ref.keys()):

    bin_new_net = new[bin_key]
    bin_ref_net = ref[bin_key]

    for key, ref_o in bin_ref_net['discriminator'].iteritems():
      new_o = bin_new_net['discriminator'][key]
      print name,' - ',bin_key,' - ',key,' - ',sum(new_o)-sum(ref_o)



