"""
pyE2EE 1.0.0
A module for end-2-end-encryption.
Author : Merwin Mathews
"""


import rsa
import socket
import threading


class Server:
    def __init__(self,port=5432,client_loop=None):
        try:
            self.PublicKey , self.PrivateKey = Utils().load_keys()
        except:
            Utils().generate_keys_save()
            self.PublicKey , self.PrivateKey = Utils().load_keys()

        # if client_loop != None:
        self.client_loop = client_loop

        # VARS
        self.TotalCons = 0
        self.clients = []


        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', port))
        self.server.listen()
        self.connection_loop()


    def connection_loop(self):
        while True:
            c, addr = self.server.accept()
            c.send(self.PublicKey.save_pkcs1("PEM"))
            client_public_key = rsa.PublicKey.load_pkcs1(c.recv(3000))
            self.clients.append([c,client_public_key])
            t = threading.Thread(target=self.client_loop,args=[self,c])
            t.daemon = True
            t.start()
            self.TotalCons += 1
            print(f"Total Connections : {self.TotalCons}")

    def sendall(self,data):
        for e in self.clients:
            self.send(e,data.encode())

    def send(self,client,data):
        data = Utils().encrypt(data,self.get_publickey(client))
        client.send(data)

    def recv(self,client):
        data = Utils().decrypt(client.recv(3000), self.PrivateKey)
        return data

    def sendping(self,cli):
        self.send(cli,".")

    def close(self,c):
        self.clients.remove([c,self.get_publickey(c)])
        c.close()
        self.TotalCons -= 1
        print(f"Total Connections : {self.TotalCons}")

    def get_publickey(self,client):
        for e in self.clients:
            if e[0] == client:
                return e[1]

class Client:
    def __init__(self,host_ip,port=5432):
        self.Client_Public_Key , self.Client_Private_Key = Utils().generate_keys()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host_ip, port))
        self.init_connection()


    def init_connection(self):
        self.Server_PublicKey = rsa.PublicKey.load_pkcs1(self.client.recv(3000))
        self.client.send(self.Client_Public_Key.save_pkcs1("PEM"))


    def send(self,data):
        self.client.send(Utils().encrypt(data,self.Server_PublicKey))

    def recv(self):
        return Utils().decrypt(self.client.recv(3000),self.Client_Private_Key)

    def close(self):
        self.client.close()

class Utils:


    def generate_keys_save(self):
        pubkey,privkey = rsa.newkeys(1024)
        with open("pubkey.pem","wb") as f:
            f.write(pubkey.save_pkcs1("PEM"))
            f.close()
        with open("privkey.pem", "wb") as f:
            f.write(privkey.save_pkcs1("PEM"))
            f.close()


    def generate_keys(self):
        pubkey,privkey = rsa.newkeys(1024)
        return pubkey,privkey



    def load_keys(self):
        with open("pubkey.pem", "rb") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
            f.close()
        with open("privkey.pem", "rb") as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())
            f.close()
        return pubkey , privkey



    def encrypt(self,data,pubkey):
        return rsa.encrypt(data.encode("ascii"),pubkey)


    def decrypt(self,data,privkey):
        try:
            return rsa.decrypt(data,privkey).decode("ascii")
        except:
            return False

