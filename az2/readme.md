# alpha zero

OpenSpiel docs here: https://github.com/deepmind/open_spiel/blob/5eaf401f7d08d68285fe214ab5cf5a741807ea6e/docs/alpha_zero.md

Hopefully this works as openspiel/dependencies change. If not, see
https://github.com/google-deepmind/open_spiel/blob/d99705de2cca7075e12fbbd76443fcc123249d6f/open_spiel/scripts/python_extra_deps.sh#L57

```sh
uv sync

# check basic openspiel functionality works
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/example.py \
  --game_string=tic_tac_toe

# train (trains for 25 'checkpoints', 100k states, 13k episodes, takes ~3min)
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/tic_tac_toe_alpha_zero.py \
  --path ttt_model

# analyse (something broken, doesn't work)
uv run .venv/lib/python3.10/site-packages/open_spiel/python/algorithms/alpha_zero/analysis.py \
  --path ttt_model

# play human (you) against the trained bot
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/mcts.py \
  --game=tic_tac_toe --player1=human --player2=az \
  --az_path ttt_model/checkpoint-25

# play vs various opponents:

# az vs random
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/mcts.py \
  --game=tic_tac_toe --player1=az --player2=random \
  --az_path ttt_model/checkpoint-25 \
  --num_games 100 --quiet

# random vs az
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/mcts.py \
  --game=tic_tac_toe --player1=random --player2=az \
  --az_path ttt_model/checkpoint-25 \
  --num_games 100 --quiet

# az vs mcts (1 rollout (random rollout only), 1000 sims)
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/mcts.py \
  --game=tic_tac_toe --player1=az --player2=mcts \
  --az_path ttt_model/checkpoint-25 \
  --num_games 100 --quiet

# az vs mcts (30 rollouts (random rollout only), 30 sims)
uv run .venv/lib/python3.10/site-packages/open_spiel/python/examples/mcts.py \
  --game=tic_tac_toe --player1=az --player2=mcts \
  --az_path ttt_model/checkpoint-25 \
  --max_simulations 30 --rollout_count 30 \
  --num_games 100 --quiet
```
