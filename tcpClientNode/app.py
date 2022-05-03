from tcpParser import TcpParser
from threading import Thread, Lock
from taskQueue import TaskQueue
from eventHandler import EventHandler
from finishedTaskHandler import FinishedTaskHandler
import constants
from taskScheduler import TaskScheduler
from heartBeat import HeartBeat
import socket, ssl, pprint
import time
import json 

mutexQueue = Lock()
mutexSocket = Lock()
taskQueue = TaskQueue()
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
finishedTaskHandler = FinishedTaskHandler(ssl_sock, tcpParser, mutexSocket)
scheduler = TaskScheduler(mutexQueue, taskQueue, finishedTaskHandler)
heartBeat = HeartBeat(ssl_sock, mutexQueue, mutexSocket, tcpParser, taskQueue)
eventHandler = EventHandler(ssl_sock, mutexQueue, mutexSocket, taskQueue)