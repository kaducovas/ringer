
__all__ = ['GeV','nvtx_bins','zee_etbins','coarse_etbins','default_etabins','ringer_tuning_etbins',\
          'ringer_tuning_etabins', 'RingerLayers']


# constants
GeV = 1000.

# Helper enumerator to navigate into the rings
class RingerLayers(object):
  PreSampler = (0,7)
  EM1  = (8,71)
  EM2  = (72,79)
  EM3  = (80,87)
  HAD1 = (88,91)
  HAD2 = (92,95)
  HAD3 = (96,99)


# Values retrieved from analysis trigger tool
default_etabins= [-2.47,-2.37,-2.01,-1.81,-1.52,-1.37,-1.15,-0.80,-0.60,-0.10,0.00,\
                   0.10, 0.60, 0.80, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47]

coarse_etbins = [4.,7.,10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,80.,150.]

zee_etbins = [0.,2.,4.,6.,8.,10.,12.,14.,16.,18.,20.,22.,24.,26.,28.,\
             30.,32.,34.,36.,38.,40.,42.,44.,46.,48.,50.,55.,60.,65.,70.,100.]

nvtx_bins = [                                         -0.5,
          0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5,
         10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,
         20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,
         30.5,31.5,32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5,
         40.5,41.5,42.5,43.5,44.5,45.5,46.5,47.5,48.5,49.5,
         50.5,51.5,52.5,53.5,54.5,55.5,56.5,57.5,58.5,59.5,
         60.5]

# The first ringer binning approch used in MC15c 2016/2017
ringer_tuning_etbins       = [14, 20, 30, 40, 50, 1e5 ]
ringer_tuning_etabins      = [0, 0.8 , 1.37, 1.54, 2.5]






