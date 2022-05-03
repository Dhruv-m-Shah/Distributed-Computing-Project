import threading
import constants
import time
class TaskScheduler:
    def __init__(self, mutexQueue, queue, finishedTaskHandler):
        self.mutexQueue = mutexQueue
        self.queue = queue
        self.finishedTaskHandler = finishedTaskHandler
        self.schedulerThread = threading.Thread(target=self.startScheduler, name="scheduler", args=[self.mutexQueue, self.queue, self.finishedTaskHandler])
        self.schedulerThread.start()
    
    def startScheduler(self, mutexQueue, queue, finishedTaskHandler):
        while(True):
            mutexQueue.acquire()
            task = None
            if(len(queue.taskQueue) > 0):
                task = queue.pop()
                resp = None
                try:
                    exec(task["pythonScript"])
                    resp = constants.SUCCESS_RESP
                except Exception as e:
                    resp = e
            mutexQueue.release()
            if(task):
                finishedTaskHandler.sendFinishedStatus(task, resp)
            time.sleep(1)
