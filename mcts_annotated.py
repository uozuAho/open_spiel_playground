# A duplicate of https://github.com/deepmind/open_spiel/blob/master/open_spiel/python/algorithms/mcts.py,
# annotated for a better understanding of the inner workings. I've removed some
# of the doc comments, see the original for those.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import time

import numpy as np

import pyspiel


class Evaluator(object):
  """Abstract class representing an evaluation function for a game.

  The evaluation function takes in an intermediate state in the game and returns
  an evaluation of that state, which should correlate with chances of winning
  the game. It returns the evaluation from all player's perspectives.
  """

  def evaluate(self, state):
    """Returns evaluation on given state."""
    raise NotImplementedError

  def prior(self, state):
    """Returns a probability for each legal action in the given state."""
    raise NotImplementedError


class RandomRolloutEvaluator(Evaluator):
  """A simple evaluator doing random rollouts.

  This evaluator returns the average outcome of playing random actions from the
  given state until the end of the game.  n_rollouts is the number of random
  outcomes to be considered.
  """

  def __init__(self, n_rollouts=1, random_state=None):
    self.n_rollouts = n_rollouts
    self._random_state = random_state or np.random.RandomState()

  def evaluate(self, state):
    """Returns evaluation on given state."""
    result = None
    for _ in range(self.n_rollouts):
      working_state = state.clone()
      while not working_state.is_terminal():
        if working_state.is_chance_node():
          outcomes = working_state.chance_outcomes()
          action_list, prob_list = zip(*outcomes)
          action = self._random_state.choice(action_list, p=prob_list)
        else:
          action = self._random_state.choice(working_state.legal_actions())
        working_state.apply_action(action)
      returns = np.array(working_state.returns())
      result = returns if result is None else result + returns

    return result / self.n_rollouts

  def prior(self, state):
    """Returns equal probability for all actions."""
    if state.is_chance_node():
      return state.chance_outcomes()
    else:
      legal_actions = state.legal_actions(state.current_player())
      return [(action, 1.0 / len(legal_actions)) for action in legal_actions]


class SearchNode(object):
  """A node in the search tree.

  A SearchNode represents a state and possible continuations from it. Each child
  represents a possible action, and the expected result from doing so.

  Attributes:
    action: The action from the parent node's perspective. Not important for the
      root node, as the actions that lead to it are in the past.
    player: Which player made this action.
    prior: A prior probability for how likely this action will be selected.
    explore_count: How many times this node was explored.
    total_reward: The sum of rewards of rollouts through this node, from the
      parent node's perspective. The average reward of this node is
      `total_reward / explore_count`
    outcome: The rewards for all players if this is a terminal node or the
      subtree has been proven, otherwise None.
    children: A list of SearchNodes representing the possible actions from this
      node, along with their expected rewards.
  """
  __slots__ = [
      "action",
      "player",
      "prior",
      "explore_count",
      "total_reward",
      "outcome",
      "children",
  ]

  def __init__(self, action, player, prior):
    self.action = action
    self.player = player
    self.prior = prior
    self.explore_count = 0
    self.total_reward = 0.0
    self.outcome = None
    self.children = []

  def uct_value(self, parent_explore_count, uct_c):
    """Returns the UCT value of child."""
    if self.outcome is not None:
      return self.outcome[self.player]

    if self.explore_count == 0:
      return float("inf")

    return self.total_reward / self.explore_count + uct_c * math.sqrt(
        math.log(parent_explore_count) / self.explore_count)

  def puct_value(self, parent_explore_count, uct_c):
    """Returns the PUCT value of child."""
    if self.outcome is not None:
      return self.outcome[self.player]

    return ((self.explore_count and self.total_reward / self.explore_count) +
            uct_c * self.prior * math.sqrt(parent_explore_count) /
            (self.explore_count + 1))

  def sort_key(self):
    """Returns the best action from this node, either proven or most visited.

    This ordering leads to choosing:
    - Highest proven score > 0 over anything else, including a promising but
      unproven action.
    - A proven draw only if it has higher exploration than others that are
      uncertain, or the others are losses.
    - Uncertain action with most exploration over loss of any difficulty
    - Hardest loss if everything is a loss
    - Highest expected reward if explore counts are equal (unlikely).
    - Longest win, if multiple are proven (unlikely due to early stopping).
    """
    return (0 if self.outcome is None else self.outcome[self.player],
            self.explore_count, self.total_reward)

  def best_child(self):
    """Returns the best child in order of the sort key."""
    return max(self.children, key=SearchNode.sort_key)

  def children_str(self, state=None):
    """Returns the string representation of this node's children.

    They are ordered based on the sort key, so order of being chosen to play.

    Args:
      state: A `pyspiel.State` object, to be used to convert the action id into
        a human readable format. If None, the action integer id is used.
    """
    return "\n".join([
        c.to_str(state)
        for c in reversed(sorted(self.children, key=SearchNode.sort_key))
    ])

  def to_str(self, state=None):
    """Returns the string representation of this node.

    Args:
      state: A `pyspiel.State` object, to be used to convert the action id into
        a human readable format. If None, the action integer id is used.
    """
    action = (
        state.action_to_string(state.current_player(), self.action)
        if state and self.action is not None else str(self.action))
    return ("{:>6}: player: {}, prior: {:5.3f}, value: {:6.3f}, sims: {:5d}, "
            "outcome: {}, {:3d} children").format(
                action, self.player, self.prior, self.explore_count and
                self.total_reward / self.explore_count, self.explore_count,
                ("{:4.1f}".format(self.outcome[self.player])
                 if self.outcome else "none"), len(self.children))

  def __str__(self):
    return self.to_str(None)


