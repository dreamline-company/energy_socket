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
import struct
from datetime import datetime, timezone, timedelta
from _thread import start_new_thread
import mysql.connector
from mysql.connector import Error

from db_var import (
    comman_var,
    general_var,
    emergency_var,
    regular_var,
    state_name,
    FILE_SEND_STATE_ID,
    RESET_STATE_ID,
    SET_TIME_STATE_ID,
)

DB_SERVER = "13.51.150.58"
DB_USERNAME = "root"
DB_PASSWORD = "my-secret-pw"
DB_NAME = "sys"
DB_PORT = 3306

THREAD_COUNT = 0
MAX_LEN_PACKET = 255
START_CHARACTER = 60
END_CHARACTER = 62
DIVIDER_FOR_FLOAT_VALUES = 10.0

LAST_INDEX = -1

REGULAR_PACKET_TYPE = 1
EMERGENCY_PACKET_TYPE = 2
CMD_PACKET_TYPE = 3


GENERAL_TABLE_ID = 0
REGULAR_TABLE_ID = 1
EMERGENCY_TABLE_ID = 2

UPLOAD_FILE = False


def get_object_name(object_number):
    """
    возвращает имя объекта из базы данных по номеру объекта
    """

    cursor = cnx.cursor()
    # запускаем SQL запрос
    cursor.execute(f"SELECT obj_name FROM obj_table WHERE obj_num={object_number}")
    # Извлекаем имя из ответа базы данных
    object_name = cursor.fetchall()[0][0]

    # Фиксируем данные в базе данных
    cnx.commit()

    cursor.close()
    return object_name


def change_state_to(state_id, object_id, state_val):
    cursor = cnx.cursor()
    # запускаем SQL запрос
    cursor.execute(
        f"UPDATE states SET {state_name[state_id]} = {state_val} WHERE id = {object_id}"
    )

    cnx.commit()

    cursor.close()


def get_states(object_id):
    cursor = cnx.cursor()
    # запускаем SQL запрос
    cursor.execute(f"SELECT file_send, reset, set_time FROM states WHERE id = {object_id}")

    # Извлекаем имя из ответа базы данных
    state = cursor.fetchall()[0]
    # Фиксируем данные в базе данных

    cnx.commit()
    cursor.close()
    return state


def create_server_connection(host_name, user_name, user_password, database_name):
    """
    Функция create_server_connection устанавливает соединение с базой данных MySQL с помощью модуля mysql.connector.
    """

    connection = None
    try:
        # передаем все данные сервера и открываем соединение
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name,
            port=DB_PORT,
        )
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def insert_table_data(data, table_id):
    """
    Функция insert_regular_table_data() вставляет полученные данные в таблицу базы данных,
    Он динамически строит SQL запрос на основе полученных данных.
    """
    cursor = cnx.cursor()
    insert_sql_statement = ()

    # строит SQL запрос для вставки в dreamline_general_data
    if table_id == GENERAL_TABLE_ID:
        insert_sql_statement = (
            "INSERT INTO general ("
            + ", ".join(comman_var[1:-1])
            + ", "
            + ", ".join(general_var[: len(data) - len(comman_var) + 1])
            + f", {comman_var[-1]}"
            + ") VALUES ("
            + "%s," * len(data)
        )
        insert_sql_statement = insert_sql_statement[:LAST_INDEX] + ")"
    # строит SQL запрос для вставки в dreamline_regular_data
    elif table_id == REGULAR_TABLE_ID:
        if len(data) == 4:
            insert_sql_statement = (
                "INSERT INTO regular ("
                + ", ".join(comman_var[1:])
                + ") VALUES ("
                + "%s," * len(data)
            )
        else: 
            insert_sql_statement = (
                "INSERT INTO regular ("
                + ", ".join(comman_var[1:-1])
                + ", "
                + ", ".join(regular_var[: len(data) - len(comman_var) + 1])
                + f", {comman_var[-1]}"
                + ") VALUES ("
                + "%s," * len(data)
            )
        insert_sql_statement = insert_sql_statement[:LAST_INDEX] + ")"
    # строит SQL запрос для вставки в dreamline_emergency_data
    elif table_id == EMERGENCY_TABLE_ID:  
        if len(data) == 4:
            insert_sql_statement = (
                "INSERT INTO emergency ("
                + ", ".join(comman_var[1:])
                + ") VALUES ("
                + "%s," * len(data)
            )   
        else :
            insert_sql_statement = (
                "INSERT INTO emergency ("
                + ", ".join(comman_var[1:-1])
                + ", "
                + ", ".join(emergency_var[: len(data) - len(comman_var) + 1])
                + f", {comman_var[-1]}"
                + ") VALUES ("
                + "%s," * len(data)
            )
        insert_sql_statement = insert_sql_statement[:LAST_INDEX] + ")"
    # запускаем SQL запрос
    print(data)
    print(insert_sql_statement)
    cursor.execute(insert_sql_statement, data)
    print(f"Inserted data into {table_id} - {data}")
    # Фиксируем данные в базе данных
    cnx.commit()
    cursor.close()
    return 0


