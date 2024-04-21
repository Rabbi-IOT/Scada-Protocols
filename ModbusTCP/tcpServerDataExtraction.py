# pip install pymodbus
# This will install the library
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ModbusException
from pymodbus.transaction import ModbusRtuFramer
import time
import datetime

server = '192.168.0.118'
port = 502

client1 = ModbusTcpClient(host=server, port=port,framer=ModbusRtuFramer)
# this frmaer is very important. Without proper framer data can't be read
# test.py includes all the framers available
client1.connect()
client2 = ModbusTcpClient(host=server, port=port,framer=ModbusRtuFramer)
'''''
try:
   client1.connect()
   sensor1 = client1.read_holding_registers(address=0,count=2,slave=1)
   temp1 = sensor1.registers[0]*165/1650-40
   hum1 = sensor1.registers[1]*100/1000
   print(sensor1.registers)
   #client1.close()
except Exception as e:
   print(e)   

try:
   client2.connect()
   sensor1 = client2.read_holding_registers(address=0,count=2,slave=1)
   temp1 = sensor1.registers[0]*165/1650-40
   hum1 = sensor1.registers[1]*100/1000
   print(sensor1.registers)
except Exception as e:
   print(e)  
'''''


while True:
    try:
        sensor1 = client1.read_holding_registers(address=0,count=2,slave=1)
        #address 0 means plc address 40001
        #count 2 means it will read two registers. 40001 and 40002
        #slave 1 means the address of modbus slave(sensor) 
        temp1 = sensor1.registers[0]*165/1650-40
        hum1 = sensor1.registers[1]*100/1000
        print(datetime.datetime.now(),"Temp:",temp1,"Hum:",hum1)
        time.sleep(5)    
        #client1.close()
    except Exception as e:
        print(e) 
    finally:
        client1.close() 
   
