import math

import numpy as np
import pyspiel
from open_spiel.python.bots import uniform_random
from open_spiel.python.algorithms import mcts

from networking import DictClient

DEBUG=False


def dbg_print(message):
  if DEBUG:
    print(message)


class NetworkBot:
  def __init__(self, bot_builder, url):
    self._bot_builder = bot_builder
    self._url = url

  def run(self):
    self._client = DictClient(self._url)
    game = NetworkGame(self._client)
    state = NetworkState(self._client)
    self._bot = self._bot_builder(game)
    while True:
      dbg_print('client a')
      action = self._bot.step(state)
      dbg_print('client b')
      new_state = state.step(action)
      dbg_print('client c')
      if 'GAME_OVER' in new_state:
        dbg_print('client game over')
        state = NetworkState(self._client)
      if 'EXIT' in new_state:
        dbg_print('client exit received')
        break

  def disconnect(self):
    self._client.close()


class NetworkGame:
  """ Implements an OpenSpiel game, that is usable by existing OpenSpiel bots """
  def __init__(self, client: DictClient):
      self._client = client

  def get_type(self):
    type = self._client.send({'type': 'game_type'})

    # reward model: I think only 2 are available: https://github.com/deepmind/open_spiel/blob/24371dd6983331a0390df68c8511f99a9e76dacf/open_spiel/spiel.h#L101
    reward_model = pyspiel.GameType.RewardModel.REWARDS
    if type['reward_model'] == 'terminal':
      reward_model = pyspiel.GameType.RewardModel.TERMINAL

    # todo: serialize required parameters for building pyspiel.GameType
    # this is a shortcut for now:
    return pyspiel.GameType(
      short_name="python_tic_tac_toe",
      long_name="Python Tic-Tac-Toe",
      dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
      chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
      information=pyspiel.GameType.Information.PERFECT_INFORMATION,
      utility=pyspiel.GameType.Utility.ZERO_SUM,
      reward_model=reward_model,
      max_num_players=2,
      min_num_players=2,
      provides_information_state_string=True,
      provides_information_state_tensor=False,
      provides_observation_string=True,
      provides_observation_tensor=True,
      parameter_specification={})

  def max_utility(self):
    info = self._client.send({'type': 'game_info'})
    return info['max_utility']


class NetworkState:
  """ Implements an OpenSpiel state, that is usable by existing OpenSpiel bots """
  def __init__(self, client: DictClient, state=None):
      self._client = client
      self._state = state

  def clone(self):
    return NetworkState(self._client, self._state)

  def current_player(self):
    return self._get_state()['current_player']

  def legal_actions(self, player_id: int=0):
    # todo: implement player_id
    return self._get_state()['legal_actions']

  def is_terminal(self):
    return self._get_state()['is_terminal']

  def is_chance_node(self):
    return self._get_state()['is_chance_node']

  def returns(self):
    return self._get_state()['returns']

  def step(self, action: int):
    dbg_print('client step')
    # note: 'step' isn't part of an OpenSpiel state, but we need a way of
    # indicating to the server that this is a 'real' action, not part of a
    # simulation.
    # todo: handle 64 bit action integers. JSON doesn't support 64 bit ints.
    self._state = self._client.send({
      'type': 'step',
      'action': int(action)})

    return self._state

  def apply_action(self, action: int):
    """ Ask the server to apply the given action to the given state """
    dbg_print(f'client apply action {action}')
    # todo: handle 64 bit action integers. JSON doesn't support 64 bit ints.
    self._state = self._client.send({
      'type': 'apply_action',
      'action': int(action),
      'state_str': self._state['state_str']})

  def _get_state(self):
    if not self._state:
      self._state = self._client.send({'type': 'get_state'})
    return self._state