def is_data_valid(received_data):
    """
    Возвращает true, если полученные данные имеют допустимый формат.
    - начинаеться с '<'
    - заканчиваться на '>'
    - длина меньше MAX_LEN_PACKET
    """
    # длина полученных данных
    length_received_data = len(received_data)
    # проверяем начальный и конечный символ
    check_start_and_end_symbol = (
        received_data[0] == START_CHARACTER
        and received_data[LAST_INDEX] == END_CHARACTER
    )
    # проверяем правильность типа пакета
    check_valid_type_packet = received_data[2] - ord('0') in [
        REGULAR_PACKET_TYPE,
        EMERGENCY_PACKET_TYPE,
        CMD_PACKET_TYPE,
    ]
    
    # на основе всех критериев возвращем ответ
    return (
        check_start_and_end_symbol
        and check_valid_type_packet
        and length_received_data <= MAX_LEN_PACKET
    )


def parse_regular_registers(base_data, main_data):
    """
    Функция возвращает массив кортежей состоящих из номера ячейки, номера регистра, значения регистра
    """
    data = []

    for cell in main_data:
        print('-----------------------')
        key_val = cell.split(b'|')
        print(key_val)
        # получаем номер ячейки
        cell_number = key_val[0].decode()
        print(cell_number)
        # регистры разделинны символом ';' делим по этому символу
        registers = key_val[1].split(b";")[:LAST_INDEX]
        print(registers)
        register_data = (cell_number,)
        for register in registers:
            key_val_reg = register.split(b':')
            # номер регистра
            register_num = key_val_reg[0].decode()
            # значение регистра
            register_val = key_val_reg[1].decode()
            # собираем кортеж из номера ячейки, номера регистра, значения регистра
            register_data += (register_val,)
        print(register_data)
        register_data = base_data[:-1] + register_data + (base_data[-1],)
        data.append(register_data)
        print('--------------------')
    return data

def parse_general_data(base_data, received_data):
    """
    Функция возвращает кортеже состоящий из значений температуры, напряжения, состояний модулей, количество перезагрузок
    """

    # между послденими символами '{' и '}' находиться общая информация с контроллера, вырезаем данный промежуток
    general_data_r = received_data[
        received_data.rindex(ord("{")) + 1 : received_data.rindex(ord("}"))
    ]
    # общая информация разделинна символом ',' делим по этому символу
    general_data_r = general_data_r.split(b",")[:LAST_INDEX]
    general_data = ()
    temp_map = {}
    for data_entry in general_data_r:
        key_val = data_entry.split(b':')
        # собираем кортеж из значений
        temp_map[key_val[0].decode()] = key_val[1].decode()

    for key in general_var:
        general_data += (temp_map[key],)

    return base_data[:-1] + general_data + (base_data[-1],)

def parse_emergency_data(base_data, main_data):
    """
    Функция возвращает кортеже состоящий из номера ячейки, значения ячейки
    """
    data = ()
    for cell in main_data:
        key_val = cell.split(b':')
        # номера ячейк
        cell_num = int(key_val[0].decode())
        # значения ячейки
        cell_val = int(key_val[1].decode())
        # собираем кортеж из номера ячейки, значения ячейки
        data += (cell_val,)
    return base_data[:-1] + data + (base_data[-1],)


