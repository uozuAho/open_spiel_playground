# Playing around with OpenSpiel

[OpenSpiel](https://github.com/deepmind/open_spiel) is a reinforcement learning
framework that comes with a bunch of games and algorithms. This repo documents
how to get it installed and run some examples.

# Getting started
- install [uv](https://docs.astral.sh/uv/)
- use linux
    - mingw: just a pain, everything breaks
    - docker: didn't work immediately, gave up :)
    - WSL: hard to get GUI working

```sh
cd getting_started
uv sync

# test it worked:
uv run print_games.py
uv run mcts_ttt_annotated.py
uv run .venv/lib/python3.12/site-packages/open_spiel/python/examples/example.py --game_string=tic_tac_toe
```

# Explore further
Folders are their own uv projects. `uv sync` to install deps.

Note: openspiel depends on certain versions of tensorflow. Search their repo
for mentions of tensorflow, eg https://github.com/google-deepmind/open_spiel/blob/d99705de2cca7075e12fbbd76443fcc123249d6f/open_spiel/scripts/python_extra_deps.sh#L57

# Getting GUI bits to run
Not sure if this works/is necessary.

```sh
sudo apt-get install python3-tk  # otherwise Matplotlib complains
python .venv/share/doc/networkx-2.4/examples/algorithms/plot_davis_club.py
```
