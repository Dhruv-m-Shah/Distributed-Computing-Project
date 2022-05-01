import constants
import json
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

    def conv16ByteStr(self, string):
        if(len(string) > 16):
            raise Exception("Too many bytes in string")
        while(len(string) < 16):
            string  = "0" + string
        return string

    def formatTcpMessage(self, msg):
        jsonStr = json.dumps(msg)
        bytesStr = str.encode(jsonStr)
        lenByte = str.encode(self.conv16ByteStr(str(len(bytesStr))))
        return lenByte + bytesStr
