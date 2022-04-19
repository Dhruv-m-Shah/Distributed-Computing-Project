import constants

class TcpParser:

    def __init__(self):
        self.buffer = b''
    
    def addToBuffer(self, recvedData):
        self.buffer += recvedData
    
    def checkIfMessageRecieved(self):
        sizeOfMessage = None
        if(len(self.buffer) >= constants.CONTENT_SIZE_LEN):
            sizeOfMessage = int(self.buffer[:constants.CONTENT_SIZE_LEN])
        
        if(sizeOfMessage):
            if(len(self.buffer) >= sizeOfMessage + constants.CONTENT_SIZE_LEN):
                message = str(self.buffer[constants.CONTENT_SIZE_LEN : (constants.CONTENT_SIZE_LEN + sizeOfMessage)])
                return message
        
        return sizeOfMessage

