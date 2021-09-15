# Plays a game of chess between two bots

DEBUG=False

from datetime import datetime
import math
from re import S
import numpy as np

import pyspiel
from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random

import chess
from andoma import andoma_bot as andoma
from andoma.movegeneration import get_ordered_moves


game = pyspiel.load_game("chess")


def main():
  mcts_vs_random()
  # mcts_incremental_vs_rando()
  # andoma_vs_random()


def mcts_vs_random():
  play_one_game_and_print_results([
    new_mcts_bot(game, 2, mcts.RandomRolloutEvaluator(n_rollouts=1)),
    uniform_random.UniformRandomBot(1, np.random.RandomState())
  ])


def andoma_vs_random():
  play_one_game_and_print_results([
    andoma.AndomaBot(search_depth=1),
    uniform_random.UniformRandomBot(1, np.random.RandomState())
  ])


def play_one_game_and_print_results(players):
  player_names = [classname(p) for p in players]
  print(f'{player_names[0]} (b) vs {player_names[1]} (W)')

  state = play_one_game(players)

  print(state)
  print(chess.Board(fen=str(state)))
  print_outcome(state, player_names)


def mcts_incremental_vs_rando():
  # Play mcts vs random player, with incrementally increasing MCTS simulations
  # and rollouts.
  # Takes ages!
  for num_sims in range(2, 11):
    for num_rollouts in range(1, 11):
      start = datetime.now()
      print(f'sims: {num_sims}, rollouts: {num_rollouts}')
      players = [
        new_mcts_bot(game, num_sims, mcts.RandomRolloutEvaluator(n_rollouts=num_rollouts)),
        uniform_random.UniformRandomBot(1, np.random.RandomState())
      ]

      state = play_one_game(players)

      is_draw = winner_idx(state) is None
      mcts_won = winner_idx(state) == 0
      result = 'draw' if is_draw else 'mcts: win' if mcts_won else 'mcts: lose'
      print(f'game over in {datetime.now() - start}, result: {result}', flush=True)


def play_one_game(players):
  # plays one game, returns the final state
  state = game.new_initial_state()
  player_labels = [classname(p) for p in players]

  while not state.is_terminal():
    current_player_idx = state.current_player()
    current_player = players[current_player_idx]
    if DEBUG:
      print_dbg_state(state, player_labels)
      input("press a key...")
    action = current_player.step(state)
    if DEBUG:
      print_action(state, action)
    state.apply_action(action)

  return state


def new_mcts_bot(game, max_sims, evaluator):
  if max_sims < 2:
    raise RuntimeError('max_sims must be > 1 ... I think the implementation is broken')
  return mcts.MCTSBot(
      game,
      uct_c=math.sqrt(2),
      max_simulations=max_sims,
      evaluator=evaluator)


class AndomaValuesRolloutEvaluator:
  """Rollout for MCTS. Greedily picks the best move based on Andoma's move
     values.
  """
  def __init__(self, n_rollouts=1):
    self.n_rollouts = n_rollouts

  def evaluate(self, state):
    """ 'Rolls out' a complete game, returning the outcome. """
    result = None
    for _ in range(self.n_rollouts):
      working_state = state.clone()
      while not working_state.is_terminal():
        if working_state.is_chance_node():
          raise RuntimeError("didn't expect a chance node!")
        else:
          action = self._best_action(working_state)
        working_state.apply_action(action)
      returns = np.array(working_state.returns())
      result = returns if result is None else result + returns

    return result / self.n_rollouts

  def prior(self, state):
    """Returns the probability for all actions at the given state. I'll just
       return 1.0 for the 'best' action, and 0 for the others. Not sure if
       that's right...
    """
    if state.is_chance_node():
      raise RuntimeError('nope')
    else:
      legal_actions = state.legal_actions(state.current_player())
      best_action = self._best_action(state)
      return [(a, 1.0 if a == best_action else 0.0) for a in legal_actions]

  def _best_action(self, state: pyspiel.State) -> int:
    board = chess.Board(str(state))
    move = get_ordered_moves(board)[0]
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


def print_dbg_state(state: pyspiel.State, player_labels):
  current_player_idx = state.current_player()
  print(state)
  print(chess.Board(fen=str(state)))
  print(f'current player ({"W" if current_player_idx == 1 else "b"}): {player_labels[current_player_idx]}')


def print_action(state, action):
  action_str = state.action_to_string(state.current_player(), action)
  print(f'action: {action_str}')


def print_outcome(state: pyspiel.State, player_labels):
  idx = winner_idx(state)
  if idx is None:
    print('Draw!')
  else:
    print(f'winner: {player_labels[idx]}')


def winner_idx(state):
  if all((x == 0 for x in state.returns())):
    return None
  else:
    return 0 if state.returns()[0] > 0 else 1


def classname(o):
  return type(o).__name__


if __name__ == '__main__':
  main()
