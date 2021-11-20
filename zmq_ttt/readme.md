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
# run tests
python tests.py
# run performance comparison of local/remote games
python performance_comparison.py
# run verbose playthrough
python play_one_verbose_game.py

# run a game-playing client that connects to a remote game server
python client.py
```


# performance
- as you'd expect, this is slow. Games run 50-100 slower.
- using IPC vs TCP transports in ZMQ makes no difference
