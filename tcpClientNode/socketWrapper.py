import socket, ssl, pprint
import time
import json
import constants



class Socket:
    def __init__(url, port, self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = ssl.wrap_socket(this.soc,
                                ca_certs="../certs/ca/ca.crt",
                                cert_reqs=ssl.CERT_REQUIRED)
        ssl_sock.connect((url, port)) # url is localhost for localtesting and port is 8000