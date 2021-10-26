import pyspiel
import zmq


def main():
  run_ttt_server()


def run_ttt_server():
  ctx = zmq.Context()
  socket = ctx.socket(zmq.REP)
  socket.bind("tcp://*:5555")
  print("listening on port 5555")
  game = pyspiel.load_game("tic_tac_toe")
  state = game.new_initial_state()
  done = False
  while not done:
    req = socket.recv().decode('UTF-8')
    response = 'yo'
    done = True
  socket.send(response.encode('UTF-8'))


def legal_actions_msg(state):
  msg = ""
  for i, action in enumerate(state.legal_actions()):
    msg += f'  {i}: {action_str(state, action)}\n'
  return msg


def int_to_action(state, int):
  for i, action in enumerate(state.legal_actions()):
    if int == i:
      return action
  raise RuntimeError(f'invalid action number: {int}')


def action_str(state, action):
  return state.action_to_string(state.current_player(), action)


if __name__ == "__main__":
  main()
