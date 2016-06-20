"""
  Support for 1-wire Dallas DS18B20 temperature sensor using owlserver
"""
from db import dbObject
from datetime import datetime

class Sensor(dbObject):
  base = '/sys/bus/w1/devices/'
  suffix = '/w1_slave'

  def __init__(self, **kwargs):
    super(Sensor, self).__init__()
    if 'id' in kwargs:
      self.load(kwargs['id'])

  def read(self):
    fname = self.base + self.busid + self.suffix
    with open(fname) as f:
      for line in f:
        if 't=' in line:
          temp = line[27:].strip()
          int_part = temp[2:-3]
          dec_part = temp[-3:]
          self.value = float(int_part + '.' + dec_part)
          self._changed.append('value')
          self.save()
          return self.value

  def age(self):
    now = datetime.now()
    diff = now - self.last_checked
    return diff.total_seconds()

if __name__ == '__main__':
  s = Sensor(id=1)
  print s.read()
  s.save()
  s.load(1)
  print s.__dict__
