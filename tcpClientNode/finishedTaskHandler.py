import config
import constants
class FinishedTaskHandler:
    def __init__(self, soc, tcpParser, mutexSoc):
        self.soc = soc
        self.tcpParser = tcpParser
        self.mutexSoc = mutexSoc
    


    def sendFinishedStatus(self, msg, taskStatus):
        resp = {
            "key": config.TASK_PROVIDER_KEY,
            "name": config.TASK_PROVER_NAME,
            "taskName": msg["taskName"],
            "taskIssuerName": msg["taskIssuerName"],
            "taskStatus": taskStatus,
            "type": constants.TASK_FINISHED
        }
        writableStr = self.tcpParser.formatTcpMessage(resp)
        self.mutexSoc.acquire()
        self.soc.sendall(writableStr)
        self.mutexSoc.release()

        