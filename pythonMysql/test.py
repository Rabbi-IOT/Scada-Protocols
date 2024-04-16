import mysql.connector
from mysql.connector.errors import Error
import time

hostName = "192.168.0.83"
userName = "ati_iot"
password = "Ati_iot12345"
databaseName = "ati_iot"
tableName = "sensor_data"
port = 3306

def insertColomnUsingProcedure(name, temp,hum):
    try:
        connection = mysql.connector.connect(host=hostName, user=userName, password=password, database=databaseName)
        if connection.is_connected():
            print("Database Connected")
            myCursor = connection.cursor()
            myCursor.callproc("insertData",[name,temp,hum])
            connection.commit()
    except Error as err:
        print(err)
    finally:
        if connection.is_connected():
            myCursor.close()
            connection.close()
            print("Database Closed")

def insertColomn(name, temp,hum):
    try:
        connection = mysql.connector.connect(host=hostName,port=port, user=userName, password=password, database=databaseName)
        if connection.is_connected():
            print("Database Connected")
            myCursor = connection.cursor()
            sql = f'INSERT INTO {tableName} (Name,Temperature,Humidity) VALUES ("{name}","{temp}","{hum}")'
            myCursor.execute(sql)
            connection.commit()
    except Error as err:
        print(err)
    finally:
        if connection.is_connected():
            myCursor.close()
            connection.close()
            print("Database Closed")


#insertColomnUsingProcedure("PythonProcedure1", 30.5,50.5)

times = 30000        
name = "sensorNew"
temp = 22.3
hum = 60.0
data = [(name, temp, hum)] * times
startTime = time.time() 
try: 
    connection = mysql.connector.connect(host=hostName,port=3306, user=userName, password=password, database=databaseName) 
    if connection.is_connected():  
        print("Database Connected")
        myCursor = connection.cursor()
        sql = f"INSERT INTO {tableName} (Name,Temperature,Humidity) VALUES (%s,%s,%s)"       
        #myCursor.execute(sql)
        myCursor.executemany(sql,data)
        connection.commit()    
except Error as err:
    print(err)   
finally:
    if connection.is_connected():
        myCursor.close()
        connection.close()
        print("Database Closed")
stopTime = time.time()
print("Execution time",(stopTime-startTime))