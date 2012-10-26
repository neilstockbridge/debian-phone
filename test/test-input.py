#!/usr/bin/env python
#
# Use:
#  test-input.py  /dev/input/event0
#
# ..then twiddle your input devices until an event is read and emitted
#

import sys
import struct

Event_format = "llHHi"
sizeof_Event = struct.calcsize( Event_format)

f = open( sys.argv[1])
packed_event = f.read( sizeof_Event)
tv_sec, tv_usec, evtype, code, value = struct.unpack( Event_format, packed_event)
time = float(tv_sec) + float(tv_usec)/1000000.0
print "time:%s, type:%i, code:%i, value:%i" % ( time, evtype, code, value)
f.close()

