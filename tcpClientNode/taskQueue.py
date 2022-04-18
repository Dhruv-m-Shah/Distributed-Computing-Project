import constants

class TaskQueue:

    def __init__(self):
        self.taskQueue = []
    
    def add(task):
        self.taskQueue.append(task)
    
    def pop():
        if(len(self.taskQueue) != 0):
            return self.taskQueue.pop(0)
        else:
            return constants.QUEUE_EMPTY
    