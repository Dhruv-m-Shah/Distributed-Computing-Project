from tcpParser import TcpParser
from threading import Thread, Lock
from taskQueue import TaskQueue
from eventHandler import EventHandler
import constants
from taskScheduler import TaskScheduler
import socket, ssl, pprint
import time
import json 

mutex = Lock()
taskQueue = TaskQueue()
scheduler = TaskScheduler(mutex, taskQueue)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="../certs/ca/ca.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect(('localhost', 8000))

eventHandler = EventHandler(ssl_sock, mutex, taskQueue)