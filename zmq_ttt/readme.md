# Demo: OpenSpiel agents play remote tic tac toe game, using ZMQ

Work in progress. Code is very messy, just trying to prove that this is
feasible.

General idea:

```
  ┌────────────┐    ┌───────────────────┐ get game info  ┌────────────────────┐
  │            │    │                   ├───────────────▲│                    │
  │ OpenSpiel  │    │ NetworkBot        │▼───────────────┤ Remote Game Server │
  │            │    │  no more network bot!  │                │                    │
  │     bot  ──┼────┼───► wrapped bot   │                │                    │
  │            │    │                   │                │                    │
  │            │    │                   │   get state    │                    │
  │            │    │                   ├───────────────▲│                    │
  │            │    │                   │▼───────────────┤                    │
  │            │    │                   │                │                    │
  │            │    │                   │                │                    │
  │            │    │                   │                │                    │
  │            │    │                   │  apply action  │                    │
  │            │    │                   │    to state    │                    │
  │            │    │                   ├───────────────▲│                    │
  │            │    │                   │▼───────────────┤                    │
  │            │    │                   │   resultant    │                    │
  │            │    │                   │     state      │                    │
  │            │    │                   │                │                    │
  │            │    │                   │                │                    │
  │            │    │                   │      step      │                    │
  │            │    │                   ├───────────────▲│                    │
  │            │    │                   │▼───────────────┤                    │
  │            │    │                   │  updated game  │                    │
  └────────────┘    └───────────────────┘     state      └────────────────────┘
```

The remote game server can be implemented in any language, and run locally or
remotely. Games are played sychronously in a request-response format. The server
initialises the game and waits for a network bot to start making requests.

# quick start
```sh
# run tests
python tests.py
# run performance comparison of local/remote games
python performance_comparison.py

# run server & client:
# in one terminal:
python game_server.py
# in another:
python bot_client.py
```

# performance
- as you'd expect, this is slow. Playing a local agent against a remote
  agent runs about 50-100 slower than two local agents.
- using IPC vs TCP transports in ZMQ makes no difference

# todo
- network bot change
  - update docs
- fix unclosed zmq context during tests
- cleanup, tests, 'harden'
  - handle bots in either order?
- try random & mcts vs pandemic game
- ideas to improve performance
  - more efficient (de)serialiser?
- server should have no references to openSpiel
