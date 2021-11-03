import math
from multiprocessing import Process
import numpy as np
from absl.testing import absltest

from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

from network_bot import NetworkGame
from game_server import TicTacToeServer


class RemoteTicTacToeTests(absltest.TestCase):
  def test_mcts_vs_random_game(self):
    server = self._start_game_server("tcp://*:5555")

    game = NetworkGame(None, "tcp://localhost:5555")

    mcts_bot = mcts.MCTSBot(
        game,
        uct_c=math.sqrt(2),
        max_simulations=2,
        evaluator=mcts.RandomRolloutEvaluator(n_rollouts=1))

    random_bot = uniform_random.UniformRandomBot(0, np.random.RandomState())

    players = [mcts_bot, random_bot]

    state = game.new_initial_state()
    while not state.is_terminal():
      current_player = players[state.current_player()]
      action = current_player.step(state)
      state.apply_action(action)

    game.exit()
    server.join()

  def test_random_vs_random(self):
    server = self._start_game_server("tcp://*:5555")

    bot1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
    bot2 = uniform_random.UniformRandomBot(0, np.random.RandomState())
    players = [bot1, bot2]

    game = NetworkGame(None, "tcp://localhost:5555")
    state = game.new_initial_state()
    while not state.is_terminal():
      current_player = players[state.current_player()]
      action = current_player.step(state)
      state.apply_action(action)

    game.exit()
    server.join()

  def _start_game_server(self, url):
    server = TicTacToeServer(url)
    process = Process(target=server.run)
    process.start()
    return process


if __name__ == "__main__":
  absltest.main()
