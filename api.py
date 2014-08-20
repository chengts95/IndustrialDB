import time
import json

import redis
import pymongo

client = pymongo.MongoClient('localhost', 27017)
realtimeDB=redis.Redis('localhost')
db = client.myTest
coll = db.messageSensor

resp = {"type": "collection", "data":[]}
def makeResp (m, query):
  resp['data'] = []
  resp['query']=query
  for d in m:
    print (d)
    resp['data'].append(d)


def findValsTag ( tag):
    m= coll.find ({ "tag": tag},{'ts':1,'val':1,'quality':1 ,'_id':0}).sort("ts",1).limit(10)
    makeResp(m, "findValsTag")

def findMinuteValsTag ( tag):
    tmax = time.time()
    tmin = tmax - 60
    m = coll.find ({ "tag": tag, "ts": {"$gte":tmin, "$lt":tmax}},{'ts':1,'val':1, 'quality':1,'_id':0}).sort("ts",1)
    makeResp(m, "findMinuteValsTag")

def findHourValsTag ( tag):
    tmax = time.time()
    tmin = tmax - 3600
    m= coll.find ({"tag": tag, "ts": {"$gte":tmin, "$lt":tmax}},{'ts':1,'val':1, 'quality':1,'_id':0}).sort("ts",1)
    makeResp(m, "findHourValsTag")

def findLastValsTag ( tag):
    m = coll.find({"tag":tag},{'ts':1,'val':1, 'quality':1,'_id':0}).sort("ts",-1).limit(1)
    makeResp(m, "findLastValsTag")

# http://cookbook.mongodb.org/patterns/date_range/

def findByPeriod (tag, min0, max0, sort):
  if ( max0 >= min0): 
    m= coll.find ({"tag":tag, "ts": {"$gt":min0, "$lt":max0}},{'ts':1,'val':1, 'quality':1,'_id':0}).sort("ts",sort)
    makeResp (m, "findByPeriod")

def findMinute (tag, ts, sort):
  tm = ts - 60
  findByPeriod (tag, tm, ts, sort)
  
def findHour (tag, ts, sort):
  tm = ts - 3600
  findByPeriod (tag, tm, ts, sort)
 

def findlastMinute (tag,sort):
   ts = time.time () - 60
   m = coll.find({"tag":tag, "ts": {"$gt":ts}}).sort("ts",sort)
   makeResp(m, "findlastMinute")

def findlastHour ( tag,sort):
   ts = time.time () - 3600 
   m = coll.find({'tag':tag,"ts": {"$gt":ts}},{'_id':0}).sort("ts",sort)
   makeResp(m, "findlastHour")


def findLast (tag):
   m = coll.find({"tag":tag}).sort("ts",-1).limit(1)
   makeResp(m, "findLast")
   
def findFirst (tag):
   m = coll.find({"tag":tag}).sort("ts",1).limit(1)
   makeResp(m, "findFirst")

def findCurrent (tag):
   m = json.loads(bytes.decode(realtimeDB.get(tag))) 
   makeResp(m, "findCurrent")

def calAverage (listVal):
   pass


def average (data):
  average = 0
  if len (resp['data']):
    for d in resp['data']:
      average += d['val']

    average = average/len(resp['data']) 
  print (average)

def averageLastHour (tag):
  findlastHour (tag,1)
  average (resp['data'])

def averageLastMinute (tag):
  findlastMinute (tag,1)
  average (resp['data'])


def mainT ():
  #findClients()
 
   #findLast ("CTSVRMS01")

 # findFirst ("CTSVRMS01")
   #findlastHour("CTSVRMS01",1)
   #averageLastMinute ("CTSVRMS01")
#  findValsTag ("CTSVRMS01" )
   findHourValsTag ("CTSVRMS01")
 # findLastValsTag ("CTSVRMS01")
   print (resp)

if __name__ == "__main__":
  mainT()
  pass

