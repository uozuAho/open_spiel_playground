# remote tic tac toe using ZMQ

What I want
- game server implemented in remote env.
- use openspiel bots to play remote game

# how it works
- bot client -> game server
- server plays as much of game as possible, until next blocking wait for client
  request
- client can request current state, legal actions, do_action

# todo
- compare speed of local_example vs client-server
  - rate of games played
- implement remote mcts bot
- extract usable interfaces
  - eg. should be able to do `bot = RemoteGameBot(MctsBot(...))`
