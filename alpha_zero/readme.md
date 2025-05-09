# Alpha zero

Playing around with ... AlphaZero

DOESN'T WORK. I think I've got the tensorflow deps wrong, meh. Run it and see
the errors.

OpenSpiel docs here: https://github.com/deepmind/open_spiel/blob/5eaf401f7d08d68285fe214ab5cf5a741807ea6e/docs/alpha_zero.md

Note: openspiel depends on certain versions of tensorflow. Search their repo
for mentions of tensorflow, eg https://github.com/google-deepmind/open_spiel/blob/d99705de2cca7075e12fbbd76443fcc123249d6f/open_spiel/scripts/python_extra_deps.sh#L57

```sh
uv sync
# simplest example: train an agent to play tic tac toe
uv run .venv/lib/python3.12/site-packages/open_spiel/python/examples/tic_tac_toe_alpha_zero.py --path ttt_model
# print some pretty charts of how training went
uv run .venv/lib/python3.12/site-packages/open_spiel/python/algorithms/alpha_zero/analysis.py --path ttt_model
# play against the trained agent:
uv run .venv/lib/python3.12/site-packages/open_spiel/python/examples/mcts.py --game=tic_tac_toe --player1=human --player2=az --az_path ttt_model/checkpoint-25
```
