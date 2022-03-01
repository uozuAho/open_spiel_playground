# Alpha zero

Playing around with ... AlphaZero

OpenSpiel docs here: https://github.com/deepmind/open_spiel/blob/5eaf401f7d08d68285fe214ab5cf5a741807ea6e/docs/alpha_zero.md

```sh
pip install --upgrade pip
# not included in requirements.txt since it's huge:
pip install tensorflow matplotlib pandas pyqt5
# simplest example: train an agent to play tic tac toe
python .venv/lib/python3.9/site-packages/open_spiel/python/examples/tic_tac_toe_alpha_zero.py --path ttt_model
# print some pretty charts of how training went
python3 .venv/lib/python3.9/site-packages/open_spiel/python/algorithms/alpha_zero/analysis.py --path ttt_model
# play against the trained agent:
python3 .venv/lib/python3.9/site-packages/open_spiel/python/examples/mcts.py --game=tic_tac_toe --player1=human --player2=az --az_path ttt_model/checkpoint-25
```
