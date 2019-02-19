from redisEventManager import redisEventManager
import os
import threading

from worker.sentences import worker
redis_host= 'localhost'
channel = 'sentences'

def work(item):
    w=worker()
    w.run(item)

def run():
    events= redisEventManager(redis_host)
    events.listen(f'{channel}*', work)
if __name__=='__main__':
    run()

