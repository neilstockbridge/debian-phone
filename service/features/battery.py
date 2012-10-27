
def level():
  f = open("/sys/class/power_supply/battery/level")
  level = int( f.read() )
  f.close()
  return level

