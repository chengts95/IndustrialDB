# 
# To see how to interface arduino with python scripts
# http://playground.arduino.cc/Interfacing/Python
#
import pymongo
from data_point  import data_point
from datetime  import datetime
import json
import random
import redis
import time

import powermonitor


conn = redis.Redis('localhost')
client = pymongo.MongoClient('localhost', 27017)
db=client.myTest
collection=db.messageSensor
point_list=[powermonitor.vrms]
# configure the serial connections (the parameters differs on the device you are connecting to)
print("init...")


def toRedis(pointlist):
  for point in pointlist:  
      tag=point.Tag
      conn.set(tag,json.dumps({}))
  x=0
  time.sleep(1)
  while True:
    time.sleep(1)
    
    for point in pointlist:
        
        val = random.uniform(-10, 10)+220
        
        if(val<point.Exception_max and val>point.Exception_min):
            q=1
        else:
            q=-1
                
        new={'ts':time.time(),'val': val,'quality':q}
        old=json.loads(bytes.decode(conn.get(tag))) 
        conn.set(tag,json.dumps(new)) 
        print(new)
        print(old)
        x+=1
            
        if(old=={}):
            continue  
        else:
            old['tag']=point.Tag
            collection.insert(old,w=0)


toRedis(point_list)



