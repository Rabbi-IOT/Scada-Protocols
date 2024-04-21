from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ModbusException
import time
import datetime

#from pymodbus.transaction import ModbusSocketFramer 
from pymodbus.transaction import ModbusRtuFramer
#from pymodbus.transaction import ModbusBinaryFramer 
#from pymodbus.transaction import ModbusAsciiFramer 

# Define the Modbus TCP server IP address and port
SERVER_HOST = '192.168.0.118'
SERVER_PORT = 502

client = ModbusTcpClient(SERVER_HOST, port=SERVER_PORT,framer=ModbusRtuFramer)
client.connect()

"""Read holding registers (code 0x03).
:param address: Start address to read from
:param count: (optional) Number of coils to read
:param slave: (optional) Modbus slave ID
:param kwargs: (optional) Experimental parameters.
:raises ModbusException:"""
while True:
    #sensor1 = client.read_holding_registers(address=0,count=3,slave=1)
    cdu1 = client.read_input_registers(address=0,count =12,slave = 2)
    #temp1 = sensor1.registers[0]*165/1650-40
    #hum1 = sensor1.registers[1]*100/1000
    print(cdu1.registers)
    #print(datetime.datetime.now(),"Temp=","%.1f"%temp1,"Hum=","%.1f"%hum1)
    time.sleep(2)
"""
time.sleep(0.01)
sensor2 = client.read_holding_registers(address=0,count=2,slave=2)
temp2 = sensor2.registers[0]*165/1650-40
hum2 = sensor2.registers[1]*100/1000
print(sensor2.registers)
print(temp2,hum2)
"""






