from multiprocessing import Process

import numpy as np
from open_spiel.python.bots import uniform_random

from game_server import TicTacToeServer
from networking import DictClient
from network_bot import NetworkGame


def main():
  server = TicTacToeServer("tcp://*:5555")
  server_process = Process(target=server.run)
  server_process.start()

  bot = uniform_random.UniformRandomBot(1, np.random.RandomState())

  client = DictClient("tcp://localhost:5555")
  game = NetworkGame(client)
  state = game.new_initial_state()

  while not state.is_terminal():
    print('state:')
    print(state)
    action = bot.step(state)
    print('bot action:', action)
    state.apply_action(action)

  game.exit()
  client.close()
  server_process.join()


if __name__ == "__main__":
  main()
