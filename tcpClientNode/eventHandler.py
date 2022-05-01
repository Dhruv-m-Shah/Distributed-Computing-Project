from tcpParser import TcpParser
from threading import Thread, Lock
import socket, ssl, pprint
import constants
import threading
import time
import select

class EventHandler:
    def __init__(self, soc, mutexQueue, mutexSocket, queue):
        self.soc = soc
        self.tcpParser = TcpParser()
        self.mutexQueue = mutexQueue
        self.mutexSocket = mutexSocket
        self.listenForData = threading.Thread(target=self.listenForData,
                                                name="listenForData", args=[self.soc, self.mutexQueue, self.mutexSocket, self.tcpParser])
        self.listenForData.start()

    def listenForData(self, soc, mutexQueue, mutexSocket, tcpParser):
        while(True):
            print("A")
            time.sleep(constants.DATA_LISTEN_FREQ)
            mutexSocket.acquire()
            data = 0
            try:
                data = soc.recv(constants.SOCK_RECV_SIZE_IN_BYTES)
                print(data)
            except Exception as e:
                print(e)
            mutexSocket.release()
                
    
    def processMsg(msg):
        jsonMsg = json.loads(str(msg))
        if(jsonMsg["type"] == constants.TASKTYPE):
            processTaskMsg(jsonMsg)
    
    def processTaskMsg(msg):
        self.mutexQueue.acquire()
        self.queue.add(msg)
        self.mutexQueue.release()


