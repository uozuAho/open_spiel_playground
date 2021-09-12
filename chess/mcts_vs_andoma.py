# Plays a game of chess between an MCTS bot and [Andoma](https://github.com/healeycodes/andoma)

DEBUG=True

import math
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts

import chess
from andoma import andoma_bot as andoma

def main():
  game = pyspiel.load_game("chess")
  state = game.new_initial_state()
  mcts_bot = new_mcts_bot(game)
  andoma_bot = andoma.AndomaBot(search_depth=1)

  players = [mcts_bot, andoma_bot]
  player_labels = ['mcts', 'andoma']

  while not state.is_terminal():
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    if DEBUG:
      print_dbg_state(state, player_labels)
      input("press a key...")
    action = current_player.step(state)
    if DEBUG:
      print_action(state, action)
    state.apply_action(action)

  print(state)
  print(chess.Board(fen=str(state)))
  print_outcome(state, player_labels)


def new_mcts_bot(game, rng=np.random.RandomState()):
  return mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      max_simulations=2,
      random_state=rng,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=1, random_state=rng))


def print_dbg_state(state: pyspiel.State, player_labels):
  current_player_idx = state.current_player()
  print(state)
  print(chess.Board(fen=str(state)))
  print(f'current player ({"W" if current_player_idx == 1 else "b"}): {player_labels[current_player_idx]}')


def print_action(state, action):
  action_str = state.action_to_string(state.current_player(), action)
  print(f'action: {action_str}')


def print_outcome(state: pyspiel.State, player_labels):
  if all((x == 0 for x in state.returns())):
    print('Draw!')
  else:
    winner = player_labels[0] if state.returns()[0] > 0 else player_labels[1]
    print(f'winner: {winner}')


if __name__ == '__main__':
  main()
