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
main_var = ["id INT AUTO_INCREMENT PRIMARY KEY", "object_number VARCHAR(8)", "timestamp_ctr datetime", "timestamp datetime", "temperature int", "voltage int", "temperature_cpu int", "restart_number int", "cell_number VARCHAR(8)"]
discrete_block_prefix = "input_state_"
discrete_block_columns = [discrete_block_prefix + str(i) + " int" for i in range(1,33)]
micom_registers = ["0140","0169","0165","002B","0111","005A","0026","0030","0032","0034","0036"]
register_data_columns = ['reg_' + register + '_data int' for register in micom_registers]
register_value_columns = ['reg_' + register + '_value int' for register in micom_registers]
combine_data_value_columns = [ data + ', ' + value for (data,value) in zip(register_data_columns,register_value_columns)]
regular_table_columns = main_var
regular_table_columns += discrete_block_columns
regular_table_columns += combine_data_value_columns

create_table = "CREATE TABLE dreamline_regular_data ( " + ','.join(regular_table_columns) + ");"
print(create_table)
# Insert new employee
cursor.execute(create_table)
# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
