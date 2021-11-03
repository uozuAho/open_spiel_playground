# Demo: OpenSpiel agents play remote tic tac toe game, using ZMQ

The remote game server can be implemented in any language, and run locally or
remotely. Games are played sychronously in a request-response format. The server
initialises the game and waits for a network bot to start making requests.

# quick start
```sh
# run tests
python tests.py
# run performance comparison of local/remote games
python performance_comparison.py
# run verbose playthrough
python play_one_verbose_game.py
```

# performance
- as you'd expect, this is slow. Playing a local agent against a remote
  agent runs about 50-100 slower than two local agents.
- using IPC vs TCP transports in ZMQ makes no difference

# todo
- game server: wrap tic tac toe game
- update docs
- fix unclosed zmq context during tests
- try random & mcts vs pandemic game
- ideas to improve performance
  - more efficient (de)serialiser?
- server should have no references to openSpiel