class MCTSBot(pyspiel.Bot):
  """Bot that uses Monte-Carlo Tree Search algorithm."""

  def __init__(self,
               game,
               uct_c,
               max_simulations,
               evaluator,
               solve=True,
               random_state=None,
               child_selection_fn=SearchNode.uct_value,
               dirichlet_noise=None,
               verbose=False):
    """Initializes a MCTS Search algorithm in the form of a bot.

    In multiplayer games, or non-zero-sum games, the players will play the
    greedy strategy.

    Args:
      game: A pyspiel.Game to play.
      uct_c: The exploration constant for UCT.
      max_simulations: How many iterations of MCTS to perform. Each simulation
        will result in one call to the evaluator. Memory usage should grow
        linearly with simulations * branching factor. How many nodes in the
        search tree should be evaluated. This is correlated with memory size and
        tree depth.
      evaluator: A `Evaluator` object to use to evaluate a leaf node.
      solve: Whether to back up solved states.
      random_state: An optional numpy RandomState to make it deterministic.
      child_selection_fn: A function to select the child in the descent phase.
        The default is UCT.
      dirichlet_noise: A tuple of (epsilon, alpha) for adding dirichlet noise to
        the policy at the root. This is from the alpha-zero paper.
      verbose: Whether to print information about the search tree before
        returning the action. Useful for confirming the search is working
        sensibly.

    Raises:
      ValueError: if the game type isn't supported.
    """
    pyspiel.Bot.__init__(self)
    # Check that the game satisfies the conditions for this MCTS implemention.
    game_type = game.get_type()
    if game_type.reward_model != pyspiel.GameType.RewardModel.TERMINAL:
      raise ValueError("Game must have terminal rewards.")
    if game_type.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
      raise ValueError("Game must have sequential turns.")

    self._game = game
    self.uct_c = uct_c
    self.max_simulations = max_simulations
    self.evaluator = evaluator
    self.verbose = verbose
    self.solve = solve
    self.max_utility = game.max_utility()
    self._dirichlet_noise = dirichlet_noise
    self._random_state = random_state or np.random.RandomState()
    self._child_selection_fn = child_selection_fn

  def restart_at(self, state):
    pass

  def step_with_policy(self, state):
    """Returns bot's policy and action at given state."""
    t1 = time.time()
    root = self.mcts_search(state)

    best = root.best_child()

    if self.verbose:
      seconds = time.time() - t1
      print("Finished {} sims in {:.3f} secs, {:.1f} sims/s".format(
          root.explore_count, seconds, root.explore_count / seconds))
      print("Root:")
      print(root.to_str(state))
      print("Children:")
      print(root.children_str(state))
      if best.children:
        chosen_state = state.clone()
        chosen_state.apply_action(best.action)
        print("Children of chosen:")
        print(best.children_str(chosen_state))

    mcts_action = best.action

    policy = [(action, (1.0 if action == mcts_action else 0.0))
              for action in state.legal_actions(state.current_player())]

    return policy, mcts_action

  def step(self, state):
    return self.step_with_policy(state)[1]

  def _apply_tree_policy(self, root, state):
    """Applies the UCT policy to play the game until reaching a leaf node.

    A leaf node is defined as a node that is terminal or has not been evaluated
    yet. If it reaches a node that has been evaluated before but hasn't been
    expanded, then expand it's children and continue.

    Args:
      root: The root node in the search tree.
      state: The state of the game at the root node.

    Returns:
      visit_path: A list of nodes descending from the root node to a leaf node.
      working_state: The state of the game at the leaf node.
    """
    visit_path = [root]
    working_state = state.clone()
    current_node = root
    print(f"applying tree policy from state\n{state}")
    while not working_state.is_terminal() and current_node.explore_count > 0:
      if not current_node.children:
        print('path from current state is unexplored. Legal actions:')
        legal_actions = self.evaluator.prior(working_state)
        print(legal_actions)
        if current_node is root and self._dirichlet_noise:
          epsilon, alpha = self._dirichlet_noise
          noise = self._random_state.dirichlet([alpha] * len(legal_actions))
          legal_actions = [(a, (1 - epsilon) * p + epsilon * n)
                           for (a, p), n in zip(legal_actions, noise)]
        # Reduce bias from move generation order.
        self._random_state.shuffle(legal_actions)
        player = working_state.current_player()
        current_node.children = [
            SearchNode(action, player, prior) for action, prior in legal_actions
        ]

      if working_state.is_chance_node():
        # For chance nodes, rollout according to chance node's probability
        # distribution
        outcomes = working_state.chance_outcomes()
        action_list, prob_list = zip(*outcomes)
        action = self._random_state.choice(action_list, p=prob_list)
        chosen_child = next(
            c for c in current_node.children if c.action == action)
      else:
        # Otherwise choose node with largest UCT value
        chosen_child = max(
            current_node.children,
            key=lambda c: self._child_selection_fn(  # pylint: disable=g-long-lambda
                c, current_node.explore_count, self.uct_c))

      working_state.apply_action(chosen_child.action)
      current_node = chosen_child
      visit_path.append(current_node)

    return visit_path, working_state

  def mcts_search(self, state):
    root_player = state.current_player()
    root = SearchNode(None, state.current_player(), 1)
    for _ in range(self.max_simulations):
      visit_path, working_state = self._apply_tree_policy(root, state)
      if working_state.is_terminal():
        returns = working_state.returns()
        visit_path[-1].outcome = returns
        solved = self.solve
      else:
        returns = self.evaluator.evaluate(working_state)
        solved = False

      for node in reversed(visit_path):
        node.total_reward += returns[root_player if node.player ==
                                     pyspiel.PlayerId.CHANCE else node.player]
        node.explore_count += 1

        if solved and node.children:
          player = node.children[0].player
          if player == pyspiel.PlayerId.CHANCE:
            # Only back up chance nodes if all have the same outcome.
            # An alternative would be to back up the weighted average of
            # outcomes if all children are solved, but that is less clear.
            outcome = node.children[0].outcome
            if (outcome is not None and
                all(np.array_equal(c.outcome, outcome) for c in node.children)):
              node.outcome = outcome
            else:
              solved = False
          else:
            # If any have max utility (won?), or all children are solved,
            # choose the one best for the player choosing.
            best = None
            all_solved = True
            for child in node.children:
              if child.outcome is None:
                all_solved = False
              elif best is None or child.outcome[player] > best.outcome[player]:
                best = child
            if (best is not None and
                (all_solved or best.outcome[player] == self.max_utility)):
              node.outcome = best.outcome
            else:
              solved = False
      if root.outcome is not None:
        break

    return root
