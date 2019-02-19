from utils.redisEventManager import redisEventManager
import os
import threading
channel = os.getenv("channel")
channel = 'sentence'
from worker.sentences import worker
redis_host= 'tina-redis'
redis_host= 'localhost'

class Listener(threading.Thread):
    def __init__(self, channel):
        threading.Thread.__init__(self)
    
    def work(self, item):
        w=worker()
        w.run(item)

    def run(self):
        events= redisEventManager(redis_host)
        events.listen('sentences*', self.work)

if __name__ == "__main__":
    if channel:
        client = Listener(channel)
        client.start()

