
import json_rpc


path_to_file = "/sys/class/leds/lcd-backlight/brightness"


def brightness():
  with open( path_to_file) as f: brightness = int( f.read() )
  return brightness


def set_brightness( level):
  if not isinstance( level, int) or level < 0 or 255 < level:
    raise json_rpc.Error( -32602, "Invalid params", "level must be a integer between 0 and 255")
  f = open( path_to_file, "w")
  f.write( str(level) )
  f.close()

