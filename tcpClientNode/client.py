import socket, ssl, pprint
import time
import json 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="../certs/ca/ca.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect(('localhost', 8000))

pprint.pprint(ssl_sock.getpeercert())

# note that closing the SSLSocket will also close the underlying socket
#ssl_sock.close()

taskProviderHeartBeat = {
   "name": "test123",
   "type": "heartbeat", 
   "key": "test123",
   "tasksInQueue": 4,
   "providerState": "OK"
}

taskClientTask = {
   "type": "task",
   "key": "test123",
   "taskName": "test123", 
   "taskClientName": "test1234",
   "computingProviderNames": ["test123"],
   "computingProviderPasswords": ["test123"],
   "pyScripts": ["print(\"test\")"] 
}

def conv16ByteStr(string):
   if(len(string) > 16):
      raise Exception("Too many bytes in string")
   while(len(string) < 16):
      string  = "0" + string
   return string

while(True):
   time.sleep(2)
   jsonStr = json.dumps(taskClientTask)
   bytesStr = str.encode(jsonStr)
   lenByte = str.encode(conv16ByteStr(str(len(bytesStr))))
   ssl_sock.write(lenByte + bytesStr)
   time.sleep(1)
   print(ssl_sock.recv(1024))
   print(ssl_sock.pending())
   break

    