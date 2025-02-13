# proof of concept: play chess via a zmq request-response interface

import textwrap

import pyspiel
import chess
import zmq


def main():
  ctx = zmq.Context()
  socket = ctx.socket(zmq.REP)
  socket.bind("tcp://*:5555")
  print("listening on port 5555")
  run_chess_server(socket)


def how_to_play():
  return textwrap.dedent("""
      s:      show the current state
      a:      show legal actions
      number: perform the corresponding action
      q:      quit
  """)


def run_chess_server(socket):
  game = pyspiel.load_game("chess")
  state = game.new_initial_state()
  done = False
  while not done:
    req = socket.recv().decode('UTF-8')
    if req == 's':
      response = str(chess.Board(str(state)))
    elif req == 'a':
      response = legal_actions_msg(state)
    elif req == 'q':
      response = 'bye!'
      done = True
    else:
      try:
        action_num = int(req)
        action = int_to_action(state, action_num)
        state.apply_action(action)
        response = str(chess.Board(str(state)))
      except ValueError:
        response = how_to_play()
    socket.send(response.encode('UTF-8'))


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
