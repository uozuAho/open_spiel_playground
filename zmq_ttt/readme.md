# Demo: OpenSpiel agents play remote tic tac toe game, using ZMQ

Allows using OpenSpiel algorithms to play games implemented in other languages
and/or hosted remotely. Uses JSON over [ZeroMQ](https://zeromq.org/) for
communication between games & agents.

Games are played sychronously in a request-response format. The game server
should initialise the game and wait for network bot(s) to start making requests.

This example code includes a server hosting a game of tic tac toe, and a few
tests of random and MCTS bots playing the game.


# quick start
```sh
uv run tests.py
uv run performance_comparison.py
uv run play_one_verbose_game.py

uv run client.py  # connect to remote game server
```


# performance
- as you'd expect, this is slow. Games run 50-100 slower.
- using IPC vs TCP transports in ZMQ makes no difference