def parse_socket_data(received_data):
    """
    Функция возвращает кортеж из тип пакета (packet_type) и спарсенных данных (data)
    """

    now = datetime.now(timezone(timedelta(hours=+6), "ALA"))
    # нужно объединить два байта для получение номера объекта (индексы 1 и 2)
    object_number = received_data[1] - ord('0')
    # на основе номера объекта получаем имя объекта из базы данных
    object_name = get_object_name(object_number)
    # байт под индексов 3 тип пакета
    packet_type = received_data[2] - ord('0')
    # вырезаем данные с индекса 4 до символа '{' между данным промежутке находиться время с контроллера
    datetime_from_ctr = datetime.fromtimestamp(
        int(str(received_data[3 : received_data.index(ord("{"))].decode()))
    )
    # между символами '{' и '}' находиться основаная информация с контроллера, вырезаем данный промежуток
    main_data = received_data[
        received_data.index(ord("{")) + 1 : received_data.index(ord("}"))
    ]
    # данные разделинны символом ',' делим по этому символу
    main_data = main_data.split(b",")[:LAST_INDEX]

    data = ()

    base_data = (
        object_number,
        object_name,
        datetime_from_ctr,
        now,
    )

    # парсим регулярный пакет который состоит из регулярных регистров и общей информацией
    if packet_type == REGULAR_PACKET_TYPE:
        data = parse_regular_registers(base_data, main_data)
        if len(data) == 0:
            data.append(base_data)
        data.append(parse_general_data(base_data, received_data))
    # парсим аварийный пакет который состоит из номера ячейки, значения ячейки
    elif packet_type == EMERGENCY_PACKET_TYPE:
        main_data = received_data[
            received_data.index(ord("{")) + 1 : received_data.rindex(ord("}"))
        ].split(b",")[:LAST_INDEX]
        data = parse_emergency_data(base_data, main_data)
    return packet_type, object_number, data


def multi_threaded_client(connection, address):
    """
    В этом методе происходит обработка подключеного клиента
    Данные которые отправил клиент парситься и добавляються в базу данных
    """
    received_data = b""
    while True:
        try:
            # Чтение данных от подключенного контроллера
            received_data += connection.recv(1024)
            # Если ничего не получили выходим из цикла
            if not received_data:
                break
            # проверям валдиность данных
            if is_data_valid(received_data):
                print("Raw view of data:", received_data)
                print("Data with length of ", len(received_data))

                packet_type, object_id, data = parse_socket_data(received_data)
                # если тип пакета REGULAR_PACKET_TYPE данные вставляем в таблицы REGULAR_TABLE_ID и GENERAL_TABLE_ID
                if packet_type == REGULAR_PACKET_TYPE:
                    for entry in data[:LAST_INDEX]:
                        insert_table_data(entry, REGULAR_TABLE_ID)
                    insert_table_data(data[LAST_INDEX], GENERAL_TABLE_ID)
                # если тип пакета EMERGENCY_PACKET_TYPE данные вставляем в таблицу EMERGENCY_TABLE_ID
                elif packet_type == EMERGENCY_PACKET_TYPE:
                    insert_table_data(data, EMERGENCY_TABLE_ID)

                received_data = b""
                states = get_states(object_id)
                # Формируем ответ контроллеру
                msg = f"<OK{THREAD_COUNT}>"
                if states[1]:
                    msg = "<RESTART>"
                    change_state_to(RESET_STATE_ID, object_id, 0)
                elif states[2]:
                    now = str(datetime.now(timezone(timedelta(hours=+6), "ALA")))
                    year = now[2:4]
                    month = now[5:7]
                    day = now[8:10]
                    hour = now[11:13]
                    min = now[14:16]
                    sec = now[17:19]
                    msg = f"<SETTIME:+CCLK:  {year}/{month}/{day},{hour}:{min}:{sec}>"
                    change_state_to(SET_TIME_STATE_ID, object_id, 0)
                # Отпраляем ответ контроллеру
                print(f"Sending : {msg}")
                connection.sendall(msg.encode())
        except ConnectionResetError:
            print(address, "is reset connection")
            received_data = b""
            break
        except IndexError as i_e:
            print(address, i_e.with_traceback, i_e)
        except ValueError as v_e:
            print(address, v_e.with_traceback, v_e)
        except ConnectionAbortedError as c_a_e:
            print(address, c_a_e.with_traceback, c_a_e)
            break

    connection.close()


# Получаем имя хоста
HOSTNAME = socket.gethostname()
# По имени хоста получаем хоста
HOST = socket.gethostbyname(HOSTNAME)
# Порт который будет слушиться
PORT = 8070
# По хосту получаем IP адрес
IP = socket.gethostbyname(HOST)

# подключаемся к базе данных
cnx = create_server_connection(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME)

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")

try:
    # создаем серверный сокет
    ServerSideSocket = socket.socket()
    # связываем серверный сокет и адрес, порт хоста
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
print("Socket is started")
# слушаем порт
ServerSideSocket.listen()

# цикл где принимаем все соединения
while True:
    # принимаем соединение от клиента
    Client, new_socket = ServerSideSocket.accept()
    Client.settimeout(60)
    print("Connection from: " + new_socket[0] + ":" + str(new_socket[1]))
    # создаем новый поток и начниаем там обработку клиента
    start_new_thread(multi_threaded_client, (Client, new_socket))
    THREAD_COUNT += 1
