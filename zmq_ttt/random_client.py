import random
from typing import Dict, List

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

  def get_legal_actions(self) -> List:
    response = self._client.send({'type': 'legal_actions'})
    if 'EXIT' in response:
      return None
    return response

  def do_random_action(self, legal_actions: List):
    action = random.choice(legal_actions)
    self._client.send({'type': 'do_action', 'action': action})


if __name__ == "__main__":
  main()
