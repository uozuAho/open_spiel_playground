from absl.testing import absltest
import numpy as np
from open_spiel.python.bots import uniform_random

from bot_client import BotClient
from game_server import TicTacToeServer


class RemoteTicTacToeTests(absltest.TestCase):
  def test_random_vs_random_game(self):
    server = TicTacToeServer("ipc:///tmp/ttt")
    server.serve_one_game()
    random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    bot = BotClient(random_bot)
    bot.connect("ipc:///tmp/ttt")
    bot.run()


if __name__ == "__main__":
  absltest.main()
