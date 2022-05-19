import socket, ssl, pprint
import time
import json
import sys
import constants

class SocketWrapper:
    def __init__(self, url, port, blocking, max_retries = 3):
        self.max_retries = max_retries
        self.url = url
        self.port = port
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Error creating socket: " + str(e))
            sys.exit(1)
        self.ssl_sock = ssl.wrap_socket(self.soc,
                           ca_certs="../certs/ca/ca.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
        ret = self.ssl_sock.connect_ex((url, port))
        if(ret != 0):
            print("Connection error: " + str(ret))
            sys.exit(1)
        self.ssl_sock.setblocking(blocking) # Make sockets async
    
    def connect(self, url, port):
        ret = 0
        for i in range(self.max_retries):
            ret = self.ssl_sock.connect((url, 8001))
            if(ret == 0):
                return
        print("Connection error: " + str(ret))
        sys.exit(1)

    def recv(self, byteSize):
        data = self.ssl_sock.recv(constants.SOCK_RECV_SIZE_IN_BYTES)
        return data
    
    def write(self, writableStr):
        self.ssl_sock.write(writableStr)
    
    def send(self, writableStr):
        self.ssl_sock.send(writableStr)