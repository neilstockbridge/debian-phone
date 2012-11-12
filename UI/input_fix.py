#
# This module reads /dev/input/event* and injects SDL events on to the queue,
# for phones where the input events are missing or mangled.
#

from struct import calcsize, unpack
from select import select
from pygame import KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import event as sdl_event
from pygame.event import Event
import pygame


Event_format = "llHHi"
sizeof_Event = calcsize( Event_format)

# A list of open files that correspond to the input devices:
open_files = []
# A map from open file to the state of the input device:
state_for_file = {}

class State:
  def __init__( self):
    self.x = 0
    self.y = 0

devices = {
  "/dev/input/event0": True,   # joypad
  "/dev/input/event1": True,   # touch screen
  "/dev/input/event3": False,  # most buttons
  "/dev/input/event4": False,  # power button
  "/dev/input/event5": False,  # joypad button
}
for path_to_event_file, is_stateful in devices.iteritems():
  f = open( path_to_event_file)
  open_files.append( f)
  if is_stateful:
    state_for_file[ f] = State()
    if "/dev/input/event1" == path_to_event_file: State.for_touchscreen = state_for_file[ f]

EV_SYN = 0x00
EV_KEY = 0x01
EV_REL = 0x02
EV_ABS = 0x03

# These are the hard buttons on the Huawei u8120
BEGIN_CALL_BUTTON  = 231
MENU_BUTTON        = 139
BACK_BUTTON        = 158
BACK_BUTTON_HELD   = 102 # When the Back button is held for a second
END_CALL_BUTTON    =  62
VOLUME_UP_BUTTON   = 115
VOLUME_DOWN_BUTTON = 114
POWER_BUTTON       = 116
OK_BUTTON          = 232

# This is a mapping from button on the phone to the key in SDL
key_for_button = {
  BEGIN_CALL_BUTTON:  pygame.K_F2,
  MENU_BUTTON:        pygame.K_F10,
  BACK_BUTTON:        pygame.K_BACKSPACE,
  BACK_BUTTON_HELD:   pygame.K_END,
  END_CALL_BUTTON:    pygame.K_ESCAPE,
  VOLUME_UP_BUTTON:   pygame.K_PAGEUP,
  VOLUME_DOWN_BUTTON: pygame.K_PAGEDOWN,
  POWER_BUTTON:       pygame.K_POWER,
  OK_BUTTON:          pygame.K_RETURN,
}


def poll_inputs( screen):
  # All pending events should be read with a single invocation of this method
  while True:
    readable, ignore, ignore = select( open_files, [], [], 0)
    if [] == readable: break
    for f in readable:
      packed_event = f.read( sizeof_Event)
      secs, usecs, event_type, code, value = unpack( Event_format, packed_event)
      time = float(secs) + float(usecs)/1000000.0
      #print "t:%i, c:%i, v:%i" % ( event_type, code, value)
      if EV_KEY == event_type:
        #act = "pressed" if 1 == value else "released"
        #print act+ ": %i"% code
        if 330 == code:
          evt = MOUSEBUTTONDOWN if 1 == value else MOUSEBUTTONUP
          state = State.for_touchscreen
          sdl_event.post( Event(evt, pos=(state.x,state.y), button=0) )
          print state.x,state.y
        else:
          evt = KEYDOWN if 1 == value else KEYUP
          sdl_event.post( Event(evt, key=key_for_button[code], unicode="", mod=0) )
      elif EV_REL == event_type:
        # The joypad is mapped to the arrow keys
        state = state_for_file[ f]
        if 0 == code:  # 0 means X axis
          state.x = screen.get_rect().w * value >> 10
          #print "moved to %i,%i"% ( state.x, state.y)
        elif 1 == code:
          state.y = screen.get_rect().h * value >> 10
        #print "moved to %i,%i"% ( state.x, state.y)
      elif EV_ABS == event_type:
        state = state_for_file[ f]
        touchscreen_state = state
        if 0 == code:  # 0 means X axis
          state.x = screen.get_rect().w * value >> 10
          #print "moved to %i,%i"% ( state.x, state.y)
        elif 1 == code:
          state.y = screen.get_rect().h * value >> 10
          #print "moved to %i,%i"% ( state.x, state.y)
        sdl_event.post( Event(MOUSEMOTION, pos = (state.x,state.y), rel = [], buttons = []) )
        #print state.x,state.y

  #KEYDOWN      unicode, key, mod
  #KEYUP      key, mod
  #MOUSEMOTION      pos, rel, buttons
  #MOUSEBUTTONUP    pos, button
  #MOUSEBUTTONDOWN  pos, button
  #JOYAXISMOTION    joy, axis, value
  #JOYBUTTONUP      joy, button
  #JOYBUTTONDOWN    joy, button

