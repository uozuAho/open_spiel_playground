# remote tic tac toe using ZMQ

Work in progress. Code is very messy, just trying to prove that this is
feasible.

What I want
- game server implemented in remote env.
- use openspiel bots to play remote game

# how it works
- bot client -> game server
- server plays as much of game as possible, until next blocking wait for client
  request

# try it out
```sh
# in one terminal:
python game_server.py
# in another
python bot_client.py
```

# performance
Not great!
- local (in same process) random vs random bots gets ~10k games/sec
- over ZMQ, random vs random bots gets ~200 games/sec
- using IPC vs TCP transports in ZMQ makes no difference

# todo
- is remote mcts working? should win most games
  - hmm seems not. try local example
    - client needs to send state
- make sure random bot still works
- try inproc transport: where is the performance loss?
- ideas to improve performance
  - more efficient (de)serialiser?
- server should have no references to openSpiel
