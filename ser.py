import socket
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import os
from _thread import *

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        for i in data:
            print(i)
        connection.sendall(str.encode(response))
    connection.close()

HOST = '167.71.43.13'
PORT = 8080  
IP = socket.gethostbyname(HOST)
ServerSideSocket = socket.socket()
ThreadCount = 0

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")

try:
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()