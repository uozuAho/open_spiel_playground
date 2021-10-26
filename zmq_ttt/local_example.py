import numpy as np

import pyspiel
from open_spiel.python.bots import uniform_random


def main():
  game = pyspiel.load_game("tic_tac_toe")
  state = game.new_initial_state()
  bot_1 = uniform_random.UniformRandomBot(0, np.random.RandomState())
  bot_2 = uniform_random.UniformRandomBot(1, np.random.RandomState())

  players = [bot_1, bot_2]
  player_labels = ['bot_1', 'bot_2']

  while not state.is_terminal():
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    action = current_player.step(state)
    state.apply_action(action)

  winner = player_labels[0] if state.returns()[0] > 0 else player_labels[1]
  print('final state:')
  print(state)
  print(f'winner: {winner}')


if __name__ == '__main__':
  main()
