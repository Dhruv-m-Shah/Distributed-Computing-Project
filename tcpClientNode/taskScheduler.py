
class taskScheduler:
    def __init__(self, mutex, queue):
        self.mutex = mutex
        self.queue = queue
        startScheduler()
    

    def startScheduler():
        while(True):
            mutex.acquire()
            if(len(self.queue.taskQueue) > 0):
                task = self.queue.pop()
                try:
                    exec(task["pythonScript"])
                except Exception as e:
                    print(e)
