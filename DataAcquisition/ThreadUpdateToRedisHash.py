
# -*- coding: utf-8 -*- 

import threading
import time
import redis
import xlrd

conn = redis.Redis('localhost')

class PeriodicSensor ():
  
    def __init__ (self, delay,file,rowindex,colnameindex,colvalueindex,by_name):
        self.next_call = time.time()
        self.delay = delay
        self.data=self.open_excel(file)
        self.rowindex=rowindex
        self.colnameindex=colnameindex
        self.colvalueindex=colvalueindex
        self.table = self.data.sheet_by_name(by_name)
        self.nrows = self.table.nrows #����
        self.taglist=self.excel_tagname_byname()
        self.sheetname=by_name
        print(self.sheetname)
      
    def open_excel(self,file):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception as e:
            print (e)


    def excel_tagname_byname(self):
        taglist =[]
        for rownum in range(self.rowindex,self.nrows):
            tagdef ={'name':u'','value':''}
            tagdef['name']=self.table.cell(rownum,self.colnameindex).value
            taglist.append(tagdef)
        return taglist
        
     
    def excel_tagvalue_byname(self):
        taglist =[]
        for rownum in range(self.rowindex,self.nrows):
            tagdef ={'name':u'','value':''}
            tagdef['name']=self.table.cell(rownum,self.colnameindex).value
            tagdef['value']=self.table.cell(rownum,self.colvalueindex).value
            taglist.append(tagdef)
      
        if self.sheetname=='DCS1AI':
                if self.colvalueindex==5: 
                    self.colvalueindex=7
                elif  self.colvalueindex==7:
                    self.colvalueindex=5  
        
        if self.sheetname=='DCS2AI':
                self.colvalueindex=self.colvalueindex+1  
                if self.colvalueindex>30: 
                    self.colvalueindex=6
                    
        return taglist   
 
    def  SendToRedisHash(self):
        tagvaluelist=self.excel_tagvalue_byname()
        pipe =conn.pipeline()
        for element in tagvaluelist:
            pipe.hset(element['name'],'value',element['value'])
        pipe.execute() 
        
        print(tagvaluelist[0])
        print(tagvaluelist[len(tagvaluelist)-1])
  
    def worker(self):
        self.SendToRedisHash()
        self.next_call = self.next_call + self.delay
        threading.Timer( self.next_call - time.time(), self.worker ).start()

if __name__ == "__main__": 
   
    rowindex=2
    colnameindex=2
    colvalueindex=5
    
    SensorU1AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'DCS1AI',)
    SensorU1AI.worker()
      
    SensorU1CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'1CAL',)
    SensorU1CO.worker()
   
    colvalueindex=6
    SensorU2AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'DCS2AI',)
    SensorU2AI.worker()
    
    colvalueindex=5
    SensorU2CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'2CAL',)
    SensorU2CO.worker()
    
    SensorU3AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'DCS3AI',)
    SensorU3AI.worker()
    
    SensorU3CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'3CAL',)
    SensorU3CO.worker()
  
    SensorU4AI = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'DCS4AI',)
    SensorU4AI.worker()
    
    SensorU4CO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'4CAL',)
    SensorU4CO.worker()
    
    SensorPLTCO = PeriodicSensor (2,u'./cs_tag_all.xlsx',rowindex,colnameindex,colvalueindex,u'PLANT',)
    SensorPLTCO.worker()