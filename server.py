import socket
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
from _thread import *
import itertools

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 8070
IP = socket.gethostbyname(HOST)
ServerSideSocket = socket.socket()
ThreadCount = 0

MAX_LEN_PACKET = 255
START_CHARACTER = 60
END_CHARACTER = 62

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")

def get_binary(data):
    list_of_bits = []
    for i in data:
        list_of_bits += [int(j) for j in  f'{i:08b}']
    return tuple(list_of_bits)

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database='sys',
            port=3306,
        )
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def insert_realtime_data(data): 
    cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
    cursor = cnx.cursor()
    insert_realtime = "INSERT INTO dreamline_regular_data (controller_id, slave_id, register, value) VALUES (%s, %s, %s, %s)"
    # Insert new employee
    cursor.execute(insert_realtime, data)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()

def insert_regular_table_data(data): 
    cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
    cursor = cnx.cursor()
    try :
        main_var = ["object_number", "timestamp_ctr", "timestamp", "temperature", "voltage", "temperature_cpu", "restart_number", "cell_number"]
        discrete_block_prefix = "input_state_"
        discrete_block_columns = [discrete_block_prefix + str(i) for i in range(1,33)]
        micom_registers = "0140" #["0140","0169","0165","002B","0111","005A","0026","0030","0032","0034","0036"]
        register_data_columns = ['reg_' + register + '_data' for register in micom_registers]
        register_value_columns = ['reg_' + register + '_value' for register in micom_registers]
        combine_data_value_columns = [ data + ', ' + value for (data,value) in zip(register_data_columns,register_value_columns)]
        regular_table_columns = main_var
        if int(data[8]) < 256:
            regular_table_columns += discrete_block_columns
        else:
            regular_table_columns += combine_data_value_columns
        insert_controller_sql_statement = 'INSERT INTO dreamline_regular_data (' + ', '.join(regular_table_columns) + ') VALUES (' + '%s,' * (len(regular_table_columns) - 1)  + '%s)'
        # Insert new employee
        cursor.execute(insert_controller_sql_statement, data)
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        print('Inserted with successs')
    except Exception as err:
        print(err)
        print(err.with_traceback)
        print(err.__traceback__)
    
def multi_threaded_client(connection, address):
    while True:
        try:
            data = connection.recv(1024)
        
            if not data:
                break
            
            print('Data in bytes:', data, 'With length of ', len(data))
            check_start_and_end_symbol = (data[0] == START_CHARACTER and data[len(data) - 1] == END_CHARACTER)
            check_valid_type_packet = data[1] in range(1,3)
            
            if check_start_and_end_symbol and check_valid_type_packet and len(data) <= MAX_LEN_PACKET:
                now = datetime.now()
                object_number = data[2] << 8 | data[3]
                if data[1] == 1:
                    temp = data[4]
                    voltage = data[5]
                    temp_cpu = data[6]
                    cell_number = hex(data[8] << 8 | data[9])
                    if (data[8] << 8 | data[9]) < 256:
                        s = (hex(object_number), now, now, float(temp), float(voltage), float(temp_cpu), data[7], cell_number) +  get_binary(data[10:14])
                        insert_regular_table_data(s)
                    else:
                        s = (hex(object_number), now, now, float(temp), float(voltage), float(temp_cpu), data[7], cell_number, data[10])
                        insert_regular_table_data(s)
                elif data[1] == 2:
                    #register to dec data[4] << 8 | data[5]
                    now = datetime.now()
                    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                    s = (data[2], data[3], data[4], data[5], formatted_date, data[3], data[4], data[5], formatted_date)
                    insert_regular_table_data(s)
            connection.sendall(b"OK!Recv")
        except ConnectionResetError:
            print(address, 'is reset connection')
    connection.close()
            
try:
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
print('Socket is started')
ServerSideSocket.listen()

while True:
    Client, address = ServerSideSocket.accept()
    print('Connection from: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, address))
    ThreadCount += 1