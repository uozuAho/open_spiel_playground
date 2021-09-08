import chess
import pyspiel
from . import movegeneration

class AndomaBot(pyspiel.Bot):
  def __init__(self):
    pyspiel.Bot.__init__(self)
    self.search_depth = 1

  def step(self, state: pyspiel.State) -> int:
    print('andoma is thinking...')
    board = chess.Board(str(state))
    print('current state:')
    print(board)

    def action_str(action):
      return state.action_to_string(state.current_player(), action)

    print('legal moves according to openspiel:')
    print([action_str(action) for action in state.legal_actions()])

    print('legal moves according to pychess:')
    print([board.san(move) for move in board.legal_moves])

    print('mapped moves:')
    move_map = {board.parse_san(action_str(action)): action for action in state.legal_actions()}
    print(move_map)

    move = movegeneration.next_move(self.search_depth, board, debug=False)
    print('andoma chooses move:')
    print(move)

    if move not in move_map:
      raise RuntimeError(f"chosen move {move} is not a legal move!")

    return move_map[move]
