import json

import zmq

ctx = zmq.Context()
socket = ctx.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# send any message to connect
socket.send('hello'.encode('UTF-8'))
response = socket.recv().decode('UTF-8')
print(response)

msg = json.dumps({'type': 'legal_actions'})
socket.send(msg.encode('UTF-8'))
response = socket.recv().decode('UTF-8')
print(response)
