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

  def recv(self) -> Dict:
    raw_message =  self._socket.recv().decode('UTF-8')
    return json.loads(raw_message)

  # todo: make this receive a response. no need for a separate recv
  def send(self, message: Dict):
    json_message = json.dumps(message)
    self._socket.send(json_message.encode('UTF-8'))

  def close(self):
    self._socket.close()
