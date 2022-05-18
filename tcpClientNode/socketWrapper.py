import socket, ssl, pprint
import time
import json
import constants

class SocketWrapper:
    def __init__(self, url, port, blocking):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Error creating socket: " + str(e))
            sys.exit(1)
        self.ssl_sock = ssl.wrap_socket(self.soc,
                           ca_certs="../certs/ca/ca.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
        try:
            ret = self.ssl_sock.connect_ex((url, port))
        except socket.error as e:
            print("Connection error: " + str(e))
            sys.exit(1)
        self.ssl_sock.setblocking(0) # Make sockets async
    
    def connect(self, url, port):
        self.ssl_sock.connect((url, port))

    def recv(self, byteSize):
        data = self.ssl_sock.recv(constants.SOCK_RECV_SIZE_IN_BYTES)
        return data
    
    def write(self, writableStr):
        self.ssl_sock.write(writableStr)
    
    def send(self, writableStr):
        self.ssl_sock.send(writableStr)