# Plays a game of chess by making random moves

import random
import pyspiel
import numpy as np

game = pyspiel.load_game("chess")
state = game.new_initial_state()
while not state.is_terminal():
  print("state:", state)
  legal_actions = state.legal_actions()
  if state.is_chance_node():
    raise RuntimeError('didnt expect a chance node')
  else:
    action = random.choice(legal_actions)
    print("current player: ", state.current_player())
    print("action: ", state.action_to_string(state.current_player(), action))
    state.apply_action(action)
