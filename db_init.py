"""
This script demonstrates creating database tables
and executing SQL statements using the mysql.connector module.

It establishes a connection to a MySQL server, 
creates two tables ('dreamline_regular_data' and 'cell_table'),
and executes the necessary CREATE TABLE queries. 
The script also includes sample column definitions for the tables.

Before running this script, make sure you have the mysql.connector module installed.

Author: Amirkhan Orazbay
Date: 02.06.2023
"""
import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password):
    """
    The create_server_connection function in the provided
    code establishes a connection to a MySQL database
    server using the mysql.connector module.

    If the connection is successful, the connection
    object is assigned to the connection variable.
    Otherwise, if an error occurs during the connection
    attempt, an Error object is raised, and an error message is printed.

    Finally, the function returns the connection object,
    whether it is a valid connection or None if the connection attempt failed.
    """

    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database="sys",
            port=3306,
        )
    except Error as err:
        print(f"Error: '{err}'")

    return connection


cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
cursor = cnx.cursor()
# main_var = [
#     "id INT AUTO_INCREMENT PRIMARY KEY",
#     "object_number int NOT NULL",
#     "object_name VARCHAR(64) NOT NULL",
#     "timestamp_ctr datetime NOT NULL",
#     "temperature FLOAT NOT NULL",
#     "voltage FLOAT NOT NULL",
#     "temperature_cpu FLOAT NOT NULL",
#     "restart_number int NOT NULL",
#     "number_of_cells int NOT NULL",
#     "timestamp datetime NOT NULL",
# ]

# CREATE_TABLE_QUERY = (
#     "CREATE TABLE dreamline_regular_data ( " + ",".join(main_var) + ");"
# )
# print(CREATE_TABLE_QUERY)

# # Insert new employee
# cursor.execute(CREATE_TABLE_QUERY)

# DISCRETE_BLOCK_PREFIX = "input_state_"
# discrete_block_columns = [
#     DISCRETE_BLOCK_PREFIX + str(i + 1) + " int" for i in range(0, 8)
# ]
# micom_registers = [
#     "0140",
#     "0169",
#     "0165",
#     "002B",
#     "0111",
#     "005A",
#     "0026",
#     "0030",
#     "0032",
#     "0034",
#     "0036",
# ]
# register_data_columns = [
#     "reg_" + register + "_data int" for register in micom_registers
# ]
# register_value_columns = [
#     "reg_" + register + "_value int" for register in micom_registers
# ]
# combine_data_value_columns = [
#     data + ", " + value
#     for (data, value) in zip(register_data_columns, register_value_columns)
# ]

# regular_table_columns = discrete_block_columns
# regular_table_columns += combine_data_value_columns

# CREATE_TABLE_QUERY = (
#     "CREATE TABLE cell_table ( "
#     + "id INT AUTO_INCREMENT PRIMARY KEY, cell_number INT, "
#     + " reg_msg_id INT,"
#     + ",".join(regular_table_columns)
#     + "CONSTRAINT `reg_msg_id` FOREIGN KEY (`reg_msg_id`) "
#     + "REFERENCES `dreamline_regular_data` (`id`)"
#     + ");"
# )

# print(CREATE_TABLE_QUERY)

# # Insert new employee
# cursor.execute(CREATE_TABLE_QUERY)
# # Make sure data is committed to the database
# cnx.commit()

CREATE_TABLE_QUERY = (
    "CREATE TABLE object_table (object_number int, object_name VARCHAR(64));"
)

cursor.execute(CREATE_TABLE_QUERY)
# Make sure data is committed to the database
cnx.commit()

cursor.execute(
    "INSERT INTO object_table (object_number, object_name) VALUES (%s,%s)",
    (1, "OBJECT 1"),
)
# Make sure data is committed to the database
cnx.commit()

cursor.execute(
    "INSERT INTO object_table (object_number, object_name) VALUES (%s,%s)",
    (2, "OBJECT 2"),
)
# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
