import ctypes
import time
import mysql.connector
from mysql.connector.errors import Error

databaseHost = "localhost"
databaseUserName = "root"
databasePassword = ""
databaseName = "scada"
databaseTable = "sensor_data"

try:
    ctAPI = ctypes.WinDLL(r'C:\Program Files (x86)\Schneider Electric\Citect SCADA 2018\Bin\Bin (x64)\CtApi.dll')
    if ctAPI:
        print("DLL loaded successfully")
    else:
        print("Error loading DLL")   
except Exception as e:
    print("Error loading DLL:", e)

ctAPI.ctOpen.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong]
ctAPI.ctOpen.restype = ctypes.c_void_p 

ctAPI.ctTagRead.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong]
ctAPI.ctTagRead.restype = ctypes.c_bool

serverName = None
userName = None
password = None
flags = 0



try:
    connectionHandle = ctAPI.ctOpen(serverName,userName,password,flags)
    if connectionHandle:
        print("Connected to Server")
    else:
        print("Failed to open connection")    
except Exception as e:
        print(e)  

def insertColomnUsingProcedure(name, temp, hum):
    try:
        connection = mysql.connector.connect(host=databaseHost, user=databaseUserName, password=databasePassword, database=databaseName)
        if connection.is_connected():
            #print("Database Connected")
            myCursor = connection.cursor()
            myCursor.callproc("insertData",[name,temp,hum])
            connection.commit()
            print(name,temp,hum,"Inserted into Database")
    except Error as err:
        print(err)
    finally:
        if connection.is_connected():
            myCursor.close()
            connection.close()
            #print("Database Closed")

def readTemp(handle,tagName):
    try:
        if handle:
            bufferSize = 256
            tagValueBuffer = ctypes.create_string_buffer(bufferSize)
            tagReadFlag = ctAPI.ctTagRead(connectionHandle,tagName, tagValueBuffer, bufferSize)
            if tagReadFlag:
                tagValueInt = int(tagValueBuffer.value.decode().strip('\x00'))
                tagValueTemp = round((tagValueInt *165)/1650-40,1)
                return tagValueTemp
    except Exception as e:
        print(e)  

def readHum(handle,tagName):              
    try:
        if handle:
            bufferSize = 256
            tagValueBuffer = ctypes.create_string_buffer(bufferSize)
            tagReadFlag = ctAPI.ctTagRead(connectionHandle,tagName, tagValueBuffer, bufferSize)
            if(tagReadFlag):
               tagValueHum = float(tagValueBuffer.value.decode().strip('\x00'))
               return tagValueHum    
    except Exception as e:
        print(e)         

def printTagValue(handle,tagName):
    try:
        if handle:
            bufferSize = 256
            tagValueBuffer = ctypes.create_string_buffer(bufferSize)
            tagReadFlag = ctAPI.ctTagRead(connectionHandle,tagName, tagValueBuffer, bufferSize)
            if(tagReadFlag):
               rawTagValue =tagValueBuffer.value.decode().strip('\x00')
               print(tagName.decode(),":",rawTagValue) 
    except Exception as e:
        print(e)     

while True:
     
    Temp = readTemp(connectionHandle,b"Archive1_T")
    Hum = readHum(connectionHandle,b"Archive1_RH")
    insertColomnUsingProcedure("Sensor1",Temp,Hum)
    print(Temp,Hum)

    Temp1 = readTemp(connectionHandle,b"Archive2_T")
    Hum1 = readHum(connectionHandle,b"Archive2_RH")
    insertColomnUsingProcedure("Sensor2",Temp1,Hum1)
    print(Temp1,Hum1)

    #printTagValue(connectionHandle,b"Archive1_T")
    #printTagValue(connectionHandle,b"Archive1_RH")

    time.sleep(5)

