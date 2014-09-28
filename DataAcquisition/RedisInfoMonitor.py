
# -*- coding: utf-8 -*-

import redis

conn = redis.Redis('localhost')

curinfo={'redis_version':' ','connected_clients':'','blocked_clients':' ','keysize':'','used_memory':''}


def RedisInfo():
    
    keysize=conn.dbsize()
    curinfo['keysize']=keysize
   
    info=conn.info('server')
    curinfo['redis_version']=info['redis_version']
    
    info=conn.info('clients')
    curinfo['connected_clients']=info['connected_clients']
    curinfo['blocked_clients']=info['blocked_clients']
    
    
    info=conn.info('memory')
    used_memory=info['used_memory']/1024/1024
    curinfo['used_memory']=used_memory
   
    info=conn.info('cpu')
    curinfo['used_cpu_sys']=info['used_cpu_sys']
    curinfo['used_cpu_user']=info['used_cpu_user']
 
    return curinfo

if __name__ == "__main__": 
    
    print(RedisInfo())
   
    print(conn.dbsize())
    
    i=eval(input("Flush db: 1 ="))
    if i==1: 
        conn.flushdb()
    print(conn.dbsize())
             
             
