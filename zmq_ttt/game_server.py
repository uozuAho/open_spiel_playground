import base64
import time
import pickle
from typing import Dict

import pyspiel
from networking import DictServer


class TicTacToeServer:
  def __init__(self, url, game=None):
    self._url = url
    if game is not None:
      self._game = game
    else:
      self._game = pyspiel.load_game("tic_tac_toe")

  def run(self):
    self._server = DictServer(self._url)
    self.serve_until_exit_requested()
    self.close()

  def close(self):
    # hack: give some time for the client to close. otherwise tests hang
    time.sleep(0.1)
    self._server.close()

  def serve_until_exit_requested(self):
    done = False
    while not done:
      request = self._server.recv()
      response = self._handle_request({}, request)
      self._server.send(response)
      if request['type'] == 'EXIT':
        done = True

  # todo: remove state
  def _handle_request(self, state, request: Dict):
    if request['type'] == 'apply_action':
      return self._handle_apply_action(request)
    if request['type'] == 'game_type':
      return self._handle_game_type()
    if request['type'] == 'game_info':
      return self._handle_game_info()
    if request['type'] == 'new_initial_state':
      return self._handle_new_initial_state()
    if request['type'] == 'EXIT':
      return self._handle_exit()
    raise RuntimeError(f'unknown request: {request["type"]}')

  def _handle_apply_action(self, request: Dict):
    state = pickle.loads(base64.b64decode(request['state_str']))
    state.apply_action(request['action'])
    return self._state_as_dict(state)

  def _state_as_dict(self, state):
    return {
      # state_str: A string that the server can use to rebuild the state.
      #            Clients need to store this for searching game graphs.
      'state_str': base64.b64encode(pickle.dumps(state)).decode('UTF-8'),
      'current_player': state.current_player(),
      'legal_actions': state.legal_actions(),
      'is_terminal': state.is_terminal(),
      'is_chance_node': state.is_chance_node(),
      'returns': state.returns(),
      'pretty_str': str(state)
    }

  def _handle_game_type(self):
    # todo: return all info as dictionary
    game_type = self._game.get_type()
    return {
      'reward_model': 'terminal'
    }

  def _handle_game_info(self):
    return {
      'max_utility': self._game.max_utility(),
      'min_utility': self._game.min_utility()
    }

  def _handle_new_initial_state(self):
    state = self._game.new_initial_state()
    return self._state_as_dict(state)

  def _handle_exit(self):
    return "bye!"
