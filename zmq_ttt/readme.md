# remote tic tac toe using ZMQ

What I want
- game server implemented in remote env.
- use openspiel bots to play remote game

# how it works
- bot client -> game server
- server plays as much of game as possible, until next blocking wait for client
  request
- client can request current state, legal actions, do_action

# try it out
```sh
# in one terminal:
python game_server.py
# in another
python bot_client.py
```

# performance
Not great! Local (in same process) gets ~10k games/sec. Over ZMQ on the same
machine gets ~150. Roughly 100 times slower. Using IPC vs TCP transports in ZMQ
makes no difference.


# todo
- implement RemoteState.clone
  - implement get_state
  - pass state with other methods
  - implement clone
- implement remote mcts bot
- make sure random bot still works
- try inproc transport
- ideas to improve performance
  - send legal actions with state
  - more efficient (de)serialiser
- server should have no references to openSpiel
