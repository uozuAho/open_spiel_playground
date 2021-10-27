import random
from typing import Dict

from networking import DictClient


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


if __name__ == "__main__":
  main()
