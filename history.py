import json
import pymongo
import api

tag = "CTSVRMS01"



def historydata():
    api.findlastHour("CTSVRMS01",1)
    return api.resp

 
       
