import pyE2EE

def client_loop(server, cli):
    server.send(cli, "Hello")
    msg = server.recv(cli)
    print(msg)
    server.close(cli)

server = pyE2EE.Server(port=1113,client_loop=client_loop)



