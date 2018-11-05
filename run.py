#!/usr/bin/env python

from config import Config
from brooder import Brooder
import time


def BrooderControl():
  brooders = Brooder()
  BrooderList = brooders.loadAll()
  cfg = Config()

  while True:
    for brooder in BrooderList:
      brooder.process()
    cfg.read()
    time.sleep(5)

if __name__ == '__main__':
  BrooderControl()
