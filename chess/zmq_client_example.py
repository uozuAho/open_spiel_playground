import zmq

ctx = zmq.Context()
socket = ctx.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

msg = b'yo!'
print(f'sending "{msg}" to server')
socket.send(msg)
received_msg = socket.recv().decode('UTF-8')
print(f'server said:\n\n{received_msg}')
