
from socket import socket, AF_INET, SOCK_STREAM
import json


remote = socket( AF_INET, SOCK_STREAM)


def connect_to( remote_host):
  remote.connect( (remote_host, 8978) )


class Error( Exception):
  def __init__( self, code, message, data):
    self.code = code
    self.message = message
    self.data = data

  def __str__( self):
    return "phone.Error( code:%s, message:%s, data:%s)"% ( code, message, str(data))


def rpc_invoke( method_name, params=[]):
  request = {"jsonrpc":"2.0", "id":1, "method":method_name, "params":params }
  request_as_json = json.dumps( request)
  print "  >> %s"% request_as_json
  remote.send( request_as_json)
  # FIXME: This is well crude:
  buf = ""
  while not "\n" in buf:
    buf += remote.recv( 2048)
  response_as_json = buf
  print "  << %s"% response_as_json
  response = json.loads( response_as_json)
  if "error" in response:
    error = response["error"]
    raise Error( error["code"], error["message"], error["data"] )
  return response["result"]


# Meta programming would be nice here:

def cpu_frequency():
  return rpc_invoke("cpu_frequency")

def memory_usage():
  return rpc_invoke("memory_usage")

def battery_level():
  return rpc_invoke("battery_level")

def temperature():
  return rpc_invoke("temperature")

def rild_size():
  return rpc_invoke("rild_size")

def restart_rild():
  return rpc_invoke("restart_rild")

