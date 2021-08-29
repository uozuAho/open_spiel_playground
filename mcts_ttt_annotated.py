#!python3
# An annotated example of playing tic tac toe with an MCTS. The intention is to
# show how MCTS works.

import math
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

UCT_C = math.sqrt(2)

game = pyspiel.load_game("tic_tac_toe")
state = game.new_initial_state()
rng = np.random.RandomState()  # init with value for a repeatable game
mcts_bot = mcts.MCTSBot(
    game,
    UCT_C,
    max_simulations=10,
    solve=True,
    random_state=rng,
    evaluator=mcts.RandomRolloutEvaluator(n_rollouts=20, random_state=rng),
    verbose=True)
random_bot = uniform_random.UniformRandomBot(1, rng)

players = [mcts_bot, random_bot]

while not state.is_terminal():
  print('current state:')
  print(state)
  if state.is_chance_node():
    raise RuntimeError("didn't expect a chance node!")
  current_player_idx = state.current_player()
  current_player = players[current_player_idx]
  action = current_player.step(state)
  action_str = state.action_to_string(current_player_idx, action)
  print(f"Player {current_player_idx} sampled action: {action_str}")
  state.apply_action(action)
