import math
from multiprocessing import Process
import numpy as np
from absl.testing import absltest

from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

from network_bot import NetworkBot
from game_server import TicTacToeServer


class RemoteTicTacToeTests(absltest.TestCase):
  def test_random_vs_random_game(self):
    server = TicTacToeServer("tcp://*:5555")
    server_process = Process(target=server.serve_one_game)
    server_process.start()

    random_bot_builder = lambda game : uniform_random.UniformRandomBot(1, np.random.RandomState())
    bot = NetworkBot(random_bot_builder, "tcp://localhost:5555")

    client_process = Process(target=bot.run)
    client_process.start()

    client_process.join()
    server_process.join()
    # if we get here without hanging, success!

  def test_mcts_vs_random_game(self):
    server = TicTacToeServer("tcp://*:5555")
    server_process = Process(target=server.serve_one_game)
    server_process.start()

    mcts_bot_builder = lambda game : mcts.MCTSBot(
        game,
        uct_c=math.sqrt(2),
        max_simulations=2,
        evaluator=mcts.RandomRolloutEvaluator(n_rollouts=1))
    bot = NetworkBot(mcts_bot_builder, "tcp://localhost:5555")

    client_process = Process(target=bot.run)
    client_process.start()

    client_process.join()
    server_process.join()
    # if we get here without hanging, success!

  def test_measure_performance(self):
    server = TicTacToeServer("tcp://*:5555")
    server_process = Process(target=server.measure_games_per_second, args=(0.5,))
    server_process.start()

    random_bot_builder = lambda game : uniform_random.UniformRandomBot(1, np.random.RandomState())
    bot = NetworkBot(random_bot_builder, "tcp://localhost:5555")

    client_process = Process(target=bot.run)
    client_process.start()

    client_process.join()
    server_process.join()
    # if we get here without hanging, success!


if __name__ == "__main__":
  absltest.main()
