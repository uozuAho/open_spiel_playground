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
python server.py
# in another
python random_client.py
```

# performance
Not great! Local (in same process) gets ~10k games/sec. Over ZMQ on the same
machine gets ~150. Roughly 100 times slower. Using IPC vs TCP transports in ZMQ
makes no difference.


# todo
- extract usable interfaces
  - eg. should be able to do `bot = RemoteGameBot(MctsBot(...))`
- implement remote mcts bot
- ideas to improve performance
  - send legal actions with state
