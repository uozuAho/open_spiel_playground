Note: openspiel depends on certain versions of tensorflow. Search their repo
for mentions of tensorflow, eg https://github.com/google-deepmind/open_spiel/blob/d99705de2cca7075e12fbbd76443fcc123249d6f/open_spiel/scripts/python_extra_deps.sh#L57

```sh
uv sync
uv run .venv/lib/python3.12/site-packages/open_spiel/python/examples/tic_tac_toe_qlearner.py
uv run .venv/lib/python3.12/site-packages/open_spiel/python/examples/tic_tac_toe_dqn_vs_tabular.py
```
