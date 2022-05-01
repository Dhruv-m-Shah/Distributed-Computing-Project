from tcpParser import TcpParser
from threading import Thread, Lock
from taskQueue import TaskQueue
from eventHandler import EventHandler
import constants
from taskScheduler import TaskScheduler
from heartBeat import HeartBeat
import socket, ssl, pprint
import time
import json 

mutexQueue = Lock()
mutexSocket = Lock()
taskQueue = TaskQueue()
scheduler = TaskScheduler(mutexQueue, taskQueue)
tcpParser = TcpParser()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="../certs/ca/ca.crt",
                           cert_reqs=ssl.CERT_REQUIRED)

ret = ssl_sock.connect_ex(('localhost', 8000))
print(ret)
ssl_sock.setblocking(0)
time.sleep(1)
heartBeat = HeartBeat(ssl_sock, mutexQueue, mutexSocket, tcpParser, taskQueue)
print("ASD")
eventHandler = EventHandler(ssl_sock, mutexQueue, mutexSocket, taskQueue)