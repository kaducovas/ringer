__all__ = ['Threshold', 'NeuralNetwork']

from RingerCore import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars

import numpy as np

class Threshold(object):

  def __init__(self, obj=None):
    self._alpha     = 0 
    self._beta      = 0 
    self._thr       = 0 
    self._etmin     = 0 
    self._etmax     = 0 
    self._etamin    = 0 
    self._etamax    = 0
    self._empty     = True
    if obj:
      self.fromRawDict(obj)
  
  def threshold( self, avgmu = None):
    if avgmu is None:
      return self._thr
    else:
      return self._alpha*avgmu + self._beta

  def checkForCompatibleBinning(self, et, eta):
    if et > self._etmin and et <= self._etmax:
      if eta > self._etamin and eta <= self._etamax:
        return True
    return False

  @property
  def etmin(self):
    return self._etmin
  
  @property
  def etamin(self):
    return self._etamin
  
  @property
  def etmax(self):
    return self._etmax
  
  @property
  def etamax(self):
    return self._etamax

  @property
  def alpha(self):
    return self._alpha

  @property
  def beta(self):
    return self._beta

  @property
  def thr(self):
    return self._thr

  @property
  def empty(self):
    self._empty

  @etamin.setter
  def etamin(self, v):
    self._etamin=v

  @etamax.setter
  def etamax(self, v):
    self._etamax=v
  
  @etmin.setter
  def etmin(self, v):
    self._etmin=v
  
  @etmax.setter
  def etmax(self, v):
    self._etmax=v

  @alpha.setter
  def alpha(self,v):
    self._alpha=v

  @beta.setter
  def beta(self, v):
    self._beta=v

  @thr.setter
  def thr(self, v):
    self._thr=v

  @empty.setter
  def empty(self,v):
    self._empty=v

  # Helper method to retrieve all information from the dict
  def fromRawDict(self, obj):
    self._alpha     = obj['threshold'][0]
    self._beta      = obj['threshold'][1]
    self._thr       = obj['threshold'][2]
    self._etmin     = obj['configuration']['etBin'][0]
    self._etmax     = obj['configuration']['etBin'][1]
    self._etamin    = obj['configuration']['etaBin'][0]
    self._etamax    = obj['configuration']['etaBin'][1]
    self._empty     = False

  def toRaw(self):
    obj = {'configuration':dict()}
    obj['configuration']['etBin'] = (self._etmin, self._etmax)
    obj['configuration']['etaBin'] = (self._etamin, self._etamax)
    obj['threshold'] = [self._alpha,self._beta,self._thr]
    return obj


class Layer(Logger):
  """
    The Neural Network Layer implemented in python using numpy as core
    to propagate all values.
  """
  def __init__(self, w, b, **kwargs):
    Logger.__init__(self)
    self.layer     = retrieve_kw(kwargs, 'Layer'       ,0       )
    self.funcName  = retrieve_kw(kwargs, 'funcName'  ,None    )
    checkForUnusedVars(kwargs)
    self.W = np.matrix(w)
    self.b = np.transpose( np.matrix(b) )
  
  def __apply(self, Y):
    if self.funcName is 'tansig':  
      return (2 / (1 + np.exp(-2*Y)))-1
    elif self.funcName is 'sigmoid': 
      return (1 / (1 + np.exp(-Y)))
    else:  
      return Y
  
  # Execute the propagation method
  def __call__(self, X):
    B = self.b * np.ones((1, X.shape[1]))
    Y = np.dot(self.W,X)+B
    return self.__apply(Y), Y
  
  # Convert the matrix to the vector ringer type
  def get_w_array(self):
    return np.array(np.reshape(self.W, (1,self.W.shape[0]*self.W.shape[1])))[0]
  
  # Convert the matrix to the vector ringer type
  def get_b_array(self):
    return np.array(np.reshape(self.b, (1,self.b.shape[0]*self.b.shape[1])))[0]



# Base Neural class
class NeuralNetwork(Logger):
  """
    Class Neural will hold the weights and bias information that came
    from tuningtool core format
  """
  def __init__(self, rawDict, logger=None):
    
    Logger.__init__(self, logger=logger)
    self._u = 0.0
    try: #Retrieve nodes information
      self._etbin = rawDict['configuration']['etBin']
      self._etabin= rawDict['configuration']['etaBin']
      self._nodes = rawDict['discriminator']['nodes']
      w = rawDict['discriminator']['weights']
      b = rawDict['discriminator']['bias']
    except KeyError:
      self._logger.fatal("Not be able to retrieve the params from the dictionary")    

    self._nLayers = len(self._nodes)-1
    self._layers  = list()

    for layer in range(self._nLayers):
      W=[]; B=[]
      for count in range(self._nodes[layer]*self._nodes[layer+1]):
         W.append(w.pop(0))
      W=np.array(W).reshape(self._nodes[layer+1], self._nodes[layer]).tolist()
      for count in range(self._nodes[layer+1]):
        B.append(b.pop(0))
      # Create hidden layers
      self._layers.append( Layer(W,B,Layer=layer,funcName='tansig') )
    #Loop over layers


  def __call__(self, input_):
    for layerIdx in range(len(self._nodes) - 1): 
      if layerIdx==0: f,u  = self._layers[layerIdx](input_.T)
      else: f,u = self._layers[layerIdx](f)
    self._u = u.T
    return f.T

  def getOutputBeforeTheActivationFunction(self):
    return self._u

  def get_w_array(self):
    w = np.array([])
    for l in range(len(self._nodes) - 1):
      w = np.concatenate((w,self._layers[l].get_w_array()),axis=0)
    return w

  def get_b_array(self):
    b = np.array([])
    for l in range(len(self._nodes) - 1):
      b = np.concatenate((b,self._layers[l].get_b_array()),axis=0)
    return b

	# Export the discriminator as a raw dictionary
  def toRawObj(self):
    rawDict = dict()
    rawDict['configuration'] = {'etBin':self._etbin, 'etaBin':self._etabin}
    rawDict['discriminator'] = {
    'nodes'     : self._nodes,
    'bias'      : self.get_b_array().tolist(),
    'weights'   : self.get_w_array().tolist()}
    return rawDict 

  # Expert function to rebin the discriminator
  #def rebin(self, etbin, etabin):
  #  self._etbin = etbin
  #  self._etabin= etabin

  @property
  def nodes(self):
    return self._nodes
  
  @property
  def etmin(self):
    return self._etbin[0]
  
  @property
  def etamin(self):
    return self._etabin[0]
  
  @property
  def etmax(self):
    return self._etbin[1]
  
  @property
  def etamax(self):
    return self._etabin[1]

  def checkForCompatibleBinning(self, et, eta):
    if et > self.etmin and et <= self.etmax:
      if eta > self.etamin and eta <= self.etamax:
        return True
    return False





