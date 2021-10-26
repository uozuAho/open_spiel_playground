import json
import random
from typing import Dict

import zmq


def main():
  bot = ClientBot()
  bot.connect("tcp://localhost:5555")
  bot.run()


class ClientBot:
  def connect(self, server):
    ctx = zmq.Context()
    self._socket = ctx.socket(zmq.REQ)
    self._socket.connect(server)
    # send any message to connect
    self._socket.send('hello'.encode('UTF-8'))
    self._socket.recv()

  def run(self):
    done = False
    while not done:
      actions = self.get_legal_actions()
      if not actions:
        done = True
      else:
        self.do_random_action(actions)

  def get_legal_actions(self) -> Dict:
    request = json.dumps({'type': 'legal_actions'})
    self._socket.send(request.encode('UTF-8'))
    raw_response = self._socket.recv().decode('UTF-8')
    return json.loads(raw_response)

  def do_random_action(self, legal_actions: Dict):
    # todo: actions can just be ints
    action = random.choice(list(legal_actions.values()))
    request = json.dumps({'type': 'do_action', 'action': action})
    self._socket.send(request.encode('UTF-8'))
    self._socket.recv()


if __name__ == "__main__":
  main()
