

from TuningTools.CreateTuningJobFiles import createTuningJobFiles
createTuningJobFiles( outputFolder   = 'config.n5to20.s10.i100.100IPerSPerN',
                      neuronBounds   = [5,20],
                      sortBounds     = 10,
                      nInits         = 100,
                      nNeuronsPerJob = 1,
                      nInitsPerJob   = 100,
                      nSortsPerJob   = 1,
                      compress       = True )

from TuningTools.CrossValid import CrossValid, CrossValidArchieve
crossValid = CrossValid(nSorts = 50,
                        nBoxes = 10,
                        nTrain = 6, 
                        nValid = 4,
                        #nTest=args.nTest,
                        #seed=args.seed,
                        #level=args.output_level
                        )
place = CrossValidArchieve( 'crossValid', 
                            crossValid = crossValid,
                            ).save( True )


from TuningTools.PreProc import *
#ppCol = PreProcCollection( PreProcChain( MapStd() ) )
ppCol = PreProcChain( Norm1() ) 
place = PreProcArchieve( 'ppFile', ppCol = ppCol ).save()

