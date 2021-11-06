import base64
import time
import pickle
from typing import Dict

from networking import DictServer


class GameServer:
  """ An example game server. Your game server should handle requests in a
      similar fashion to _handle_request.
  """
  def __init__(self, url, game):
    self._url = url
    self._game = game

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
      response = self._handle_request(request)
      self._server.send(response)
      if request['type'] == 'EXIT':
        done = True

  def _handle_request(self, request: Dict):
    """ Handle a request from a game-playing agent """
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
    type = self._game.get_type()
    return {
      "short_name" : type.short_name,
      "long_name" : type.long_name,
      "dynamics" : type.dynamics.value,
      "chance_mode" : type.chance_mode.value,
      "information" : type.information.value,
      "utility" : type.utility.value,
      "reward_model" : type.reward_model.value,
      "max_num_players" : type.max_num_players,
      "min_num_players" : type.min_num_players,
      "provides_information_state_string" : type.provides_information_state_string,
      "provides_information_state_tensor" : type.provides_information_state_tensor,
      "provides_observation_string" : type.provides_observation_string,
      "provides_observation_tensor" : type.provides_observation_tensor,
      'parameter_specification' : type.parameter_specification
    }

  def _handle_game_info(self):
    return {
      'num_distinct_actions' : self._game.num_distinct_actions(),
      'max_chance_outcomes' : self._game.max_chance_outcomes(),
      'num_players' : self._game.num_players(),
      'min_utility' : self._game.min_utility(),
      'max_utility' : self._game.max_utility(),
      'utility_sum' : self._game.utility_sum(),
      'max_game_length' : self._game.max_game_length()
    }

  def _handle_new_initial_state(self):
    state = self._game.new_initial_state()
    return self._state_as_dict(state)

  def _handle_exit(self):
    return "bye!"
