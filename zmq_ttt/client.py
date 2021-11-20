import math

import numpy as np
from open_spiel.python.bots import uniform_random
from open_spiel.python.algorithms import mcts

from network_game import NetworkGame


def main():
  game = NetworkGame("tcp://localhost:5555")
  # bot = uniform_random.UniformRandomBot(0, np.random.RandomState())
  bot = mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      max_simulations=3,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=2))
  state = game.new_initial_state()

  while not state.is_terminal():
    action = bot.step(state)
    print('bot action:', action)
    state.apply_action(action)

  game.exit()
  print("done")
  print(state)


if __name__ == "__main__":
  main()
