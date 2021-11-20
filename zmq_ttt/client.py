import numpy as np
from open_spiel.python.bots import uniform_random

from network_game import NetworkGame


def main():
  bot1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  game = NetworkGame("tcp://localhost:5555")
  state = game.new_initial_state()

  while not state.is_terminal():
    action = bot1.step(state)
    print('bot action:', action)
    state.apply_action(action)

  game.exit()
  print("done")
  print(state)


if __name__ == "__main__":
  main()
