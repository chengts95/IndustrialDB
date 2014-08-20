from data_point import data_point
from datetime import datetime, time, timedelta
import pymongo
import random
import sys
from threading import Thread, Timer
import time


c=pymongo.MongoClient('127.0.0.1', 27017)
db=c.mydb
print("pre alloc init")
id_hourly='hourly_template'
id_daily='daily_template'
hourly_zero=[('minute.%d'%h,{'count':0,'sum_value':0,'sum_quality':0})for h in range(60)]
hourly_zero+=[('second.%d.%d'%(h,m),{'value':-1000,'quality':-1000})
                     for h in range(60)
                     for m in range(60)]
daily_zero=[('hourly.%d'%h,{'count':0,'sum_value':0,'sum_quality':0})for h in range(24)]
       
db.template.update(

                   {

        
                   '_id':id_hourly,
                   'tag':'ini'
            
                   },
                   {
                       '$set':dict(hourly_zero)

                       },
                   upsert=True
                  )
db.template.update(

                   {

        
                   '_id':id_daily,
                  'tag':'ini'
            
                   },
                   {
                       '$set':dict(daily_zero)
                       },
                   upsert=True
                         )
