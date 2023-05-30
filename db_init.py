import socket
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
from _thread import *
import itertools


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

cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
cursor = cnx.cursor()
# main_var = ["id INT AUTO_INCREMENT PRIMARY KEY", "object_number int NOT NULL", "timestamp_ctr datetime NOT NULL", "temperature int NOT NULL", "voltage int NOT NULL", "temperature_cpu int NOT NULL", "restart_number int NOT NULL", "cell_number int NOT NULL", "timestamp datetime NOT NULL"]
# create_table = "CREATE TABLE dreamline_regular_data ( " + ','.join(main_var) + ");"
# print(create_table)
# # Insert new employee
# cursor.execute(create_table)
print()
discrete_block_prefix = "input_state_"
discrete_block_columns = [discrete_block_prefix + str(i+1) + " int" for i in range(0,8)]
micom_registers = ["0140","0169","0165","002B","0111","005A","0026","0030","0032","0034","0036"]
register_data_columns = ['reg_' + register + '_data int' for register in micom_registers]
register_value_columns = ['reg_' + register + '_value int' for register in micom_registers]
combine_data_value_columns = [ data + ', ' + value for (data,value) in zip(register_data_columns,register_value_columns)]

regular_table_columns = discrete_block_columns
regular_table_columns += combine_data_value_columns

create_table = "CREATE TABLE cell_table ( " + 'id INT AUTO_INCREMENT PRIMARY KEY,' + ','.join(regular_table_columns) + ',CONSTRAINT `reg_msg_id` FOREIGN KEY (`id`) REFERENCES `dreamline_regular_data` (`id`)' + ");"
print(create_table)
# Insert new employee
cursor.execute(create_table)
# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
