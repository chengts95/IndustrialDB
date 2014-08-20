# 
# To see how to interface arduino with python scripts
# http://playground.arduino.cc/Interfacing/Python
#
from IndustrialDB import IndustrialDB
from data_point  import data_point
from datetime  import datetime
import json
import minimalmodbus
import redis
import serial
import time


tag = "TE-01"
conn = redis.Redis('localhost')

client = IndustrialDB()
p1=data_point(
  dict_point={

        'Tag':tag,
        'Desc':'温度传感器１',
        'EngUnit':'0C',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'20',
        'Exception_max':120,
        'Exception_min':-40
  })
point_list=[p1]
# configure the serial connections (the parameters differs on the device you are connecting to)
print("init...")

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) 
instrument.serial.baudrate = 9600   # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 2
instrument.serial.timeout  = 1   # seconds

client.point_config_init([point_list[0].encode()])
client.point_init(datetime.now())

def toRedis(tag):
  
  conn.set(tag,json.dumps({}))
  time.sleep(1)
  while True:
    time.sleep(1)
    val = instrument.read_register(0,1)
    new={'ts':datetime.now().strftime("%Y%m%d%H:%M:%S"),'val': val}
    old=json.loads(bytes.decode(conn.get(tag))) 
    conn.set(tag,json.dumps(new)) 
    print(new)
    print(old)
    if(old=={}):
      continue  
    else:
        point_list[0].value=old['val']
        point_list[0].quality=1
        client.log_timed_value(old['ts'],point_list[0])


toRedis(tag)



