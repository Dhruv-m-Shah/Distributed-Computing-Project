from tcpParser import TcpParser
from threading import Thread, Lock
import socket, ssl, pprint
import constants
import threading
import time
import select
import json

class EventHandler:
    def __init__(self, soc, mutexQueue, mutexSocket, queue):
        self.soc = soc
        self.tcpParser = TcpParser()
        self.mutexQueue = mutexQueue
        self.mutexSocket = mutexSocket
        self.queue = queue
        self.listenForData = threading.Thread(target=self.listenForData,
                                                name="listenForData", args=[self.soc, self.mutexQueue, self.mutexSocket, self.tcpParser])
        self.listenForData.start()

    def listenForData(self, soc, mutexQueue, mutexSocket, tcpParser):
        while(True):
            time.sleep(constants.DATA_LISTEN_FREQ)
            mutexSocket.acquire()
            data = 0
            try:
                data = soc.recv(constants.SOCK_RECV_SIZE_IN_BYTES)
                tcpParser.addToBuffer(data)
                msg = tcpParser.checkIfMessageRecieved()
                if(msg):
                    self.processMsg(msg)
            except Exception as e:
                print(e)
            mutexSocket.release()
                
    
    def processMsg(self, msg):
        print(str(msg)[0])
        print("A")
        jsonMsg = json.loads(msg, encoding='utf-8')
        print(jsonMsg)
        if(jsonMsg["type"] == constants.TASKTYPE):
            self.processTaskMsg(jsonMsg)
    
    def processTaskMsg(self, msg):
        self.mutexQueue.acquire()
        self.queue.add(msg)
        self.mutexQueue.release()


