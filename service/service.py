#!/usr/bin/env python

import socket
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, error
import json_rpc

bind_to_address = "0.0.0.0"
listen_on_port = 8978

s = socket( AF_INET, SOCK_STREAM)
s.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1)
s.bind( (bind_to_address, listen_on_port) )
s.listen( 5) # 5 is how many conns to queue while busy

while True:
  print "Listing on %s, port %i" % ( bind_to_address, listen_on_port)
  conn, addr = s.accept()
  print "Incoming:", addr[0]
  while True:
    try: request_as_json = conn.recv( 2048)
    except error: break
    if not request_as_json: break
    print "  << ", request_as_json
    response_as_json = json_rpc.response_to( request_as_json)
    print "  >> ", response_as_json
    conn.send( response_as_json)
    conn.send("\r\n")
  conn.close()

