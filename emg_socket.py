# EMG_skv. ivp
# Date: 17.11.2023

import socket
import struct
from datetime import datetime, timezone, timedelta
from _thread import start_new_thread
import mysql.connector
from mysql.connector import Error
from random import randint
from time import sleep

THREAD_COUNT = 0
CHAR_1 = 60
CHAR_END = 62
DIVIDER = 10.0
LAST_INDEX = -1
# Писать принятый пакет в таблицу без парсинга
fl_data_raw = False

# * * * * * * * * * * * * * * * * * * * * * * ФУНКЦИИ * * * * * * * * * * * * * * * * * * * * * *
# Строка текущего времени
def do_sTime():
    # dt = datetime.now() + timedelta(hours=6)
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')
     
# Запись подтверждения отправки команды контроллеру
def cmd_ok(id):
    global cnx
    res = True
    try:
        cursor = cnx.cursor()
        dt = datetime.now()
        dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        insert_sql = f"UPDATE tx_config SET dt2 = '{dt}' WHERE id = {id}"
        #print('id',id,insert_sql)
        cursor.execute(insert_sql)
        cnx.commit()
    except () as e:
        print(e,'bad') 
        res = False   
    finally:
        cursor.close()
    return res

# Наличие команды в таблице БД 'tx_config'
def get_cmd(skv_num):
    global cnx
    cmd = None
    try:
        cursor = cnx.cursor()
        insert_sql = f"SELECT id, cmd FROM tx_config WHERE skv_num = {skv_num} AND dt2 IS NULL"
        cursor.execute(insert_sql)
        cmd = cursor.fetchone()
        #print('cmd rx ->:',cmd)
        cnx.commit()
    except:
        print('NO Comand:',cmd,skv_num)
    finally:
        cursor.close()
    return cmd

# Устанавливает соединение с базой данных 
def create_server_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = database_name,
            port = DB_PORT,
        )
        return connection
    except Error as err:
        print(f"Error connection: '{err}'")
    
# Вставляем полученные данные в таблицы БД
def sql_data(arD):
    global cnx 
    res = None
    # Проверка подключения к БД
    if (cnx == None): 
        cnx = create_server_connection(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME)
        if (cnx == None):
            print('Нет подключения к базе данных!')
            return res
    elif cnx.is_connected() == False:
        cnx = create_server_connection(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME)  
        if (cnx == None):
            print('Нет подключения к базе данных!')
            return res
    
    cursor = cnx.cursor()
    insert_sql = ''
    skv_dan = ''
    pak_type = int(arD[0])
    skv_n = int(arD[1])
    if pak_type == 1:
        sTable = 'skv_onoff'
        # dt = datetime.now() + timedelta(hours=6)
        dt = datetime.now()
        dan = int(arD[2])
        insert_sql = (f"INSERT INTO skv_onoff (skv_num, dan, dt) VALUES ('{skv_n}', '{dan}','{dt}')")
    elif pak_type == 2:
        if len(arD) == 6:
            sTable = 'skv_dan'
            dt = datetime.fromtimestamp(int(arD[2]))
            avr = int(arD[3])
            insert_sql = (f"INSERT INTO skv_dan (skv_num, dt, avr, dan0, dan1) VALUES ('{skv_n}', '{dt}', '{avr}', '{arD[4]}', '{arD[5]}')")
        else: 
            insert_sql = (f"INSERT INTO data_raw (skv_num, skv_bytes) VALUES ('{skv_n}', '{arD}')")
    else: pass    
    try:
        cursor.execute(insert_sql)
        print(f"Insert data into {sTable}: {arD}")
        cnx.commit()
        res = True
    except:
        res = False
        print('Данные в БД не записаны!!!!!!!!!!!!!!!!!')
    finally:    
    #     cnx.commit()
        cursor.close()
    return res

# Проверка валидности принятого пакета
def is_data_valid(bdata):
    if bdata[0] == CHAR_1 and bdata[-1] == CHAR_END  and (bdata[1] in [49,50]):
        return True
    else: return False

# = = = = = = = = = = = = = = == = = = = = = = = = = = = = == = = = = = = = = = = = = = == = = = = = 
# Шаблоны
#s1 = '<1 1234 12>'
#s2 = '<2 1234 1699126211 3 {"t1":220,"t2":240,"V":243,"rst":10} {"i1":100,"i2":200,"v":300,"f":500}>'

# = = = = = = = = = = = = = = == = = = = = = Обработка подключеного клиента = == = = = = = = = = = = 
def multi_threaded_client(connection, address):
    id = 0
    cmd = ''
    res = 0
    receiv_data = b""
    msg = ''
    while True:
        try:
            receiv_data += connection.recv(1024)
            if not receiv_data: break
            if is_data_valid(receiv_data):
                print("rx data:", receiv_data)
                receiv_data = receiv_data[1:-1]
                sDan = receiv_data.decode()
                receiv_data = b""
                arDan = sDan.split()
                if sql_data(arDan) == True:
                    ar_cmd = get_cmd(int(arDan[1]))
                    print('ar_cmd',ar_cmd,type(ar_cmd))
                    #if isinstance(ar_cmd, tuple):
                    if ar_cmd != None:
                        id = ar_cmd[0]
                        cmd = ar_cmd[1] 
                        if len(cmd) >= 2 and cmd[:2] == 'T=':
                            cmd = 'T=' + do_sTime()
                        msg = f"OK: {cmd}" 
                        cmd_ok(id)
                    else: 
                        msg = f"OK: <{THREAD_COUNT}>"
                else:  msg = 'Err=2' 
            else: 
                msg = 'Err=1'

            print(f"Sending : {msg}")
            connection.sendall(msg.encode())
            break

        except ConnectionResetError:
            print(address, "reset connection")
            receiv_data = b""
            break
        except IndexError as i_e:
            print(address, i_e.with_traceback, i_e)
        except ValueError as v_e:
            print(address, v_e.with_traceback, v_e)
        except ConnectionAbortedError as c_a_e:
            print(address, c_a_e.with_traceback, c_a_e)
            break
        except BrokenPipeError as b_p_e:
            print(address, b_p_e.with_traceback, b_p_e)
            break
    connection.close()

# * * * * * * * * * * * * * * * * * * * * * * * * * * ЦИКЛ * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Получаем имя хоста
# HOSTNAME = socket.gethostname()
# По имени хоста получаем хост
HOST = "0.0.0.0"
PORT = 8111
IP = socket.gethostbyname(HOST)

IS_FILE_SENDING = {}
CONTENTOFTHEFILE = {}
line_index = {}

# Подключаемся к базе данных
DB_SERVER = "192.168.17.158"     #"194.87.238.61"	#"127.0.0.1"
DB_USERNAME = "eme_user"             #"root"  
DB_PASSWORD = "Eme2023*"      #""
DB_NAME = "emg_skv"
DB_PORT = 3306
cnx = create_server_connection(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME)

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")

# Создаем серверный сокет
try:
    ServerSocket = socket.socket()
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ServerSocket.bind((HOST, PORT))
    print("Socket started")
except socket.error as e:
    print('Socket:',str(e))

ServerSocket.listen()

# Цикл, где принимаем все соединения
while True:
    # принимаем соединение от клиента
    sleep(randint(1, 10))
    Client, new_socket = ServerSocket.accept()
    Client.settimeout(60)
    print("Connection from: " + new_socket[0] + ":" + str(new_socket[1]))
    # создаем новый поток и начниаем там обработку клиента
    start_new_thread(multi_threaded_client, (Client, new_socket))
    THREAD_COUNT += 1
