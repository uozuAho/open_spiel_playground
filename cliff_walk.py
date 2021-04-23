# Replicating my cliff walking agent comparison from https://github.com/uozuAho/cs-ai/blob/462f80c3f7b6352c6489e930844894d8a80256d6/environments/cliff_walking/CliffWalking.Plots/InterimVsAsymptotic.cd

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from open_spiel.python.algorithms import tabular_qlearner
from open_spiel.python.environments import cliff_walking


def main():
  env = cliff_walking.Environment(width=5, height=3)
  num_actions = env.action_spec()["num_actions"]

  agent = tabular_qlearner.QLearner(
      player_id=0, step_size=0.05, num_actions=num_actions)

  train(env, agent, 100)
  avg_reward = eval_agent(env, agent, 50)

  print(avg_reward)


def train(env, agent, num_episodes):
  for _ in range(num_episodes):
    time_step = env.reset()
    while not time_step.last():
      agent_output = agent.step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)
    # Episode is over, step agent with final info state.
    agent.step(time_step)


def eval_agent(env, agent, num_episodes):
  """ Returns the average rewards received by the agent over the given episodes """
  rewards = 0.0
  for _ in range(num_episodes):
    time_step = env.reset()
    episode_reward = 0
    while not time_step.last():
      agent_output = agent.step(time_step, is_evaluation=True)
      time_step = env.step([agent_output.action])
      episode_reward += time_step.rewards[0]
    rewards += episode_reward
  return rewards / num_episodes


if __name__ == "__main__":
  main()
