
from core import contents_of


def frequency():
  return int( contents_of("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") ) >> 10

