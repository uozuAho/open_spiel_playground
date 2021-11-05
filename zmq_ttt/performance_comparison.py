from datetime import datetime, timedelta
import math
from multiprocessing import Process
import numpy as np

import pyspiel
from open_spiel.python.bots import uniform_random
from open_spiel.python.algorithms import mcts

from game_server import TicTacToeServer
from network_game import NetworkGame


def main():
  local_random_vs_random()
  remote_random_vs_random()
  local_random_vs_mcts()
  random_vs_remote_mcts()


def local_random_vs_random():
  print("local_random_vs_random")
  game = pyspiel.load_game("tic_tac_toe")
  b1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  b2 = uniform_random.UniformRandomBot(1, np.random.RandomState())
  print_games_per_second(game, b1, b2, time_limit_s=3)


def remote_random_vs_random():
  print("remote_random_vs_random")
  server = start_game_server("tcp://*:5555")
  game = NetworkGame("tcp://localhost:5555")
  b1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  b2 = uniform_random.UniformRandomBot(1, np.random.RandomState())

  print_games_per_second(game, b1, b2, time_limit_s=3)

  game.exit()
  server.join()


def local_random_vs_mcts():
  print("local_random_vs_mcts")
  game = pyspiel.load_game("tic_tac_toe")
  b1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  b2 = mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      # starts beating random bot at ~ 3 sims, 1 rollout
      max_simulations=3,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=2))
  print_games_per_second(game, b1, b2, time_limit_s=3)


def random_vs_remote_mcts():
  print("random_vs_remote_mcts")
  server = start_game_server("tcp://*:5555")
  game = NetworkGame("tcp://localhost:5555")
  random_bot = uniform_random.UniformRandomBot(0, np.random.RandomState())
  mcts_bot = mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      # starts beating random bot at ~ 3 sims, 1 rollout
      max_simulations=3,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=2))

  print_games_per_second(game, random_bot, mcts_bot, time_limit_s=3)

  game.exit()
  server.join()


def start_game_server(url):
  server = TicTacToeServer(url)
  process = Process(target=server.run)
  process.start()
  return process


def print_games_per_second(game, player_1, player_2, time_limit_s):
  end = datetime.now() + timedelta(seconds=time_limit_s)
  last = datetime.now()
  num_games = 0
  bot_1_wins = 0
  bot_2_wins = 0
  while datetime.now() < end:
    state = local_play_one_game(game, player_1, player_2)
    if state.returns()[0] > 0:
      bot_1_wins += 1
    else:
      bot_2_wins += 1
    num_games += 1
    if (datetime.now() - last).total_seconds() > 1:
      print(f'{num_games} games/sec. wins: bot 1: {bot_1_wins}, bot 2: {bot_2_wins}')
      num_games = 0
      last = datetime.now()


def local_play_one_game(game, player_1, player_2):
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
