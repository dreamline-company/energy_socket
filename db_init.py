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
from db_var import *
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


cnx = create_server_connection("13.53.42.132", "root", "my-secret-pw")
cursor = cnx.cursor()

main = [data + " " + value for (data, value) in zip(main_var, main_var_param)]

CREATE_TABLE_QUERY = "CREATE TABLE dreamline_general_data ( " + ",".join(main) + ");"
print(CREATE_TABLE_QUERY)

# Insert new employee
cursor.execute(CREATE_TABLE_QUERY)
cnx.commit()

CREATE_TABLE_QUERY = (
    "CREATE TABLE dreamline_regular_data ( "
    + "id INT AUTO_INCREMENT PRIMARY KEY, cell_number INT, "
    + ",".join(general_var_creation)
    + ");"
)

print(CREATE_TABLE_QUERY)

# Insert new employee
cursor.execute(CREATE_TABLE_QUERY)
# Make sure data is committed to the database
cnx.commit()

emergency = [
    data + " " + value for (data, value) in zip(emergency_var, emergency_var_param)
]

CREATE_TABLE_QUERY = (
    "CREATE TABLE dreamline_emergency_data ( " + ",".join(emergency) + ");"
)
print(CREATE_TABLE_QUERY)

# Insert new employee
cursor.execute(CREATE_TABLE_QUERY)
cnx.commit()


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
