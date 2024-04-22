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
import json
from _thread import start_new_thread
from datetime import datetime
import pytz
import os
import socket
import ast
import logging
import logging.config
import service.general as general
import service.emergency as emergency
import service.regular as regular
import service.tx_config as tx_config
import service.data_raw as data_raw

import socket_data_parser
import sys

sys.path.append("database")
sys.path.append("service")


THREAD_COUNT = 0

LAST_INDEX = -1

REGULAR_PACKET_TYPE = 1
EMERGENCY_PACKET_TYPE = 2
CMD_PACKET_TYPE = 3

GENERAL_TABLE_ID = 0
REGULAR_TABLE_ID = 1
EMERGENCY_TABLE_ID = 2

GREETINGS_LOG_FILE = "greetings.log"


def insert_table_data(data, table_id):
    """
    Функция insert_regular_table_data() вставляет полученные данные в таблицу базы данных,
    Он динамически строит SQL запрос на основе полученных данных.
    """

    # logger.info("Inserted data into %s - %s", table_id, data)

    if table_id == GENERAL_TABLE_ID:
        general.create_general(data)
    elif table_id == REGULAR_TABLE_ID:
        regular.create_regular(data)
    elif table_id == EMERGENCY_TABLE_ID:
        emergency.create_emergency(data)

    return -1


def check_for_greeting_message(bytes_message: bytes):
    message = bytes_message.decode()
    greeting_message = message[message.rindex("{") + 1: message.rindex("}")]
    greetings = greeting_message.split(':')
    if len(greetings) == 2:
        if greetings[0].strip() == "Hello from":
            log_text = "[{} - {}]".format(
                datetime.now(pytz.timezone('Asia/Atyrau')),
                greeting_message,
            )
            if os.path.exists(GREETINGS_LOG_FILE):
                with open(GREETINGS_LOG_FILE, "r+") as file:
                    content = file.read()
                    file.seek(0)
                    file.write(log_text + "\n" + content)
            else:
                with open(GREETINGS_LOG_FILE, "w+") as file:
                    file.write(log_text + "\n")
            return bytes(
                message[:message.rindex("{")] + message[message.rindex("}") + 1:],
                "utf-8",
            )
    return bytes_message


def make_dict_from_string(string_data):
    string_data = string_data.strip("{}")
    params = string_data.split(",")
    data = {}
    for param in params:
        key, value = param.split(":")
        key = key.strip()
        value = value.strip()
        if value.isdigit():
            if value == "-1":
                value = -1
            else:
                value = float(value)
        else:
            if "{" in value and "}" in value:
                value = make_dict_from_string(value)

        data[key] = value
    return data


def get_counters_params(packet: bytes):
    """
    :return: packet and list of param dictionaries
    """
    try:
        message = packet.decode()
        string_list = message[message.index('['): message.rindex("]") + 1]
        received_data = bytes(
            message[:message.index('[')] + message[message.rindex("]") + 1:],
            "utf-8",
        )
        try:
            params_list = ast.literal_eval(string_list)
            params = dict(
                counter_id=params_list[0],
                cell=params_list[1],
                current_a_volt=params_list[2],
                current_b_volt=params_list[3],
                current_c_volt=params_list[4],
                current_a_amper=params_list[5],
                current_b_amper=params_list[6],
                current_c_amper=params_list[7],
                frequency=params_list[8],
                power=params_list[9],
            )
            return received_data, params
        except Exception:
            print("No data for ce303 params")
            return received_data, None
    except ValueError:
        return packet, None


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
            if socket_data_parser.is_packet_valid(received_data):
                # logger.info("Raw view of data: %s", received_data)
                # logger.info("Data with length of %s", len(received_data))
                received_data = check_for_greeting_message(received_data)
                received_data, counters_params = get_counters_params(received_data)
                packet_type, object_id, dt, data = socket_data_parser.parse_socket_data(
                    received_data
                )

                print(data_raw.create_data_raw({'obj_num': object_id, 'dt': dt, 'text': received_data}))

                logger.info(
                    "Packet from object with id:%s, type of packet is %s, data is %s",
                    str(object_id),
                    str(packet_type),
                    data,
                )

                # если тип пакета REGULAR_PACKET_TYPE данные вставляем в таблицы REGULAR_TABLE_ID и GENERAL_TABLE_ID
                if packet_type == REGULAR_PACKET_TYPE:
                    for entry in data[:LAST_INDEX]:
                        insert_table_data(entry, REGULAR_TABLE_ID)
                    insert_table_data(data[LAST_INDEX], GENERAL_TABLE_ID)
                # если тип пакета EMERGENCY_PACKET_TYPE данные вставляем в таблицу EMERGENCY_TABLE_ID
                elif packet_type == EMERGENCY_PACKET_TYPE:
                    insert_table_data(data, EMERGENCY_TABLE_ID)

                received_data = b""

                # # Формируем ответ контроллеру
                msg = f"<OK{THREAD_COUNT}>"
                cmd = tx_config.read_unsended_tx_config(object_id)

                if abs((dt - datetime.now()).days) > 1:
                    now = str(datetime.now(pytz.timezone('Asia/Almaty')))
                    year = now[2:4]
                    month = now[5:7]
                    day = now[8:10]
                    hour = now[11:13]
                    minu = now[14:16]
                    sec = now[17:19]
                    msg = f"<SETTIME:+CCLK:  {year}/{month}/{day},{hour}:{minu}:{sec}>"
                elif cmd:
                    msg = f'<{cmd[0][2]}>'
                    tx_config.update_dt_2_tx_config(cmd[0][0])

                # Отпраляем ответ контроллеру
                logger.info("Sending : %s", msg)
                connection.sendall(msg.encode())
                break
        except ConnectionResetError:
            logger.info(address, "is reset connection")
            received_data = b""
            break
        except IndexError as i_e:
            logger.info(address, i_e.with_traceback, i_e)
        except ValueError as v_e:
            logger.info(address, v_e.with_traceback, v_e)
        except ConnectionAbortedError as c_a_e:
            logger.info(address, c_a_e.with_traceback, c_a_e)
            break
        except BrokenPipeError as b_p_e:
            logger.info(address, b_p_e.with_traceback, b_p_e)
            break

    connection.close()


# Получаем имя хоста
# HOSTNAME = socket.gethostname()
# По имени хоста получаем хоста
HOST = "0.0.0.0"
# Порт который будет слушиться
PORT = 8070
# По хосту получаем IP адрес
IP = socket.gethostbyname(HOST)
# подключаемся к базе данных

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("server")


try:
    # создаем серверный сокет
    ServerSideSocket = socket.socket()
    ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # связываем серверный сокет и адрес, порт хоста
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    logger.error(str(e))
logger.info("Socket is started on port '%s' under IP address '%s'", PORT, HOST)
# слушаем порт
ServerSideSocket.listen()

# цикл где принимаем все соединения
while True:
    # принимаем соединение от клиента
    Client, new_socket = ServerSideSocket.accept()
    Client.settimeout(60)
    logger.info("New connection from %s:%s", new_socket[0], new_socket[1])
    # создаем новый поток и начниаем там обработку клиента
    start_new_thread(multi_threaded_client, (Client, new_socket))
    THREAD_COUNT += 1
