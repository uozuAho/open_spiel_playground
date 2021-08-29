#!python3
# An annotated example of playing tic tac toe with an MCTS. The intention is to
# show how MCTS works.

import math
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

UCT_C = math.sqrt(2)

def main():
  game = pyspiel.load_game("tic_tac_toe")
  state = game.new_initial_state()
  mcts_bot = new_mcts_bot(game)
  random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())

  players = [mcts_bot, random_bot]
  player_labels = ['mcts', 'random']

  while not state.is_terminal():
    print('current state:')
    print(state)
    if state.is_chance_node():
      raise RuntimeError("didn't expect a chance node!")
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    if current_player_idx == 0:
      action = mcts_step_standard(current_player, state)
    else:
      action = current_player.step(state)
    action_str = state.action_to_string(current_player_idx, action)
    print(f"Player {player_labels[current_player_idx]} action: {action_str}")
    state.apply_action(action)
    print()

  winner = player_labels[0] if state.returns()[0] > 0 else player_labels[0]
  print('final state:')
  print(state)
  print(f'winner: {winner}')

def new_mcts_bot(game, rng=np.random.RandomState()):
  return mcts.MCTSBot(
      game,
      UCT_C,
      max_simulations=10,
      solve=True,
      random_state=rng,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=20, random_state=rng),
      verbose=True)

def mcts_step_standard(bot, state):
  return bot.step(state)

if __name__ == '__main__':
  main()
