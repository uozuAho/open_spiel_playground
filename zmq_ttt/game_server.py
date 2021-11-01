import base64
from datetime import datetime, timedelta
import time
import pickle
from typing import Dict

import pyspiel
import numpy as np
from open_spiel.python.bots import uniform_random
from networking import DictServer


DEBUG=False


def dbg_print(message):
  if DEBUG:
    print(message)


class TicTacToeServer:
  def __init__(self, url):
    self._url = url

  def serve_one_game(self):
    self._server = DictServer(self._url)
    self._game = pyspiel.load_game("tic_tac_toe")
    local_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    self.play_one_game(local_bot)
    print('done')
    print(self._state)
    self.close()

  def close(self):
    # hack: give some time for the client to close. otherwise tests hang
    time.sleep(0.1)
    self._server.close()

  def measure_games_per_second(self, time_limit_s):
    self._server = DictServer(self._url)
    self._game = pyspiel.load_game("tic_tac_toe")
    local_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    end = datetime.now() + timedelta(seconds=time_limit_s)
    last = datetime.now()
    num_games = 0
    local_wins = 0
    remote_wins = 0
    while datetime.now() < end:
      state = self.play_one_game(local_bot, exit=False)
      if state.returns()[0] > 0:
        remote_wins += 1
      else:
        local_wins += 1
      num_games += 1
      if (datetime.now() - last).total_seconds() > 1:
        print(f'{num_games} games/sec. wins: remote: {remote_wins}, local: {local_wins}')
        num_games = 0
        last = datetime.now()
    self.play_one_game(local_bot, exit=True)
    self.close()

  def play_one_game(self, local_player, exit=True):
    dbg_print('qwer')
    self._state = self._game.new_initial_state()

    remote_player = self  # this is confusing...
    players = [remote_player, local_player]
    remote_is_waiting = False

    while not self._state.is_terminal():
      dbg_print('s')
      current_player_idx = self._state.current_player()
      current_player = players[current_player_idx]
      if current_player is remote_player:
        dbg_print('remote turn')
        if remote_is_waiting:
          dbg_print('send state')
          self._server.send(self._state_as_dict(self._state))
          remote_is_waiting = False
        action = self.serve_until_step_requested(self._state)
        remote_is_waiting = True
      else:
        dbg_print('server turn')
        action = current_player.step(self._state)
      self._state.apply_action(action)

    if remote_is_waiting:
      if exit:
        dbg_print('server send exit')
        self._server.send({'EXIT': True})
      else:
        self._server.send({'GAME_OVER': True})

    return self._state

  def serve_until_step_requested(self, state):
    action_done = False
    action = None
    while not action_done:
      request = self._server.recv()
      response = self._handle_request(state, request)
      if request['type'] == 'step':
        action_done = True
        action = response
      else:
        self._server.send(response)
    return action

  def _handle_request(self, state, request: Dict):
    if request['type'] == 'apply_action':
      return self._handle_apply_action(request)
    if request['type'] == 'step':
      return self._handle_step(request)
    if request['type'] == 'get_state':
      return self._handle_get_state(state)
    if request['type'] == 'game_type':
      return self._handle_game_type()
    if request['type'] == 'game_info':
      return self._handle_game_info()
    raise RuntimeError(f'unknown request: {request["type"]}')

  def _handle_apply_action(self, request: Dict):
    state = pickle.loads(base64.b64decode(request['state_str']))
    state.apply_action(request['action'])
    return self._state_as_dict(state)

  def _handle_step(self, request: Dict):
    action = int(request['action'])
    return action

  def _handle_get_state(self, state):
    return self._state_as_dict(state)

  def _state_as_dict(self, state):
    return {
      # state_str: A string that the server can use to rebuild the state.
      #            Not used by clients.
      'state_str': base64.b64encode(pickle.dumps(state)).decode('UTF-8'),
      'current_player': state.current_player(),
      'legal_actions': state.legal_actions(),
      'is_terminal': state.is_terminal(),
      'is_chance_node': state.is_chance_node(),
      'returns': state.returns()
    }

  def _handle_game_type(self):
    return {'reward_model': 'terminal'}

  def _handle_game_info(self):
    return {'max_utility': 1, 'min_utility': -1}
