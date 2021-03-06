from multiprocessing import Process

import numpy as np
import pyspiel
from open_spiel.python.bots import uniform_random

from game_server import GameServer
from network_game import NetworkGame


def main():
  server = GameServer("tcp://*:5555", pyspiel.load_game("tic_tac_toe"))
  server_process = Process(target=server.run)
  server_process.start()

  bot1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  bot2 = uniform_random.UniformRandomBot(1, np.random.RandomState())

  players = [bot1, bot2]

  game = NetworkGame("tcp://localhost:5555")
  state = game.new_initial_state()

  while not state.is_terminal():
    print('state:')
    print(state)
    current_player = players[state.current_player()]
    print('current player', state.current_player())
    action = current_player.step(state)
    print('bot action:', action)
    state.apply_action(action)

  game.exit()
  server_process.join()


if __name__ == "__main__":
  main()
