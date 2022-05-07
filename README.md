
# pyE2EE 1.0.0

End To End Encryption in Python.



## Features

- Cross platform (i think)
- RSA and AES Encryption
- Examples provided
## Usage/Examples

```python
import pyE2EE

```


### Server Side
```python

def client_loop(server,cli):
  pass # do stuff

server = pyE2EE.Server(port,client_loop) # client_loop will be called giving args server-obj and client 

server.TotalCons        # gives number of total connections
server.clients          # is a list of all [client, publckey-of-the-cli]
server.send(client,msg) # sends msg
server.recv(client)     # recvs msg
server.sendall(msg)     # send all connected clients
server.close(client)    # close a connection
```

### Client Side
```python
client = pyE2EE.Client(server_ip,port) 

client.send(msg)  # send msg to server
client.recv()     # recv msg from server
client.close()    # close connection with server

```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@Merwin](https://www.github.com/mastercodermerwin)

