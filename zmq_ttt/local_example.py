from datetime import datetime
import math
import numpy as np

import pyspiel
from open_spiel.python.bots import uniform_random
from open_spiel.python.algorithms import mcts


def main():
  play_one_demo_game()
  print_games_per_second()


def play_one_demo_game():
  game = pyspiel.load_game("tic_tac_toe")
  bot_1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  bot_2 = uniform_random.UniformRandomBot(1, np.random.RandomState())

  state = play_one_game(game, bot_1, bot_2)

  player_labels = ['bot_1', 'bot_2']
  winner = player_labels[0] if state.returns()[0] > 0 else player_labels[1]
  print('final state:')
  print(state)
  print(f'winner: {winner}')


def print_games_per_second():
  game = pyspiel.load_game("tic_tac_toe")
  bot_1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  # bot_2 = uniform_random.UniformRandomBot(1, np.random.RandomState())
  bot_2 = mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      # starts beating random bot at ~ 3 sims, 1 rollout
      max_simulations=4,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=2))

  last = datetime.now()
  num_games = 0
  bot_1_wins = 0
  bot_2_wins = 0
  while True:
    state = play_one_game(game, bot_1, bot_2)
    if state.returns()[0] > 0:
      bot_1_wins += 1
    else:
      bot_2_wins += 1
    num_games += 1
    if (datetime.now() - last).total_seconds() > 1:
      print(f'{num_games} games/sec. wins: bot 1: {bot_1_wins}, bot 2: {bot_2_wins}')
      num_games = 0
      last = datetime.now()


def play_one_game(game, player_1, player_2):
  players = [player_1, player_2]
  state = game.new_initial_state()

  while not state.is_terminal():
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    action = current_player.step(state)
    state.apply_action(action)

  return state


if __name__ == '__main__':
  main()
