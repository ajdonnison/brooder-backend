"""
  Abstraction of the Brooder object
"""
from temp import Sensor
from datetime import datetime
import RPi.GPIO as GPIO
from db import dbObject
from config import Config

class Brooder(dbObject):
  def __init__(self, **kwargs):
    super(Brooder, self).__init__()
    if 'id' in kwargs:
      self.load(kwargs['id'])
      self.initPins()

  def initPins(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([self.light, self.heater], GPIO.OUT, initial=GPIO.LOW)

  """
    Read the temperature, and compare against the required temp.
  """
  def process(self):
    config = Config()
    self.load(self.id)
    if (self.enabled):
      sensor = Sensor(id=self.sensor)
      temp = sensor.read()
      self.setLight(config.compareTime())
      if self.set_temperature:
        self.setHeater(config.compareRaw(temp, self.set_temperature, self.heater_state))
      elif self.cycle_started:
        self.setHeater(config.compareRampedTemp(temp, self.cycle_started, self.heater_state))
      else:
        self.setHeater(config.compareDefaultTemp(temp, self.heater_state))
      # print "{name}: {temp}T {heater}H {light}L".format(name=self.name, temp=temp, heater=self.heater_state, light=self.light_state)
    else:
      self.setHeater(False)
      self.setLight(False)
    self.save()

  def setLight(self, state):
    if self.light_state != state:
      self._changed.append('light_state')
    self.light_state = state
    GPIO.output(self.light, state)

  def loadAll(self):
    result = super(Brooder, self).loadAll()
    for brooder in result:
      brooder.initPins()
    return result

  def listAll(self):
    result = super(Brooder, self).loadAll()
    for brooder in result:
      brooder._sensor = Sensor(id=brooder.sensor)
    return result

  def setHeater(self, state):
    if self.heater_state != state:
      self._changed.append('heater_state')
    self.heater_state = state
    GPIO.output(self.heater, state)

  def setEnabled(self, state):
    self._changed.append('enabled')
    self.enabled = state
    self.save()

  def setCycle(self, state):
    self._changed.append('cycle_enabled')
    if state:
      self._changed.append('cycle_started')
      self.cycle_started = datetime.now()
      if self.set_temperature:
        self.set_temperature = None
        self._changed.apped('set_temperature')
    self.cycle_enabled = state
    self.save()

  def setTemperature(self, value):
    self._changed.append('set_temperature')
    if self.cycle_enabled:
      self._changed.append('cycle_enabled')
      self.cycle_enabled = False
    self.set_temperature = float(value)
    self.save()
      
  def setDefault(self):
    if self.set_temperature:
      self.set_temperature = None
      self._changed.append('set_temperature')
    if self.cycle_enabled:
      self.cycle_enabled = False
      self._changed.appedn('cycle_enabled')
    self.save()

  def status(self):
    result = super(Brooder, self).status()
    sensor = Sensor(id=self.sensor)
    result['sensor'] = sensor.status()
    return result

if __name__ == '__main__':
  c = Brooder(1)
  temp = c.process()
  print temp
  print c.last_checked
