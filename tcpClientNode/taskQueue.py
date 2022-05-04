import constants

class TaskQueue:

    def __init__(self):
        self.taskQueue = []

    def length(self):
        return len(self.taskQueue)
    
    def add(self, task):
        print(self.taskQueue)
        self.taskQueue.append(task)
    
    def pop(self):
        if(len(self.taskQueue) != 0):
            return self.taskQueue.pop(0)
        else:
            return constants.QUEUE_EMPTY
    