# proof of concept: play chess via a zmq interface

import pyspiel
import chess
import zmq


def main():
  ctx = zmq.Context()
  socket = ctx.socket(zmq.REP)
  socket.bind("tcp://*:5555")
  print("listening on port 5555")
  run_chess_server(socket)


def run_chess_server(socket):
  game = pyspiel.load_game("chess")
  state = game.new_initial_state()
  done = False
  while not done:
    recv_msg = socket.recv()
    msg = str(chess.Board(str(state)))
    socket.send(msg.encode('UTF-8'))
    done = True


def run_chess_serverasdf(socket):
  game = pyspiel.load_game("chess")
  state = game.new_initial_state()
  while not state.is_terminal():
    msg = chess.Board(str(state))
    legal_actions = state.legal_actions()
    action = get_action_from_user(state, legal_actions)
    print("current player: ", state.current_player())
    print("action: ", state.action_to_string(state.current_player(), action))
    state.apply_action(action)
  print('game over!')


def get_action_from_user(state, legal_actions):
  print('choose an action:')
  for i, action in enumerate(legal_actions):
    print('  ', i, action_str(state, action))
  user_choice = int(input())
  for i, action in enumerate(legal_actions):
    if user_choice == i:
      return action
  raise RuntimeError('oops!')


def action_str(state, action):
  return state.action_to_string(state.current_player(), action)


if __name__ == "__main__":
  main()
