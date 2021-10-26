import json
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
    self._socket.recv().decode('UTF-8')

  def run(self):
    actions = self.get_legal_actions()
    print(actions)

  def get_legal_actions(self) -> Dict:
    request = json.dumps({'type': 'legal_actions'})
    self._socket.send(request.encode('UTF-8'))
    raw_response = self._socket.recv().decode('UTF-8')
    return json.loads(raw_response)


if __name__ == "__main__":
  main()
