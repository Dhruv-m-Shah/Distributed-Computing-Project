import threading
import time
class TaskScheduler:
    def __init__(self, mutex, queue):
        self.mutex = mutex
        self.queue = queue
        self.schedulerThread = threading.Thread(target=self.startScheduler, name="scheduler", args=[self.mutex, self.queue])
        self.schedulerThread.start()
    
    def startScheduler(self, mutex, queue):
        while(True):
            mutex.acquire()
            if(len(queue.taskQueue) > 0):
                task = queue.pop()
                try:
                    exec(task["pythonScript"])
                except Exception as e:
                    print(e)
            mutex.release()
