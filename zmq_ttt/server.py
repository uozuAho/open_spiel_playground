import json
from typing import Dict

import pyspiel
import zmq
import numpy as np
from open_spiel.python.bots import uniform_random


def main():
  run_ttt_server()


def run_ttt_server():
  server = TicTacToeServer("tcp://*:5555")
  print("listening on port 5555")
  server.wait_for_client()
  print('Client connected')
  game = pyspiel.load_game("tic_tac_toe")
  remote_bot = server.get_remote_bot()
  local_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
  state = play_one_game(game, remote_bot, local_bot)
  server.wait_for_disconnect()
  print('done')
  print(state)


class TicTacToeServer:
  def __init__(self, url):
    ctx = zmq.Context()
    self._socket = ctx.socket(zmq.REP)
    self._socket.bind("tcp://*:5555")

  def wait_for_client(self):
    self._socket.recv().decode('UTF-8')
    response = 'Hi! You are player 0.'
    self._socket.send(response.encode('UTF-8'))

  def get_remote_bot(self):
    return RemoteBot(self._socket)

  def wait_for_disconnect(self):
    self._wait_for_request()
    self._send_response({'EXIT': True})
    self._socket.close()

  # todo: this is duped in remote bot. extract a 'string server'?
  def _wait_for_request(self) -> Dict:
    raw_request = self._socket.recv().decode('UTF-8')
    return json.loads(raw_request)

  def _send_response(self, response: Dict):
    raw_response = json.dumps(response)
    self._socket.send(raw_response.encode('UTF-8'))


class RemoteBot(pyspiel.Bot):
  def __init__(self, socket: zmq.Socket):
    pyspiel.Bot.__init__(self)
    self._socket = socket

  def step(self, state):
    # allow any request at this point. Step only finishes when the client
    # requests 'do action'
    action_done = False
    action = None
    while not action_done:
      request = self._wait_for_request()
      response = self._handle_request(state, request)
      self._send_response(response)
      if request['type'] == 'do_action':
        action_done = True
        action = response
    return action

  def _wait_for_request(self) -> Dict:
    raw_request = self._socket.recv().decode('UTF-8')
    return json.loads(raw_request)

  def _send_response(self, response: Dict):
    raw_response = json.dumps(response)
    self._socket.send(raw_response.encode('UTF-8'))

  def _handle_request(self, state, request: Dict):
    if request['type'] == 'legal_actions':
      return self._handle_legal_actions(state)
    if request['type'] == 'do_action':
      return self._handle_do_action(request)
    raise NotImplemented(request)

  def _handle_legal_actions(self, state) -> Dict:
    return {i: a for i, a in enumerate(state.legal_actions())}

  def _handle_do_action(self, request: Dict):
    action = int(request['action'])
    return action


def play_one_game(game, player_1, player_2):
  players = [player_1, player_2]
  state = game.new_initial_state()

  while not state.is_terminal():
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    action = current_player.step(state)
    state.apply_action(action)

  return state


if __name__ == "__main__":
  main()
