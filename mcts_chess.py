# Plays a game of chess between an MCTS bot a random bot.
#
# To do
# - why is it so slow?

import math
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

def main():
  game = pyspiel.load_game("chess")
  state = game.new_initial_state()
  mcts_bot = new_mcts_bot(game)
  random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())

  players = [mcts_bot, random_bot]
  player_labels = ['mcts', 'random']

  while not state.is_terminal():
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    action = current_player.step(state)
    state.apply_action(action)

  winner = player_labels[0] if state.returns()[0] > 0 else player_labels[0]
  print('final state:')
  print(state)
  print(f'winner: {winner}')

def new_mcts_bot(game, rng=np.random.RandomState()):
  return mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      max_simulations=2,
      random_state=rng,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=1, random_state=rng))


if __name__ == '__main__':
  main()
