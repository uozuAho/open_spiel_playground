import base64
from datetime import datetime
import pickle
from typing import Dict, List

import pyspiel
import numpy as np
from open_spiel.python.bots import uniform_random
from networking import DictServer


def main():
  # serve_one_game()
  # measure_games_per_second()
  server = TicTacToeServer("ipc:///tmp/ttt")
  # server.serve_one_game()
  server.measure_games_per_second()


class TicTacToeServer:
  def __init__(self, url):
    self._server = DictServer(url)
    self._game = pyspiel.load_game("tic_tac_toe")

  def serve_one_game(self):
    local_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    self.play_one_game(local_bot)
    self.wait_for_disconnect()
    print('done')
    print(self._state)

  def measure_games_per_second(self):
    local_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    last = datetime.now()
    num_games = 0
    while True:
      self.play_one_game(local_bot)
      num_games += 1
      if (datetime.now() - last).total_seconds() > 1:
        print(f'{num_games} games/sec')
        num_games = 0
        last = datetime.now()

  def play_one_game(self, opponent):
    self._state = self._game.new_initial_state()

    players = [self, opponent]

    while not self._state.is_terminal():
      current_player_idx = self._state.current_player()
      current_player = players[current_player_idx]
      action = current_player.step(self._state)
      self._state.apply_action(action)

  def get_remote_bot(self):
    return self

  def wait_for_disconnect(self):
    self._server.recv()
    self._server.send({'EXIT': True})
    self._server.close()

  def step(self, state):
    # allow any request at this point. Step only finishes when the client
    # requests 'do action'
    action_done = False
    action = None
    while not action_done:
      request = self._server.recv()
      response = self._handle_request(state, request)
      self._server.send(response)
      if request['type'] == 'do_action':
        action_done = True
        action = response
    return action

  def _handle_request(self, state, request: Dict):
    if request['type'] == 'legal_actions':
      return self._handle_legal_actions(state)
    if request['type'] == 'do_action':
      return self._handle_do_action(request)
    if request['type'] == 'current_player':
      return self._handle_current_player(state)
    if request['type'] == 'get_state':
      return self._handle_get_state(state)
    if request['type'] == 'game_type':
      return self._handle_game_type()
    if request['type'] == 'game_info':
      return self._handle_game_info()
    raise RuntimeError(f'unknown request: {request["type"]}')

  def _handle_legal_actions(self, state) -> List:
    return state.legal_actions()

  def _handle_do_action(self, request: Dict):
    action = int(request['action'])
    return action

  def _handle_current_player(self, state):
    return state.current_player()

  def _handle_get_state(self, state):
    return {
      # state_str: A string that the server can use to rebuild the state.
      #            Not used by clients.
      'state_str': str(base64.b64encode(pickle.dumps(state))),
      'current_player': state.current_player(),
      'legal_actions': state.legal_actions()
    }

  def _handle_game_type(self):
    return {'reward_model': 'terminal'}

  def _handle_game_info(self):
    return {'max_utility': 1, 'min_utility': -1}


if __name__ == "__main__":
  main()
