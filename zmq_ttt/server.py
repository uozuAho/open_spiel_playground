import pyspiel
import zmq
import numpy as np
from open_spiel.python.bots import uniform_random


def main():
  run_ttt_server()


def run_ttt_server():
  ctx = zmq.Context()
  socket = ctx.socket(zmq.REP)
  socket.bind("tcp://*:5555")
  print("listening on port 5555")
  game = pyspiel.load_game("tic_tac_toe")
  done = False
  while not done:
    req = socket.recv().decode('UTF-8')
    response = 'Hi! You are player 0.'
    print('Client connected')
    state = game.new_initial_state()
    remote_bot = RemoteBot(socket)
    local_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    done = True
  socket.send(response.encode('UTF-8'))


class RemoteBot(pyspiel.Bot):
  def __init__(self, socket: zmq.Socket):
    pyspiel.Bot.__init__(self)
    self._socket = socket


def legal_actions_msg(state):
  msg = ""
  for i, action in enumerate(state.legal_actions()):
    msg += f'  {i}: {action_str(state, action)}\n'
  return msg


def int_to_action(state, int):
  for i, action in enumerate(state.legal_actions()):
    if int == i:
      return action
  raise RuntimeError(f'invalid action number: {int}')


def action_str(state, action):
  return state.action_to_string(state.current_player(), action)


if __name__ == "__main__":
  main()
