import random
import pyspiel
import numpy as np

game = pyspiel.load_game("kuhn_poker")
state = game.new_initial_state()
while not state.is_terminal():
  print("state:", state)
  legal_actions = state.legal_actions()
  print("legal actions:", legal_actions)
  if state.is_chance_node():
    print("chance node")
    # Sample a chance event outcome.
    outcomes_with_probs = state.chance_outcomes()
    action_list, prob_list = zip(*outcomes_with_probs)
    action = np.random.choice(action_list, p=prob_list)
    print("random action: ", action)
    state.apply_action(action)
  else:
    print("agent node")
    # The algorithm can pick an action based on an observation (fully observable
    # games) or an information state (information available for that player)
    # We arbitrarily select the first available action as an example.
    action = legal_actions[0]
    print("action: ", action)
    state.apply_action(action)
