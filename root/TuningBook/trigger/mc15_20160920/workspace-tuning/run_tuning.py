#!/usr/bin/env python
from timeit import default_timer as timer
from RingerCore import Logger, LoggingLevel
from TuningTools import TuningJob
from TuningTools.TuningJob import BatchSizeMethod
from TuningTools.PreProc import *
import logging

start = timer()
basepath = '/afs/cern.ch/work/j/jodafons/public/Online/tuning/mc15_201609XX/data'

DatasetLocationInput = basepath + '/mc15_13TeV.sgn.361106.probes.newLH.bkg.423300.vetotruth.strig.l2calo.veryLoose.npz'

tuningJob = TuningJob()
tuningJob( DatasetLocationInput, 
           neuronBoundsCol = [5, 5], 
           sortBoundsCol = 1,
           initBoundsCol = 1,
           etBin = 0,
           etaBin = 0,
           #confFileList = basepath + '/config.nn5to20_sorts50_1by1_inits100_100by100_201607XX/job.hn0016.s0044.il0000.iu0099.pic.gz',
           #ppFileList = basepath+'/ppMapStd.pic.gz',
           #crossValidFile = basepath+'/crossValid-JackKnife.pic.gz',
           crossValidFile = basepath+'/jobconfigs/user.wsfreund.crossValid-JackKnife.pic.gz/crossValid-JackKnife.pic.gz',
           epochs = 5000,
           showEvo = 0,
           doMultiStop = True,
           maxFail = 50,
           #batchSize = 10,
           #batchMethod = BatchSizeMethod.OneSample,
           #seed = 0,
           ppFile = basepath + '/jobconfigs/user.wsfreund.ppFile_et_eta_bins_indep.pic.gz/ppFile_et_eta_bins_indep.pic.gz',
           #crossValidSeed = 66,
           level = 20
           )

end = timer()

print 'execution time is: ', (end - start)      
