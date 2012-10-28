
import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"features")))
if cmd_subfolder not in sys.path:
  sys.path.insert( 0, cmd_subfolder)

import cpu, memory, battery, backlight
from glob import glob
from os import kill
from signal import SIGTERM
from core import contents_of, write_to_file


def cpu_frequency():
  return cpu.frequency()

# Provides a simplified view of memory usage.  Return a 5-tuple with elements:
#
#  - RAM installed
#  - RAM in use ( by applications directly)
#  - RAM idle ( installed - in_use+idle will be less than total.  the
#               difference is buffers and cache)
#  - amount of swap configured
#  - amount of swap in use
#
# All values are reported in MB.
#
def memory_usage():
  total, free, buffers, cached, swap_total, swap_free = memory.usage()
  idle = free
  in_use = total - ( idle + buffers + cached)
  swap_in_use = swap_total - swap_free
  return [ v >> 10 for v in [ total, in_use, idle, swap_total, swap_in_use] ]

def battery_level():
  return battery.level()

def backlight_brightness():
  return backlight.brightness()

def set_backlight_brightness( level):
  backlight.set_brightness( level)

def temperature():
  return battery.temperature()

# My rild has a memory leak, although I don't want it restarted automatically
# because I might be using the phone.
#
write_to_file( str(1), "/var/run/rild.pid")

def rild_pid():
  # Shared code:
  belongs_to_rild = lambda fn: contents_of( fn).startswith("/system/bin/rild")
  try:
    last_known_pid = int( contents_of("/var/run/rild.pid") )
  except IOError:
    last_known_pid = 1
  # If rild no longer has a process ID of last_known_pid:
  if not belongs_to_rild("/proc/%i/cmdline"%last_known_pid):
    # find rild:
    for fn in glob("/proc/*/cmdline"):
      if belongs_to_rild( fn):
        last_known_pid = int( fn.split("/")[2] )
        write_to_file( str(last_known_pid), "/var/run/rild.pid")
  return last_known_pid

def rild_size():
  f = open("/proc/%i/status"%rild_pid() )
  for line in f:
    if line.startswith("VmSize:"):
      size = int( line.split()[1] ) >> 10
      break
  f.close()
  return size

def restart_rild():
  kill( rild_pid(), SIGTERM)
  # It will be restarted auto by init

