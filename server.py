import socket
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

HOST = socket.gethostname()
PORT = 8080  
IP = socket.gethostbyname(HOST)

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
    insert_controller = ("INSERT INTO controller "
                "(controller_id, current_a, current_b, current_c, timestamp) "
                "VALUES (%s, %s, %s, %s, %s)")
    # Insert new employee
    cursor.execute(insert_controller, data)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if data[0] == 60:
                if data[1] == 0:
                    if data[len(data) - 1] == 62:
                        calc = data[len(data) - 2]
                        for i in range (len(data) - 8):
                            calc |= data[6 + i] << (8 ** (i+1))
                        #register to dec data[4] << 8 | data[5]
                        s = (data[2], data[3], hex(data[4] << 8 | data[5]), calc)
                        print(s)
                        insert_realtime_data(s)
                elif data[1] == 1:
                    if data[len(data) - 1] == 62:
                        #register to dec data[4] << 8 | data[5]
                        now = datetime.now()
                        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                        s = (data[2], data[3], data[4], data[5], formatted_date)
                        print(s)
                        insert_controller_data(s)
            conn.sendall(b"OK!Recv")