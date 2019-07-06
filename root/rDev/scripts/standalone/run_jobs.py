#!/usr/bin/env python


from TrigEgammaDevelopments.Event          import EventLooper
from TrigEgammaDevelopments.dataframe      import ElectronCandidate
from TuningTools.dataframe.EnumCollection  import Dataframe as DataframeEnum
from RingerCore                            import LoggingLevel, Logger, csvStr2List, expandFolders


import argparse
mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFiles', action='store', 
    dest='fList', required = True, nargs='+',
    help = "The input files.")


parser.add_argument('-c','--command', action='store', 
    dest='command', required = True,
    help = "The command job")


parser.add_argument('-m','--merge', action='store_true',
    dest='merge', required = False,
    help = 'merge all files.')

parser.add_argument('-n','--maxJobs', action='store', 
    dest='maxJobs', required = False, default = 10,
    help = "The number of jobs inside of the pipe.")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()

# Take all files
fList = csvStr2List ( args.fList )
fList = expandFolders( fList )
process_pipe = []
output_stack = []


import random
import time
random.seed(time.time())
# return a random number 
id = random.randrange(100000)

import subprocess
from pprint import pprint

while len(fList) > 0:
  if len(process_pipe) < int(args.maxJobs):
    job_id = len(fList)
    f = fList.pop()
    output_stack.append( ('output_%d_%d.root') % (id, job_id) )
    command = args.command+' '
    command += ('-i %s -o %s') % (f, output_stack[-1])
    mainLogger.info( ('adding process into the stack with id %d')%(job_id), extra={'color':'0;35'})
    pprint(command)
    proc = subprocess.Popen(command.split(' '))
    #thread = Thread(group=None, target=lambda:os.system(command))
    #thread.run()
    process_pipe.append( (job_id, proc) )

  for proc in process_pipe:
    if not proc[1].poll() is None:
      mainLogger.info( ('pop process id (%d) from the stack')%(proc[0]), extra={'color':'0;35'})
      # remove proc from the pipe
      process_pipe.remove(proc)


# Check pipe process
# Protection for the last jobs
while len(process_pipe)>0:
  for proc in process_pipe:
    if not proc[1].poll() is None:
      mainLogger.info( ('pop process id (%d) from the stack')%(proc[0]), extra={'color':'0;35'})
      # remove proc from the pipe
      process_pipe.remove(proc)



if args.merge:
  mainLogger.info( 'merge all files...', extra={'color':'0;35'})
  command = 'hadd output_'+str(id)+'_merged.root '
  for o in output_stack:
    command+=' '+o
  os.system(command)
  for o in output_stack:
    os.system('rm '+o)


