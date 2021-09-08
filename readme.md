# Playing around with OpenSpiel

[OpenSpiel](https://github.com/deepmind/open_spiel) is a reinforcement learning
framework that comes with a bunch of games and algorithms. This repo documents
how to get it installed and run some examples.

# todo for mcts vs andoma
- play more games!

# Getting started
- use linux
    - mingw: just a pain, everything breaks
    - docker: didn't work immediately, gave up :)
    - WSL: hard to get GUI working

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# test it worked:
python print_games.py
python mcts_ttt_annotated.py
python .venv/lib/python3.8/site-packages/open_spiel/python/examples/example.py --game=tic_tac_toe

# browse open speil stuff
code ./venv/lib/python3.8/site-packages/open_spiel
```

# Getting GUI bits to run
Not sure if this works/is necessary.

```sh
sudo apt-get install python3-tk  # otherwise Matplotlib complains
python .venv/share/doc/networkx-2.4/examples/algorithms/plot_davis_club.py
```
