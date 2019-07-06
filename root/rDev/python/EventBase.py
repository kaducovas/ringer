
__all__ = ['EventBase']

from RingerCore import  ( Logger, checkForUnusedVars,  traverse
                       , retrieve_kw, NotSet, appendToFileName
                       , ensureExtension, secureExtractNpItem
                       , progressbar, csvStr2List, expandFolders
                       )

from TuningTools.dataframe.EnumCollection import Dataframe as DataframeEnum
from TrigEgammaDevelopments.StatusCode    import StatusCode

# Import all root classes
import ROOT

class EventBase( Logger ):
    
  def __init__(self, **kw):
    
    Logger.__init__(self, kw)
    # Retrieve all information needed
    self._fList      = retrieve_kw( kw, 'inputFiles', NotSet                      )
    self._ofile      = retrieve_kw( kw, 'outputFile', "histos.root"               )
    self._treePath   = retrieve_kw( kw, 'treePath'  , NotSet                      )
    self._dataframe  = retrieve_kw( kw, 'dataframe' , DataframeEnum.SkimmedNtuple )
    self._nov        = retrieve_kw( kw, 'nov'       , -1                          )
    self._fList = csvStr2List ( self._fList )
    self._fList = expandFolders( self._fList )
    
    # Loading libraries
    if ROOT.gSystem.Load('libTuningTools') < 0:
       self._fatal("Could not load TuningTools library", ImportError)

    self._containersSvc = {}
    self._storegateSvc = NotSet
    import random
    import time
    random.seed(time.time())
    # return a random number 
    self._id = random.randrange(100000)
 

  def __getRunNumber(self,d):
    from ROOT import TFile
    f=TFile(d,'r')
    name = f.GetListOfKeys()[0].GetName()
    try:
      f.Close(); del f
      return name
    except:
      self._logger.warning('Can not retrieve the run number')

  # Initialize all services
  def initialize( self ):

    self._logger.info('Initializing EventReader...')

    ### Prepare to loop:
    self._t = ROOT.TChain()
    for inputFile in progressbar(self._fList, len(self._fList),
                                 logger = self._logger,
                                 prefix = "Creating collection tree "):
      # Check if file exists
      self._f  = ROOT.TFile.Open(inputFile, 'read')
      if not self._f or self._f.IsZombie():
        self._warning('Couldn''t open file: %s', inputFile)
        continue
      # Inform user whether TTree exists, and which options are available:
      self._debug("Adding file: %s", inputFile)
      
      # Custon directory token
      if '*' in self._treePath:
        dirname = self._f.GetListOfKeys()[0].GetName()
        treePath = self._treePath.replace('*',dirname)
      else:
        treePath=self._treePath
      obj = self._f.Get(treePath)
      if not obj:
        self._warning("Couldn't retrieve TTree (%s)!", treePath)
        self._info("File available info:")
        self._f.ReadAll()
        self._f.ReadKeys()
        self._f.ls()
        continue
      elif not isinstance(obj, ROOT.TTree):
        self._fatal("%s is not an instance of TTree!", treePath, ValueError)
      self._t.Add( inputFile+'/'+treePath )
    # Turn all branches off.
    self._t.SetBranchStatus("*", False)
    # RingerPhysVal hold the address of required branches
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      self._event = ROOT.SkimmedNtuple()
    elif self._dataframe is DataframeEnum.PhysVal:
      self._event = ROOT.RingerPhysVal()
    else:
      return StatusCode.FATAL

    # Ready to retrieve the total number of events
    self._t.GetEntry(0)
    ## Allocating memory for the number of entries
    self._entries = self._t.GetEntries()

    self._logger.info("Creating containers...")
    # Allocating containers
    from TrigEgammaDevelopments.dataframe.Electron   import Electron
    from TrigEgammaDevelopments.dataframe.FastCalo   import FastCalo
    from TrigEgammaDevelopments.dataframe.EventInfo  import EventInfo
    from TrigEgammaDevelopments.dataframe.MonteCarlo import MonteCarlo
  
    # Initialize the base of this container
    self._containersSvc  = {'Electron':Electron(),
                            'FastCalo':FastCalo(),
                            'EventInfo':EventInfo(), 
                            'MonteCarlo':MonteCarlo(), 
                            }

    # force the event id number for this event looper
    self._containersSvc['EventInfo'].setId( self.id() )

    # configure all EDMs needed
    for key, edm  in self._containersSvc.iteritems():
      # add properties
      edm.dataframe = self._dataframe
      edm.tree = self._t
      edm.level = self._level
      edm.event = self._event
      edm.setSvc(self._containersSvc)
      # If initializations is failed, we must remove this from the container 
      # service
      if(edm.initialize().isFailure()):
        self._logger.warning('Impossible to create the EDM: %s',key)

    # Create the StoreGate service
    if not self._storegateSvc:
      self._logger.info("Creating StoreGate...")
      from RingerCore import StoreGate
      self._storegateSvc = StoreGate( self._ofile)
    else:
      self._logger.info('The StoraGate was created for ohter service. Using the service setted by client.')

    return StatusCode.SUCCESS

  def execute(self):
    for key, edm in self._containersSvc.iteritems():
      if edm.execute().isFailure():
        self._logger.warning( 'Can not execute the edm %s', key )
    return StatusCode.SUCCESS

  def finalize(self):
    self._storegateSvc.write()
    del self._storegateSvc
    return StatusCode.SUCCESS

  def getEntries(self):
    return self._entries

  def getEntry( self, entry ):
    self._t.GetEntry( entry )

  def retrieve( self, key ):
    try:
      return self._containersSvc[key]
    except KeyError:
      self._logger.warning('Container %s not found.',key)

  def getSvc(self):
    return self._containersSvc, self._storegateSvc

  def getStoreSvc(self):
    return self._storegateSvc

  def setStoreSvc(self, store):
    self._storegateSvc = store

  @property
  def nov(self):
    if self._nov < 0:
      return self.getEntries()
    else:
      return self._nov

  def id(self):
    return self._id


