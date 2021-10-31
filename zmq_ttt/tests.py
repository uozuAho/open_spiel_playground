from absl.testing import absltest
from multiprocessing import Process
import numpy as np
from open_spiel.python.bots import uniform_random

from bot_client import BotClient
from game_server import TicTacToeServer


class RemoteTicTacToeTests(absltest.TestCase):
  def test_random_vs_random_game(self):
    server = TicTacToeServer("ipc:///tmp/ttt")
    server_process = Process(target=server.serve_one_game)
    server_process.start()

    random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())
    bot = BotClient(random_bot)
    bot.connect("ipc:///tmp/ttt")

    client_process = Process(target=bot.run)
    client_process.start()

    client_process.join()
    server_process.join()


if __name__ == "__main__":
  absltest.main()
