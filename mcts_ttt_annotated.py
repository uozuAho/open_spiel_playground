#!python3
# An annotated example of playing tic tac toe with an MCTS. The intention is to
# show how MCTS works.

import math
import time
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

UCT_C = math.sqrt(2)

def main():
  game = pyspiel.load_game("tic_tac_toe")
  state = game.new_initial_state()
  mcts_bot = new_mcts_bot(game)
  random_bot = uniform_random.UniformRandomBot(1, np.random.RandomState())

  players = [mcts_bot, random_bot]
  player_labels = ['mcts', 'random']

  while not state.is_terminal():
    print('current state:')
    print(state)
    if state.is_chance_node():
      raise RuntimeError("didn't expect a chance node!")
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    if current_player_idx == 0:
      # action = mcts_step_standard(current_player, state)
      action = mcts_step_verbose(current_player, state)
    else:
      action = current_player.step(state)
    action_str = state.action_to_string(current_player_idx, action)
    print(f"Player {player_labels[current_player_idx]} action: {action_str}")
    state.apply_action(action)
    print()

  winner = player_labels[0] if state.returns()[0] > 0 else player_labels[0]
  print('final state:')
  print(state)
  print(f'winner: {winner}')

def new_mcts_bot(game, rng=np.random.RandomState()):
  return mcts.MCTSBot(
      game,
      UCT_C,
      max_simulations=10,
      solve=True,
      random_state=rng,
      evaluator=mcts.RandomRolloutEvaluator(n_rollouts=20, random_state=rng),
      verbose=False)

def mcts_step_standard(bot, state):
  # does whatever the mcts bot.step does
  return bot.step(state)

def mcts_step_verbose(bot, state):
  # additional verbosity of what's going on within the MCTS algorithm
  # note: set Verbose=False when instantiating the mcts bot
  t1 = time.time()
  root = bot.mcts_search(state)

  best = root.best_child()

  seconds = time.time() - t1
  print(f"Finished {root.explore_count} sims in {seconds:.3f} secs, " +
        f"{root.explore_count / seconds:.1f} sims/s")
  print("Root:")
  print(root.to_str(state))
  print("Children:")
  print(root.children_str(state))
  if best.children:
    chosen_state = state.clone()
    chosen_state.apply_action(best.action)
    print("Children of chosen:")
    print(best.children_str(chosen_state))

  return best.action


if __name__ == '__main__':
  main()
