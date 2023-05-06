import socket
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
from _thread import *

HOST = '167.71.43.13'
PORT = 8080  
IP = socket.gethostbyname(HOST)
ServerSideSocket = socket.socket()
ThreadCount = 0

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database='defaultdb',
            port=25060,
            ssl_ca='/Users/amirkhanorazbay/Downloads/ca-certificate (1).crt'
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def insert_realtime_data(data): 
    cnx = create_server_connection("db-mysql-fra1-01434-do-user-13902982-0.b.db.ondigitalocean.com", "doadmin", "AVNS_YJZHKISaSzqXCi6aSRo")
    cursor = cnx.cursor()
    insert_realtime = "INSERT INTO realtime (controller_id, slave_id, register, value) VALUES (%s, %s, %s, %s)"
    print(data)
    # Insert new employee
    cursor.execute(insert_realtime, data)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_controller_data(data): 
    cnx = create_server_connection("db-mysql-fra1-01434-do-user-13902982-0.b.db.ondigitalocean.com", "doadmin", "AVNS_YJZHKISaSzqXCi6aSRo")
    cursor = cnx.cursor()
    insert_controller = 'INSERT INTO controller (controller_id, vs, temp_cpu, temp, timestamp) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE vs=%s, temp_cpu=%s, temp=%s, timestamp=%s'
    # Insert new employee
    cursor.execute(insert_controller, data)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()
    
def multi_threaded_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        if data[0] == 60:
            print(data)
            print(data[1])
            if data[1] == 0:
                if data[len(data) - 1] == 62:
                    calc = data[len(data) - 2]
                    for i in range (len(data) - 8):
                        calc |= data[6 + i] << (8 ** (i+1))
                    #register to dec data[4] << 8 | data[5]
                    s = (data[2], data[3], hex(data[4] << 8 | data[5]), calc)
                    print('iamhere')
                    insert_realtime_data(s)
            elif data[1] == 1:
                if data[len(data) - 1] == 62:
                    #register to dec data[4] << 8 | data[5]
                    now = datetime.now()
                    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                    s = (data[2], data[3], data[4], data[5], formatted_date, data[3], data[4], data[5], formatted_date)
                    insert_controller_data(s)
        connection.sendall(b"OK!Recv")
    connection.close()
            
try:
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()