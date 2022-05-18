import configTaskClient as config
import constants
class FinishedTaskHandler:
    def __init__(self, soc, tcpParser, mutexSoc):
        self.soc = soc
        self.tcpParser = tcpParser
        self.mutexSoc = mutexSoc
    


    def sendFinishedStatus(self, msg, taskStatus):
        resp = {
            "key": configTaskClient.TASK_PROVIDER_KEY,
            "name": configTaskClient.TASK_PROVER_NAME,
            "taskName": msg["taskName"],
            "taskIssuerName": msg["taskIssuerName"],
            "taskStatus": taskStatus,
            "type": constants.TASK_FINISHED
        }
        print(resp)
        writableStr = self.tcpParser.formatTcpMessage(resp)
        self.mutexSoc.acquire()
        self.soc.write(writableStr)
        self.mutexSoc.release()

        