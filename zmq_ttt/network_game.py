import pyspiel

from networking import DictClient


class NetworkGame:
  """ Presents an OpenSpiel Game interface, proxying requests to a remote game
      server.
  """
  def __init__(self, url):
    self._client = DictClient(url)

  def new_initial_state(self):
    state = self._client.send({'type': 'new_initial_state'})
    return NetworkState(self._client, state)

  def exit(self):
    self._client.send({'type': 'EXIT'})
    self._client.close()

  def get_type(self):
    type = self._client.send({'type': 'game_type'})

    # see https://github.com/deepmind/open_spiel/blob/master/open_spiel/spiel.h
    # GameType for the values of these fields
    return pyspiel.GameType(
      short_name = type['short_name'],
      long_name = type['long_name'],
      dynamics = pyspiel.GameType.Dynamics(type['dynamics']),
      chance_mode = pyspiel.GameType.ChanceMode(type['chance_mode']),
      information = pyspiel.GameType.Information(type['information']),
      utility = pyspiel.GameType.Utility(type['utility']),
      reward_model = pyspiel.GameType.RewardModel(type['reward_model']),
      max_num_players = type['max_num_players'],
      min_num_players = type['min_num_players'],
      provides_information_state_string = type['provides_information_state_string'],
      provides_information_state_tensor = type['provides_information_state_tensor'],
      provides_observation_string = type['provides_observation_string'],
      provides_observation_tensor = type['provides_observation_tensor'],
      # todo: handle parameter_specification
      parameter_specification={})

  def max_utility(self):
    info = self._client.send({'type': 'game_info'})
    return info['max_utility']


class NetworkState:
  """ Presents an OpenSpiel State interface, proxying requests to a remote game
      server.
  """
  def __init__(self, client: DictClient, state):
      self._client = client
      self._state = state

  def clone(self):
    return NetworkState(self._client, self._state)

  def current_player(self):
    return self._state['current_player']

  def legal_actions(self, player_id: int=0):
    # todo: implement player_id
    return self._state['legal_actions']

  def is_terminal(self):
    return self._state['is_terminal']

  def is_chance_node(self):
    return self._state['is_chance_node']

  def returns(self):
    return self._state['returns']

  def apply_action(self, action: int):
    """ Ask the server to apply the given action to the given state """
    # todo: handle 64 bit action integers. JSON doesn't support 64 bit ints.
    self._state = self._client.send({
      'type': 'apply_action',
      'action': int(action),
      'state_str': self._state['state_str']})

  def __str__(self):
    return self._state['pretty_str']
