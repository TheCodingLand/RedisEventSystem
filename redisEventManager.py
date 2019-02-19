import redis
import json
import time
import datetime
class redisEventManager(object):
    """This class implements the logic for redis event job reservation, and hadnling the connection for task results."""

    def __init__(self, redis_host):
        self.data=None
        self.redis = redis.Redis(host=redis_host, decode_responses=True, port=6379)
        self.pubsub = self.redis.pubsub()
        #Subscription will allow us to recieve commands on the registered channel
        
        #a connexion to channel 1 is used to recieve commands for this container.
        #tasks can also be sent to this channel from this containers; other containers also listen to this channel for commands.
        self.redis_in = redis.StrictRedis(
            host=redis_host, decode_responses=True, port=6379, db=1)
        #a connexion to channel 2 is used to send back results from this container's execution.
     
    def dateConverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def listen(self, channel, workFunction):
        """the argument handleKey is a function passed to deal with the Key Value result, args are arguments for the handlekay function"""
        self.pubsub.psubscribe([channel])
        for item in self.pubsub.listen():
            self.data=self.reservation(item)
            if self.data:
                self.data['state'] = 'in progress'
                timestamp = time.time()
                self.data['started'] = timestamp
                job = workFunction(self.data)
                self.data['state'] = "finished"
                timestamp = time.time()
                self.data['finished'] = timestamp
                self.output(channel,self.data['id'],self.data)
    
    def output(self, channel, id, data):
        res = json.dumps(data, default=self.dateConverter)
        self.redis_in.hmset(f"{id}", {"data": res})
        self.redis_in.publish(f"{id}", f"{id}")
        self.redis_in.expire(f"{id}",500)
    
            
    def publish(self, channel, id, data, work):
        """Channel is a general service target, and ID is an identifyer a subscribed client will lisen to updates from """
        
        self.pubsub.psubscribe([id]) 
        res = json.dumps(data, default=self.dateConverter)
        self.redis_in.hmset(f'{channel}.{id}', {"id": f"{id}", "data" : res })
        self.redis_in.publish(f'{channel}.{id}', f'{channel}.{id}')
        self.redis_in.expire(f'{channel}.{id}',500)
        
        for item in self.pubsub.listen():
                if item['data'] != 1:
                    if item['data']==id:
                        result = self.redis_in.hgetall(id)
            
                        result['data'] = json.loads(result['data'])
                        work(result)
                        return True
             
        
    def exit(self):
        self.pubsub.unsubscribe()
        exit()
        
    def reservation(self, item):
        if item['data'] != 1:
            state='ok'
            try:
                data = self.redis_in.hgetall(item['channel'])
                k = self.redis_in.delete(item['channel'])
            except:
                state='already in progress'
                return False
            if k == 0:
                state='already in progress'
                return False
            try:
                data['data'] = json.loads(data['data'])
            except KeyError:
                
                state='already in progress'
                return False
            return data
        return False