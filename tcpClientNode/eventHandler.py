from socket import Socket
import TcpParser
from threading import Thread, Lock
import constants

class EventHandler:
    def __init__(soc):
        self.soc = soc
        self.tcpParser = TcpParser()
        self.mutex = Lock()
    

    def listenForData():
        while(True):
            time.sleep(constants.DATA_LISTEN_FREQ)
            data = self.soc.recv(constants.SOCK_RECV_SIZE_IN_BYTES)
            if data:
                self.tcpParser.addToBuffer(data)
                msg = self.tcpParser.checkIfMessageRecieved()
                if(msg) {
                    processMsg(msg)
                }
    
    def processMsg(msg):
        jsonMsg = json.loads(str(msg))
        if(jsonMsg["type"] == constants.TASKTYPE):
            processTaskMsg(jsonMsg)
    
    def processTaskMsg(msg):


