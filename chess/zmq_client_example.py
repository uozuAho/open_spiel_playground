import zmq

ctx = zmq.Context()
socket = ctx.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
  msg = input()
  socket.send(msg.encode('UTF-8'))
  response = socket.recv().decode('UTF-8')
  print(response)
