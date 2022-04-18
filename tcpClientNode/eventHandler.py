from socket import Socket
import constants

class EventHandler:
    def __init__(soc):
        self.soc = soc
    

    def listenForData():
        while(True):
            time.sleep(1)
            data = self.soc.recv(1024)
            if not data:
                print('\r{}:'.format(ssl_sock.getpeername()),'disconnected')
            else:
                print('\r{}:'.format(ssl_sock.getpeername()),data)

