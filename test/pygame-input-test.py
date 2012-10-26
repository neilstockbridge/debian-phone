#!/usr/bin/env python
#
# Check if pygame is returning the correct input events for your phone.
#
# The Huawei u8120 ignored the joystick and touchscreen ( although didn't try
# TSLIB) and additionally the keys were wrong:
#
#  + Begin Call   'scancode': 0, 'key': 0
#  + Menu         'scancode': 0, 'key': 0
#  + Back         'scancode': 0, 'key': 0
#  + End Call:    'scancode': 62, 'key': 285
#  + Volume Up:   'scancode': 115, 'key': 0
#  + Volume Down: 'scancode': 114, 'key': 0
#  + Power:        no event
#  + OK:          'scancode': 116, 'key': 0
#

import pygame

pygame.display.init()
pygame.display.set_mode()

print "Waiting for events.."
while True:
  for event in pygame.event.get():
    print event

