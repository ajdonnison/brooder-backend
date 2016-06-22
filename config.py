"""
  Configuration from the database
"""

from db import dbObject
from temp import Sensor
from datetime import datetime, timedelta
import re

class Config(dbObject):
  def __init__(self):
    super(Config, self).__init__()
    self.load(False)

  def compareTemp(self, temp1, temp2, direction):
    if direction:
      factor = 0
    else:
      factor = 1
    if temp1 > temp2:
      return False
    else:
      return temp1 < (temp2 - self.hysterisis * factor)

  def compareRaw(self, temp, compare_temp, direction):
    return self.compareTemp(temp, compare_temp, direction)

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

  def compareRampedTemp(self, temp, cycle_start, direction):
    return self.compareTemp(temp, self.rampedTemp(cycle_start), direction)

  def compareDefaultTemp(self, temp, direction):
    return self.compareTemp(temp, self.temp_high, direction)

  def compareTime(self):
    now = datetime.now()
    current_time = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    return current_time > self.time_start and current_time < self.time_end

  def read(self):
    sensor = Sensor(id=self.reference)
    return sensor.read()

  def convertTime(self, value):
    match = re.match(u'(?P<hour>[0-9]+)((:(?P<minute>[0-9]+))?(:(?P<second>[0-9]+))?)?', value)
    if match:
      matchset = {}
      if match.group('hour'):
        matchset['hours'] = int(match.group('hour'))
      if match.group('minute'):
        matchset['minutes'] = int(match.group('minute'))
      if match.group('second'):
        matchset['seconds'] = int(match.group('second'))
      return timedelta(**matchset)

  def setValueFromForm(self, field, value):
    if field not in self.__dict__:
      return False
    if field[:5] == 'time_':
      # Handle time conversion
      val = self.convertTime(value)
    elif field == 'reference' or field == 'cycle_offset':
      val = int(value)
    else:
      val = float(value)
    if self.__dict__[field] != val:
      self._changed.append(field)
      setattr(self, field, val)
      return True
    return False

if __name__ == '__main__':
  c = Config()
  print c.__dict__

