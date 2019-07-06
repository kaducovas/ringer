__all__ = ['StatusCode']


class StatusObj(object):

  _status = 1

  def __init__(self, sc):
    self._status = sc

  def isFailure(self):
    if self._status < 1:
      return True
    else:
      return False

  def __eq__(self, a, b):
    if a.status == b.status:
      return True
    else:
      return False

  def __ne__(self, a, b):
    if a.status != b.status:
      return True
    else:
      return False

  @property
  def status(self):
    return self._status


class StatusCode(object):
  """
    The status code of something
  """

  SUCCESS = StatusObj(1)
  FAILURE = StatusObj(0)
  FATAL   = StatusObj(-1)

