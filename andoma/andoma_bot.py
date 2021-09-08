import chess
import pyspiel
from . import movegeneration

class AndomaBot(pyspiel.Bot):
  def __init__(self, search_depth=1):
    pyspiel.Bot.__init__(self)
    self.search_depth = search_depth

  def step(self, state: pyspiel.State) -> int:
    board = chess.Board(str(state))
    move = movegeneration.next_move(self.search_depth, board, debug=False)
    return self._pychess_to_spiel_move(move, state)

  def _pychess_to_spiel_move(self, move: chess.Move, state: pyspiel.State):
    # This is necessary, as openspiel's chess SANs differ from pychess's.
    # For example, in a new game, openspiel lists 'aa3' as a valid action. The
    # file disambiguation is unnecessary here - pychess lists this valid action
    # as 'a3'.
    board = chess.Board(str(state))

    def action_str(action):
      return state.action_to_string(state.current_player(), action)

    move_map = {board.parse_san(action_str(action)): action for action in state.legal_actions()}

    if move not in move_map:
      raise RuntimeError(f"{move} is not a legal move!")

    return move_map[move]
