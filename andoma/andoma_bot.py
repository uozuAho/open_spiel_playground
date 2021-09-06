import chess
import pyspiel
from . import movegeneration

class AndomaBot(pyspiel.Bot):
  def __init__(self):
    pyspiel.Bot.__init__(self)
    self.search_depth = 1

  def step(self, state: pyspiel.State) -> int:
    board = chess.Board(str(state))
    print([state.action_to_string(state.current_player(), action) for action in state.legal_actions()])
    move = movegeneration.next_move(self.search_depth, board, debug=False)
    print(move)
