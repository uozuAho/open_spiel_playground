# Playing around with OpenSpiel

[OpenSpiel](https://github.com/deepmind/open_spiel) is a reinforcement learning
framework that comes with a bunch of games and algorithms. This repo documents
how to get it installed and run some examples.


# Getting started
- use linux
    - mingw: just a pain, everything breaks
    - docker: didn't work immediately, gave up :)
    - WSL: hard to get GUI working
- follow [install docs](https://github.com/deepmind/open_spiel/blob/master/docs/install.md)
- run `sudo apt-get install python3-tk` (otherwise Matplotlib complains)
- test it worked:

> python3 venv/lib/python3.8/site-packages/open_spiel/python/examples/example.py --game=tic_tac_toe

Now some more:

```sh
# run some games
python3 venv/lib/python3.8/site-packages/open_spiel/python/examples/example.py --game=breakthrough
python3 venv/lib/python3.8/site-packages/open_spiel/python/examples/mcts.py --game=tic_tac_toe

# browse open speil stuff
code venv/lib/python3.8/site-packages/open_spiel

# print games
python3 print_games.py

# single agent cliff walking demo
python3 venv/lib/python3.8/site-packages/open_spiel/python/examples/single_agent_cliff_walking.py

# test GUI works
python3 venv/share/doc/networkx-2.4/examples/algorithms/plot_davis_club.py
```


# notes
- what's the difference between an env and a game. Why can't I use
  value_iteration on an env?
    - open_spiel.python.rl_environment wraps pyspiel.game
- why can't I find the definition of pyspiel.load_game?
    - it's bound to the C++ LoadGame implementation


# todo
- try value iteration with cliff walking. need to use game instead of env
- can I use sarsa from python?
  - there's only 2 bots in pyspiel.registered_bots(). How to use c algorithms?
