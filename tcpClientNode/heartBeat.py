import threading
import time

class HeartBeat:
    def __init__(self, soc, mutexQueue, mutexSocket, tcpParser, queue):
        self.soc = soc
        self.mutexQueue = mutexQueue
        self.mutexSocket = mutexSocket
        self.tcpParser = tcpParser
        self.queue = queue
        self.heartBeatThread = threading.Thread(target=self.startHeartBeat,
                                                name="heartBeat", args=[self.soc, self.mutexQueue, self.mutexSocket, self.tcpParser, self.queue])
        self.heartBeatThread.start()

    def startHeartBeat(self, soc, mutexQueue, mutexSocket, tcpParser, queue):
        while(True):
            time.sleep(2)
            mutexQueue.acquire()
            print(queue.length())
            taskProviderHeartBeat = {
                "name": "test123",
                "type": "heartbeat", 
                "key": "test123",
                "tasksInQueue": queue.length(),
                "providerState": "OK"
            }
            mutexQueue.release()
            formattedTcpMessage = tcpParser.formatTcpMessage(taskProviderHeartBeat)
            mutexSocket.acquire()
            soc.send(formattedTcpMessage)
            mutexSocket.release()



    