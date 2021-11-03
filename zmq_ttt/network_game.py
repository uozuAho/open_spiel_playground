import pyspiel

from networking import DictClient


class NetworkGame:
  """ Implements an OpenSpiel game, that is usable by existing OpenSpiel bots """
  def __init__(self, client, url=None):
      self._client = client
      if url is not None:
        self._client = DictClient(url)

  def new_initial_state(self):
    state = self._client.send({'type': 'new_initial_state'})
    return NetworkState(self._client, state)

  def exit(self):
    self._client.send({'type': 'EXIT'})
    self._client.close()

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
