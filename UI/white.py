#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import platform
ON_PHONE = platform.node() != "neils-laptop"
# SHOULD_CONNECT = False allows some development without connecting to the phone service
SHOULD_CONNECT = True

import sys, pygame, phone
from os import environ
environ["SDL_NOMOUSE"] = "1"
if ON_PHONE: import input_fix
from pygame import KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from time import localtime, strftime
from time import time
from textbox import TextBox
from keyboard import OnScreenKeyboard

black = 0, 0, 0
white = 255, 255, 255

smooth_fonts = True

pygame.display.init()
pygame.font.init()

resolution = (240, 320) # Can leave this off for the phone but it required when running this on the desktop
screen = pygame.display.set_mode( resolution)
screen_dimensions = screen.get_rect()

battery_frames = pygame.image.load("battery.png")

#print pygame.font.get_fonts()
droid10 = pygame.font.Font("DroidSans-Bold.ttf", 10)
droid20 = pygame.font.Font("DroidSans-Bold.ttf", 20)
#print droid10.get_linesize()


keyboard = OnScreenKeyboard( screen_dimensions, droid20)
textbox = TextBox( droid20)


class State:

  def __init__( self):
    self.when_last_updated = 0
    self.when_last_updated_slow = 0


  def update( self):
    now = int( time() )

    if self.when_last_updated + 1 < now:
      self.when_last_updated = now
      self.cpu_frequency = phone.cpu_frequency()
      self.temperature = phone.temperature()
      self.memory_usage = phone.memory_usage()

    # Infrequently changing state should be updated less often
    if self.when_last_updated_slow + 60 < now:
      self.when_last_updated_slow = now
      print "update slow"
      self.battery_level = phone.battery_level()
      self.rild_size = phone.rild_size()


def write( text, coords):
  surf = droid10.render( text, smooth_fonts, black, white)
  screen.blit( surf, coords)
  #print "dims of %s: %s"% ( text, surf.get_rect() )


def render( state):

  screen.fill( white)

  formatted_time = strftime( "%I:%M%p", localtime() )
  if formatted_time.startswith("0"): formatted_time = formatted_time[1:]
  write( formatted_time.lower(), (screen_dimensions.w - 40, 0))

  if SHOULD_CONNECT:
    if 50 < state.battery_level: frame = 0
    elif 20 < state.battery_level: frame = 1
    else: frame = 2
    screen.blit( battery_frames, (screen_dimensions.w - 50,0), (8*frame,0,8,12))

    write("%i MHz"%state.cpu_frequency, (10,0) )

    write(u"%i°C"%state.temperature, (60,0) )

    write("r:%iM"%state.rild_size, (90,0) )

    total, in_use, idle, swap_total, swap_in_use = state.memory_usage
    write("i:%iM"%idle, (120,0) )

  # panel?: list of objects that know how to render themselves

  keyboard.render_to( screen)
  textbox.render_to( screen)


state = State()
if SHOULD_CONNECT: phone.connect_to("vf845")

clock = pygame.time.Clock()

while True:
  clock.tick( 10)
  if SHOULD_CONNECT: state.update()
  if ON_PHONE: input_fix.poll_inputs( screen)
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if event.type == KEYUP and event.key in [pygame.K_ESCAPE, pygame.K_q]: sys.exit()
    if event.type in [ MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
      # TODO: Will really need to be able to deliver the mouse event to a "widget"
      x, y = event.pos
      if y > keyboard.top:
        row = ( y - keyboard.top) / keyboard.key_h
        col = ( x - keyboard.rows[row].left) / keyboard.key_w
        key = keyboard.rows[row].keys[ col]
        if event.type == MOUSEBUTTONDOWN:
          keyboard.key_held = key
          post_type = KEYDOWN
        else:
          # Check to see if the pointer was dragged before being lifted:
          if key == keyboard.key_held:
            post_type = KEYUP
        if post_type != None:
          pygame.event.post( pygame.event.Event( post_type, scancode=0, key=ord(key), mod=0) )
      #print event.pos
    if KEYUP == event.type:
      #print "  released", event.key
      if 32 <= event.key and event.key <= 127:
        textbox.insert( chr(event.key) )
      if pygame.K_LEFT == event.key:
        if 0 < textbox.cursor: textbox.cursor -= 1
      elif pygame.K_RIGHT == event.key:
        if textbox.cursor < len(textbox.text): textbox.cursor += 1
      elif pygame.K_BACKSPACE == event.key:
        textbox.delete()
      #print event
  #phone.restart_rild

  render( state)
  pygame.display.flip()

