# -*- coding: utf-8 -*- 
import xlrd
import redis

conn = redis.Redis('localhost')

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (e)

def excel_tagdef_table_byname(excelfile,rowindex,colnameindex,coldescindex,by_name):
    table = excelfile.sheet_by_name(by_name)
    nrows = table.nrows  
    tagdeflist =[]
    for rownum in range(rowindex,nrows):
        tagdef ={'name':u'','desc':u''}
        tagdef['name']=table.cell(rownum,colnameindex).value
        tagdef['desc']=table.cell(rownum,coldescindex).value
        tagdeflist.append(tagdef)
    return tagdeflist


def TagDefToRedisHashKey(tagdef):
    pipe =conn.pipeline()
    for element in tagdef:
#        conn.hmset(element['name'],{'desc':element['desc'],'value':"-10000",'ts':""})
        pipe.hmset(element['name'],{'desc':element['desc'],'value':"-10000",'ts':""})
    pipe.execute()    

def TagDefFromRedisHash(tagdef):
    tagdeflist =[]
    for element in tagdef:
        htag=conn.hgetall(element['name'])
        tagdeflist.append(htag)
    return tagdeflist

def UnitTagDefToRedisHash(unitid,AI,DI,CO):
    tagdeflist =excel_tagdef_table_byname(data,rowbegindex,colnameindex,coldescindex,AI)
    TagDefToRedisHashKey(tagdeflist)

    AICount=len(tagdeflist)
    print(tagdeflist[AICount-1])
   
    tagdeflist =excel_tagdef_table_byname(data,rowbegindex,colnameindex,coldescindex,DI)
    TagDefToRedisHashKey(tagdeflist)
 
    DICount=len(tagdeflist)
    print(tagdeflist[DICount-1])
    
    tagdeflist =excel_tagdef_table_byname(data,rowbegindex,colnameindex,coldescindex,CO)
    TagDefToRedisHashKey(tagdeflist)
 
    COCount=len(tagdeflist)
    print(tagdeflist[COCount-1])
    
    print('u',unitid,' AICount= ',AICount,'DICount= ',DICount,'COCount= ',COCount,'KeyCount= ',conn.dbsize())

def AUXTagDefToRedisHash(sheetname):
    tagdeflist =excel_tagdef_table_byname(data,rowbegindex,colnameindex,coldescindex,sheetname)
    TagDefToRedisHashKey(tagdeflist)

    TagCount=len(tagdeflist)
    print(tagdeflist[TagCount-1])
    print(sheetname,' Count= ',TagCount,'KeyCount= ',conn.dbsize())
        
       
if __name__ == "__main__": 
    
    rowbegindex=2
    colnameindex=2
    coldescindex=1
    
    data = open_excel(u'./cs_tag_all.xlsx')
    
    UnitTagDefToRedisHash(1,u'DCS1AI',u'DCS1DI',u'1CAL')
    UnitTagDefToRedisHash(2,u'DCS2AI',u'DCS2DI',u'2CAL')
    UnitTagDefToRedisHash(3,u'DCS3AI',u'DCS3DI',u'3CAL')
    UnitTagDefToRedisHash(4,u'DCS4AI',u'DCS4DI',u'4CAL')
   
    AUXTagDefToRedisHash(u'PLANT')
    
    AUXTagDefToRedisHash(u'RTU')
    AUXTagDefToRedisHash(u'RANLIAO')
    AUXTagDefToRedisHash(u'ECS')
    AUXTagDefToRedisHash(u'1ECS')
    AUXTagDefToRedisHash(u'3ECS')
    AUXTagDefToRedisHash(u'TL12DCS')
    AUXTagDefToRedisHash(u'TL34DCS')
    AUXTagDefToRedisHash(u'HUAXDCS')
    AUXTagDefToRedisHash(u'CANATAL')
    AUXTagDefToRedisHash(u'CANATAL2')
    
   
    
    
    
