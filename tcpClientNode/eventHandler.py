from socket import Socket
import TcpParser
import constants

class EventHandler:
    def __init__(soc):
        self.soc = soc
        self.tcpParser = TcpParser()
    

    def listenForData():
        while(True):
            time.sleep(constants.DATA_LISTEN_FREQ)
            data = self.soc.recv(constants.SOCK_RECV_SIZE_IN_BYTES)
            if not data:
                print('\r{}:'.format(ssl_sock.getpeername()),'disconnected')
            else:
                self.tcpParser.addToBuffer(data)
                msg = self.tcpParser.checkIfMessageRecieved()
                if(msg) {
                    processMsg(msg)
                }
    
    def processMsg(msg):
        jsonMsg = json.loads(str(msg))

