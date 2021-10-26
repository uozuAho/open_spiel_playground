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
- ttt server: use ttt from openspiel
  - allow client to make first move
    - client requests legal actions
    - server responds
    - client requests do_action
- compare speeds
- remote mcts bot. requires storage of state
