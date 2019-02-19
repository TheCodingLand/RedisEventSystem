from utils.redisEventManager import redisEventManager
redis_host='localhost'
def work(data):
    print (data)
events = redisEventManager(redis_host)
result = events.publish('sentences','12',{ "text": "this is a test2 key", "nbofitems" : 1 }, work)