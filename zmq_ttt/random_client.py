import json
import random
from typing import Dict

import zmq


def main():
  bot = ClientBot()
  bot.connect("tcp://localhost:5555")
  bot.run()
  bot.disconnect()


class ClientBot:
  def connect(self, url):
    self._client = DictClient(url)
    # send any message to connect
    self._client.send({})
    self._client.recv()

  def run(self):
    done = False
    while not done:
      actions = self.get_legal_actions()
      if not actions:
        done = True
      else:
        self.do_random_action(actions)

  def disconnect(self):
    self._client.close()

  def get_legal_actions(self) -> Dict:
    self._client.send({'type': 'legal_actions'})
    response = self._client.recv()
    if 'EXIT' in response:
      return None
    return response

  def do_random_action(self, legal_actions: Dict):
    # todo: actions can just be ints
    action = random.choice(list(legal_actions.values()))
    self._client.send({'type': 'do_action', 'action': action})
    self._client.recv()


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


if __name__ == "__main__":
  main()
