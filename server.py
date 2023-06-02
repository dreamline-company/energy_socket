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
import socket
from datetime import datetime
import pytz
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

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")


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


def insert_regular_table_data(regular_data):
    """
    The insert_regular_table_data() function connects
    to a MySQL server and inserts the received data into two database tables,
    namely dreamline_regular_data and cell_table.
    It constructs the SQL statements dynamically based on the data received.
    """
    cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
    cursor = cnx.cursor()

    main_var = [
        "object_number",
        "timestamp_ctr",
        "temperature",
        "voltage",
        "temperature_cpu",
        "restart_number",
        "number_of_cells",
        "timestamp",
    ]

    regular_table_columns = main_var
    insert_controller_sql_statement = (
        "INSERT INTO dreamline_regular_data ("
        + ", ".join(regular_table_columns)
        + ") VALUES ("
        + "%s," * (len(regular_data) - 1)
        + "%s)"
    )

    cursor.execute(insert_controller_sql_statement, regular_data)
    cnx.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    msg_id = cursor.fetchall()[0][0]

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()
    return msg_id


def insert_cell_table_data(cell_data):
    """
    The insert_regular_table_data() function connects
    to a MySQL server and inserts the received data into two database tables,
    namely dreamline_regular_data and cell_table.
    It constructs the SQL statements dynamically based on the data received.
    """
    cnx = create_server_connection("46.101.102.163", "root", "my-secret-pw")
    cursor = cnx.cursor()

    discrete_block_prefix = "input_state_"
    discrete_block_columns = [discrete_block_prefix + str(i + 1) for i in range(0, 8)]
    micom_registers = [
        "0140"
    ]  # ["0140","0169","0165","002B","0111","005A","0026","0030","0032","0034","0036"]
    register_data_columns = [
        "reg_" + register + "_data" for register in micom_registers
    ]
    register_value_columns = [
        "reg_" + register + "_value" for register in micom_registers
    ]
    combine_data_value_columns = [
        data + ", " + value
        for (data, value) in zip(register_data_columns, register_value_columns)
    ]

    insert_controller_sql_statement = (
        "INSERT INTO cell_table (cell_number,"
        + ", ".join(discrete_block_columns)
        + ",reg_msg_id) VALUES ("
        + "%s," * (len(cell_data) - 1)
        + "%s)"
    )
    cursor.execute(insert_controller_sql_statement, cell_data)

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
            length_received_data = len(received_data)

            if not received_data:
                break

            print("Data with length of ", length_received_data)
            check_start_and_end_symbol = (
                received_data[0] == START_CHARACTER
                and received_data[length_received_data - 1] == END_CHARACTER
            )
            check_valid_type_packet = received_data[1] in range(1, 3)

            if (
                check_start_and_end_symbol
                and check_valid_type_packet
                and length_received_data <= MAX_LEN_PACKET
            ):
                now = datetime.now(pytz.timezone("asian/almaty"))
                message_type = received_data[1]
                object_number = received_data[3] << 8 | received_data[2]
                datetime_from_ctr, end_index = get_datetime_index(received_data)
                temperature, voltage, temperature_cpu, end_index = get_temp_volt(
                    received_data, end_index + 1
                )
                restart_number = (
                    received_data[end_index + 1] << 8 | received_data[end_index]
                )
                number_of_cells = received_data[end_index + 2]
                end_index = end_index + 2

                regular_data = (
                    object_number,
                    datetime_from_ctr,
                    temperature,
                    voltage,
                    temperature_cpu,
                    restart_number,
                    number_of_cells,
                    now,
                )

                print(regular_data)
                if message_type == 1:
                    reg_msg_id = insert_regular_table_data(regular_data)
                    if reg_msg_id:
                        print("Insert Success")
                    else:
                        print("Insert Fail")

                    for i in range(number_of_cells):
                        try:
                            index_of_start_symbol = received_data.index(123, end_index)
                            index_of_end_symbol = received_data.index(
                                125, index_of_start_symbol + 1
                            )

                            cell_number = received_data[index_of_start_symbol + 1]
                            cell_data = (
                                (cell_number,)
                                + get_binary(
                                    received_data[
                                        index_of_start_symbol
                                        + 2 : index_of_start_symbol
                                        + 3
                                    ]
                                )
                                + (reg_msg_id,)
                            )
                            print(cell_data)
                            insert_result = insert_cell_table_data(cell_data)
                            if insert_result == 0:
                                print("Insert Success")
                            else:
                                print("Insert Fail")
                            end_index = index_of_end_symbol
                        except ValueError:
                            pass
            connection.sendall(b"OK!Recv")
        except ConnectionResetError:
            print(address, "is reset connection")
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
