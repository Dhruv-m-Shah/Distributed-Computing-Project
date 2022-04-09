import socket, ssl, pprint
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="../certs/ca/ca.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect(('localhost', 8000))

pprint.pprint(ssl_sock.getpeercert())

# note that closing the SSLSocket will also close the underlying socket
#ssl_sock.close()

while(True):
    time.sleep(10)
    ssl_sock.send(b'testtest')