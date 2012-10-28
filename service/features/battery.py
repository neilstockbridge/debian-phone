
from core import contents_of


def level():
  return int( contents_of("/sys/class/power_supply/battery/level") )


def temperature():
  t = int( contents_of("/sys/class/power_supply/battery/batt_temp") )
  return t / 10

