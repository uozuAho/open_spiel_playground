# Plays a game of chess between two bots

DEBUG=False

import math
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

import chess
from andoma import andoma_bot as andoma


game = pyspiel.load_game("chess")


def main():
  mcts_vs_random()


def mcts_vs_random():
  players = [
    new_mcts_bot(game, 2, 1),
    uniform_random.UniformRandomBot(1, np.random.RandomState())
  ]

  state = play_one_game(players)

  print(state)
  print(chess.Board(fen=str(state)))
  print_outcome(state, ['mcts', 'random'])


def play_one_game(players):
  # plays one game, returns the final state
  state = game.new_initial_state()
  player_labels = [classname(p) for p in players]

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

  return state


def new_mcts_bot(game, max_sims, num_rollouts, rng=np.random.RandomState()):
  if max_sims < 2:
    raise RuntimeError('max_sims must be > 1 ... I think the implementation is broken')
  return mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      max_simulations=max_sims,
      random_state=rng,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=num_rollouts, random_state=rng))


def print_dbg_state(state: pyspiel.State, player_labels):
  current_player_idx = state.current_player()
  print(state)
  print(chess.Board(fen=str(state)))
  print(f'current player ({"W" if current_player_idx == 1 else "b"}): {player_labels[current_player_idx]}')


def print_action(state, action):
  action_str = state.action_to_string(state.current_player(), action)
  print(f'action: {action_str}')


def print_outcome(state: pyspiel.State, player_labels):
  idx = winner_idx(state)
  if idx is None:
    print('Draw!')
  else:
    print(f'winner: {player_labels[idx]}')


def winner_idx(state):
  if all((x == 0 for x in state.returns())):
    return None
  else:
    return 0 if state.returns()[0] > 0 else 1


def classname(o):
  return type(o).__name__


if __name__ == '__main__':
  main()
