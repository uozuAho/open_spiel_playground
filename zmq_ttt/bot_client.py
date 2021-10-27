import numpy as np
from open_spiel.python.bots import uniform_random

from networking import DictClient


def main():
  random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
  bot = ClientBot(random_bot)
  try:
    bot.connect("ipc:///tmp/ttt")
    bot.run()
  finally:
    bot.disconnect()


class ClientBot:
  def __init__(self, bot):
    self._bot = bot

  def connect(self, url):
    self._client = DictClient(url)
    # send any message to connect
    self._client.send({})

  def run(self):
    state = RemoteState(self._client)
    while True:
      action = self._bot.step(state)
      state.apply_action(action)

  def disconnect(self):
    self._client.close()


class RemoteState:
  def __init__(self, client: DictClient):
      self._client = client

  def legal_actions(self, player_id: int):
    # todo: use player id
    return self._client.send({'type': 'legal_actions'})

  def apply_action(self, action: int):
    # todo: handle 64 bit action integers. JSON doesn't support 64 bit ints,
    # which is what is currently used to serialise messages.
    self._client.send({'type': 'do_action', 'action': int(action)})


if __name__ == "__main__":
  main()
