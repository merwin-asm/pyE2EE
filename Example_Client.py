import pyE2EE
import socket

client = pyE2EE.Client(socket.gethostbyname(socket.gethostname()),port=1113)


msg = client.recv()
print(msg)
client.send("Hello")
client.close()
