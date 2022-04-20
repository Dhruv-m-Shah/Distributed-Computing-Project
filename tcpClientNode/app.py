from tcpParser import TcpParser
from threading import Thread, Lock
from taskQueue import TaskQueue
import constants
from taskScheduler import TaskScheduler

mutex = Lock()
taskQueue = TaskQueue()
scheduler = TaskScheduler(mutex, taskQueue)