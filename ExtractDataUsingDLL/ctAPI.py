import ctypes
import time
import datetime

serverName = None
userName = None
password = None
flags = 0

def loadDLL():    
    try:
        ctAPI = ctypes.WinDLL(r'C:\Program Files (x86)\Schneider Electric\Citect SCADA 2018\Bin\Bin (x64)\CtApi.dll')
        if ctAPI:
            print(datetime.datetime.now(),"DLL loaded successfully")
            return ctAPI
        else:
            print(datetime.datetime.now(),"Error loading DLL")   
    except Exception as e:
        print(datetime.datetime.now(),e)

def openConnection():
    try:
        connectionHandle = ctAPI.ctOpen(serverName,userName,password,flags)
        if connectionHandle:
            print(datetime.datetime.now(),"Connected to Server")
            return connectionHandle
        else:
            print(datetime.datetime.now(),"Failed to open connection.")  
    except Exception as e:
            print(datetime.datetime.now(),e) 


ctAPI = loadDLL()

ctAPI.ctOpen.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong]
ctAPI.ctOpen.restype = ctypes.c_void_p 

ctAPI.ctTagRead.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong]
ctAPI.ctTagRead.restype = ctypes.c_bool

connectionHandle = openConnection()

def readTemp(handle,tagName):
    try:
        if handle:
            bufferSize = 256
            tagValueBuffer = ctypes.create_string_buffer(bufferSize)
            tagReadFlag = ctAPI.ctTagRead(connectionHandle,tagName, tagValueBuffer, bufferSize)
            if tagReadFlag:
                tagValueInt = int(tagValueBuffer.value.decode().strip('\x00'))
                return (tagValueInt *165)/1650-40
    except Exception as e:
        print(datetime.datetime.now(),e)  

def readHum(handle,tagName):              
    try:
        if handle:
            bufferSize = 256
            tagValueBuffer = ctypes.create_string_buffer(bufferSize)
            tagReadFlag = ctAPI.ctTagRead(connectionHandle,tagName, tagValueBuffer, bufferSize)
            if(tagReadFlag):
               return tagValueBuffer.value.decode().strip('\x00')   
    except Exception as e:
        print(datetime.datetime.now(),e)         


while True:
    try:
        if connectionHandle:    
            Temp = readTemp(connectionHandle,b"Archive1_T")
            Hum = readHum(connectionHandle,b"Archive1_RH")
            print(datetime.datetime.now(),"Sensor1: ","Temperature:","%.1f"%Temp,"Humidity:",Hum)
            Temp1 = readTemp(connectionHandle,b"Archive2_T")
            Hum1 = readHum(connectionHandle,b"Archive2_RH")
            print(datetime.datetime.now(),"Sensor2: ","Temperature:","%.1f"%Temp1,"Humidity:",Hum1)
            print("\n")
        else:
            print(datetime.datetime.now(),"Not connected to Scada Server.Retrying")
            connectionHandle = openConnection()    
    except Exception as e:
        print(datetime.datetime.now(),e)
    time.sleep(5)    


    #intValueTemp = readTag(connectionHandle,b"Archive1_T")
    #intValueHum  = readTag(connectionHandle,b"Archive1_RH")
    #print(intValueHum)
    #floatValueTemp = (intValueTemp * 165)/1650-40
    #floatValueHum = (intValueHum * 100)/1000
    #print("Temperature:","%.1f"%floatValueTemp)

'''''
def readTag(handle,tagName):
    try:
        if handle:
            bufferSize = 256  
            tagValueBuffer = ctypes.create_string_buffer(bufferSize)
            tagValueRaw = ctAPI.ctTagRead(connectionHandle,tagName, tagValueBuffer, bufferSize)
            print("RawValue:",tagValueRaw)
            if tagValueRaw:
               return tagValueBuffer.value.decode().strip('\x00')
               #tagValueInt = int(tagValueBuffer.value.decode().strip('\x00'))
               #print(tagValueInt)
               #if tagValueInt:
                 # return tagValueInt 
            else:
                print(f"Failed to read value of tag '{tagName}'")
    except Exception as e:
        print(e) 
'''''

