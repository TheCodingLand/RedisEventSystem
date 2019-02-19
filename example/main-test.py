from redisEventManager import redisEventManager
from random import choice
import string

redis_host='localhost'
def work(data):
    print (data)

events = redisEventManager(redis_host)
id= ''.join([choice(string.ascii_letters) for i in range(10)])

# arguments : channelToSendCommandTo, IdOfTheReturnedCommand, a dictionnary that will be passed to the work function; 
result = events.publish('langdetect',id,{ "text": "this is a test2 text and should detect English", "nbofresults" : 1 }, work)
