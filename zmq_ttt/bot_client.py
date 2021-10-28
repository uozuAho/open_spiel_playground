import math

import numpy as np
import pyspiel
from open_spiel.python.bots import uniform_random
from open_spiel.python.algorithms import mcts

from networking import DictClient


def main():
  # random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
  client = DictClient("ipc:///tmp/ttt")
  game = RemoteGame(client)
  mcts_bot = mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      max_simulations=2,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=1))
  # bot = BotClient(random_bot)
  bot = BotClient(mcts_bot)
  try:
    bot.connect("ipc:///tmp/ttt")
    bot.run()
  finally:
    bot.disconnect()


class BotClient:
  def __init__(self, bot):
    self._bot = bot

  def connect(self, url):
    self._client = DictClient(url)

  def run(self):
    state = RemoteState(self._client)
    while True:
      action = self._bot.step(state)
      state.apply_action(action)

  def disconnect(self):
    self._client.close()


class RemoteGame:
  """ Implements an OpenSpiel game, that is usable by existing OpenSpiel bots """
  def __init__(self, client: DictClient):
      self._client = client

  def get_type(self):
    type = self._client.send({'type': 'game_type'})

    print(type)

    # reward model: I think only 2 are available: https://github.com/deepmind/open_spiel/blob/24371dd6983331a0390df68c8511f99a9e76dacf/open_spiel/spiel.h#L101
    reward_model = pyspiel.GameType.RewardModel.REWARDS
    if type['reward_model'] == 'terminal':
      reward_model = pyspiel.GameType.RewardModel.TERMINAL

    return pyspiel.GameType(reward_model=reward_model)


class RemoteState:
  """ Implements an OpenSpiel state, that is usable by existing OpenSpiel bots """
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
