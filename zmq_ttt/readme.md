# remote tic tac toe using ZMQ

What I want
- game server implemented in remote env.
- use openspiel bots to play remote game

# todo
- ttt server: use ttt from openspiel
  - allow a client to connect as player 0
  - server creates player 1
  - allow client to make first move
    - client requests legal actions
    - server responds
    - client chooses an action
- compare speeds
