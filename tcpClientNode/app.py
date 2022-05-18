from tcpParser import TcpParser
from threading import Thread, Lock
from taskQueue import TaskQueue
from eventHandler import EventHandler
from finishedTaskHandler import FinishedTaskHandler
import constants
from taskScheduler import TaskScheduler
from heartBeat import HeartBeat
import socket, ssl, pprint
from socketWrapper import SocketWrapper
import time
import json
import sys
import configTaskClient as config

if(len(sys.argv) < 3):
    print("Need to provide both user name and key")
    sys.exit(1)

config.TASK_PROVER_NAME = sys.argv[1]
config.TASK_PROVIDER_KEY = sys.argv[2]

mutexQueue = Lock()
mutexSocket = Lock()
taskQueue = TaskQueue()
tcpParser = TcpParser()

url = "localhost"
port = 8000
isBlocking = False

ssl_sock = SocketWrapper(url, port, isBlocking)

time.sleep(1)
finishedTaskHandler = FinishedTaskHandler(ssl_sock, tcpParser, mutexSocket)
scheduler = TaskScheduler(mutexQueue, taskQueue, finishedTaskHandler)
heartBeat = HeartBeat(ssl_sock, mutexQueue, mutexSocket, tcpParser, taskQueue)
eventHandler = EventHandler(ssl_sock, mutexQueue, mutexSocket, taskQueue)