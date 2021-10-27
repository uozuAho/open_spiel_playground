import json
import zmq
from typing import Dict


class DictServer:
  """ A request-response server that sends & receives dictionaries.
      Dictionaries are easy to send & receive, as they are just
      encoded as JSON.
  """
  def __init__(self, url):
    ctx = zmq.Context()
    self._socket = ctx.socket(zmq.REP)
    self._socket.bind(url)

  def recv(self) -> Dict:
    """ Blocking wait for a request """
    raw_message =  self._socket.recv().decode('UTF-8')
    return json.loads(raw_message)

  def send(self, message: Dict):
    json_message = json.dumps(message)
    self._socket.send(json_message.encode('UTF-8'))

  def close(self):
    self._socket.close()


class DictClient:
  """ A request-response client that sends & receives dictionaries.
      Dictionaries are easy to send & receive, as they are just
      encoded as JSON.
  """
  def __init__(self, url):
    ctx = zmq.Context()
    self._socket = ctx.socket(zmq.REQ)
    self._socket.connect(url)

  def send(self, message: Dict) -> Dict:
    """ Send a message and blocking wait for a response """
    json_message = json.dumps(message)
    self._socket.send(json_message.encode('UTF-8'))
    raw_message =  self._socket.recv().decode('UTF-8')
    return json.loads(raw_message)

  def close(self):
    self._socket.close()
