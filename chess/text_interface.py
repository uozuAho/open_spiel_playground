# play chess via a text interface

import pyspiel


def main():
  game = pyspiel.load_game("chess")
  state = game.new_initial_state()
  while not state.is_terminal():
    print("state:", state)
    legal_actions = state.legal_actions()
    action = get_action_from_user(state, legal_actions)
    print("current player: ", state.current_player())
    print("action: ", state.action_to_string(state.current_player(), action))
    state.apply_action(action)


def get_action_from_user(state, legal_actions):
  print('choose an action:')
  for i, action in enumerate(legal_actions):
    print('  ', i, action_str(state, action))
  user_choice = int(input())
  for i, action in enumerate(legal_actions):
    if user_choice == i:
      return action
  raise RuntimeError('oops!')


def action_str(state, action):
  return state.action_to_string(state.current_player(), action)


if __name__ == "__main__":
  main()
