
import json
import api


class Error( Exception):
  def __init__( self, code, message, data=None):
    self.code = code
    self.message = message
    self.data = data


def response_to( request_as_json):

  response = {"jsonrpc":"2.0"}
  try:
    try: request = json.loads( request_as_json)
    except ValueError: raise Error( -32700, "Parse error")

    response["id"] = request["id"]

    try: method = getattr( api, request["method"])
    except AttributeError: raise Error( -32601, "Method not found")

    response["result"] = method( *request["params"])

  except Error, e:
    response["error"] = {"code":e.code, "message":e.message, "data":e.data }

  return json.dumps( response)

