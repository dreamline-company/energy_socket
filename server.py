"""
The code you provided appears to be a server-side script 
that listens for incoming connections on a specified IP address and port.
It creates a socket using the socket module, 
binds it to the specified IP and port, 
and listens for incoming connections.

Once a connection is established, 
the script starts a new thread using the _thread.start_new_thread() function 
to handle the client's requests concurrently. 

The script continuously listens for new client connections in an infinite loop, 
creating a new thread for each connection.

It's worth noting that the code provided lacks proper error handling 
and termination conditions for the server. 
In a real-world scenario, you should handle exceptions, 
close connections properly, and implement a way to stop the server gracefully.

Author: Amirkhan Orazbay
Date: 02.06.2023
"""
from db_var import *
import socket
from datetime import datetime, timezone, timedelta
from _thread import start_new_thread
import mysql.connector
from mysql.connector import Error

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 8070
IP = socket.gethostbyname(HOST)
ServerSideSocket = socket.socket()


THREAD_COUNT = 0
MAX_LEN_PACKET = 255
START_CHARACTER = 60
END_CHARACTER = 62
DIVIDER_FOR_FLOAT_VALUES = 10.0

upload_file = False

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")


def get_object_name(object_number):
    cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
    cursor = cnx.cursor()
    cursor.execute(
        f"SELECT object_name FROM object_table WHERE object_number={object_number}"
    )
    object_name = cursor.fetchall()[0][0]

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    return object_name


def get_temp_volt(data, start_index):
    result = ()
    for i in range(start_index, start_index + 3 * 2, 2):
        result += (float(data[i + 1] << 8 | data[i]) / DIVIDER_FOR_FLOAT_VALUES,)
    result += (start_index + 3 * 2,)
    return result


def get_datetime_index(data):
    index_of_start_symbol = data.index(124)
    index_of_end_symbol = data.index(124, index_of_start_symbol + 1)
    return (
        (data[index_of_start_symbol + 1 : index_of_end_symbol]).decode(),
        index_of_end_symbol,
    )


def get_binary(data):
    """
    The get_binary function in the provided code converts
    a sequence of integers into a tuple of binary values.

    The function takes a parameter data,
    which is expected to be an iterable containing integers.
    It initializes an empty list called list_of_bits to store the binary values.

    For each element, it converts the integer i
    to its binary representation using the f"{i:08b}" formatting syntax.
    The :08b specifies that the binary representation
    should have a width of 8 digits, padded with zeros if necessary.

    The resulting binary representation is then
    converted into a list of integers using a list comprehension.

    Each character in the binary string is
    converted to an integer using the int() function.

    Finally, the function returns a tuple of the binary
    values by passing list_of_bits to the tuple() function.
    """

    list_of_bits = []
    for i in data:
        list_of_bits += [int(j) for j in f"{i:08b}"]
    return tuple(list_of_bits)


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


def insert_table_data(data, table_id):
    """
    The insert_regular_table_data() function connects
    to a MySQL server and inserts the received data into two database tables,
    namely dreamline_regular_data and cell_table.
    It constructs the SQL statements dynamically based on the data received.
    """
    cnx = create_server_connection("13.53.42.132", "root", "my-secret-pw")
    cursor = cnx.cursor()
    insert_sql_statement = ()
    if table_id == 0:
        insert_sql_statement = (
            "INSERT INTO dreamline_general_data ("
            + ", ".join(main_var[:-1])
            + ") VALUES ("
            + "%s," * (len(data) - 1)
            + "%s)"
        )
    elif table_id == 1:
        insert_sql_statement = (
            "INSERT INTO dreamline_regular_data (cell_number,"
            + ", ".join(general_var[:-1])
            + ") VALUES ("
            + "%s," * (len(data) - 1)
            + "%s)"
        )
    elif table_id == 2:
        insert_sql_statement = (
            "INSERT INTO dreamline_general_data ("
            + ", ".join(emergency_var[:-1])
            + ") VALUES ("
            + "%s," * (len(data) - 1)
            + "%s)"
        )
    print(insert_sql_statement)
    cursor.execute(insert_sql_statement, data)

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()
    return 0


def multi_threaded_client(connection, address):
    """
    The multi_threaded_client() function is responsible
    for processing the data received from the client.

    Within the multi_threaded_client() function,
    the received data is checked for validity
    and parsed according to a specific protocol.
    If the data is valid and the message type is 1,
    the insert_regular_table_data() function is called
    to insert the extracted data into a MySQL database.
    """
    while True:
        try:
            received_data = connection.recv(1024)

            if not received_data:
                break
            print(
                " ".join(
                    received_data.hex()[i : i + 2].upper()
                    for i in range(0, len(received_data.hex()), 2)
                )
            )
            length_received_data = len(received_data)
            start_index = received_data.index(START_CHARACTER)
            end_index = received_data.index(END_CHARACTER, start_index)

            received_data = received_data[start_index : end_index + 1]

            print("Data with length of ", length_received_data)

            check_start_and_end_symbol = (
                received_data[0] == START_CHARACTER
                and received_data[-1] == END_CHARACTER
            )

            check_valid_type_packet = received_data[1] in range(1, 4)

            if (
                check_start_and_end_symbol
                and check_valid_type_packet
                and length_received_data <= MAX_LEN_PACKET
            ):
                now = datetime.now(timezone(timedelta(hours=+6), "ALA"))
                message_type = received_data[1]
                object_number = int.from_bytes(received_data[2:4], "little")
                object_name = get_object_name(object_number)
                datetime_from_ctr = datetime.fromtimestamp(
                    int.from_bytes(
                        received_data[4 : received_data.index(ord("{"))], "little"
                    )
                )

                main_data = received_data[
                    received_data.index(ord("{")) + 1 : received_data.index(ord("}"))
                ]

                main_data = main_data.split(b",")[:-1]
                print(main_data)
                data = (
                    object_number,
                    object_name,
                    datetime_from_ctr,
                )
                if message_type == 1:
                    data += tuple(main_data)
                elif message_type == 2:
                    for registers in main_data:
                        register_data = data + (registers[0],)
                        registers = registers[1:]
                        registers = registers.split(b";")[:-1]
                        for register_number, register_value in registers:
                            register_data += (register_number, register_value)
                        register_data += (now,)
                        print("dawdawdawd", register_data)
                        insertion_result = 0

                        if insertion_result == 0:
                            print("Insert Success")
                        else:
                            print("Insert Fail")
                elif message_type == 3:
                    for cell_number, cell_value in main_data:
                        data += (cell_number, cell_value)

                if message_type != 2:
                    data += (now,)
                    # insertion_result = insert_table_data(data, message_type - 1)
                    print(data)
                    if 0 == 0:
                        print("Insert Success")
                    else:
                        print("Insert Fail")
        except ConnectionResetError:
            print(address, "is reset connection")
        except IndexError as ie:
            print(address, ie.with_traceback)
        except ValueError as ve:
            print(address, ve.with_traceback)
        finally:
            msg = f"<OK!Recv {main_data}>"
            connection.sendall(msg.encode())
    connection.close()


try:
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
print("Socket is started")
ServerSideSocket.listen()

while True:
    Client, new_socket = ServerSideSocket.accept()
    print("Connection from: " + new_socket[0] + ":" + str(new_socket[1]))
    start_new_thread(multi_threaded_client, (Client, new_socket))
    THREAD_COUNT += 1
