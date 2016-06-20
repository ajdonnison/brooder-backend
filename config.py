"""
  Configuration from the database
"""

from db import dbObject
from temp import Sensor
from datetime import datetime, timedelta

class Config(dbObject):
  def __init__(self):
    super(Config, self).__init__()
    self.load(False)

  def compareTemp(self, temp1, temp2):
    if temp1 > temp2:
      return False
    else:
      return temp1 < (temp2 - self.hysterisis)

  def compareRaw(self, temp, compareTemp):
    return self.compareTemp(temp, compareTemp)

  """
    Ramped temperature depends on the phase of
    the cycle.
  """
  def rampedTemp(self, cycle_start):
    diff = datetime.now() - cycle_start
    days = diff.days - self.cycle_offset
    if days < 0:
      days = 0
    return max(self.temp_high - (days * self.ramp_factor), self.temp_low)

  def compareRampedTemp(self, temp, cycle_start):
    return self.compareTemp(temp, self.rampedTemp(cycle_start))

  def compareDefaultTemp(self, temp):
    return self.compareTemp(temp, self.temp_high)

  def compareTime(self):
    now = datetime.now()
    current_time = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    return current_time > self.time_start and current_time < self.time_end

  def read(self):
    sensor = Sensor(id=self.reference)
    return sensor.read()

if __name__ == '__main__':
  c = Config()
  print c.__dict__
