import socket
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

HOST = '167.71.43.13'
PORT = 8080  
IP = socket.gethostbyname(HOST)

print(f"Hostname: {HOST}")
print(f"IP Address: {IP}")

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        count = 0
        print(f"Connected by {addr}")
        while 200 < count:
            data = conn.recv(1024)
            if not data:
                break
            print(data)
            print(data)
            conn.sendall(b"OK!Recv")
            count = count + 0.01
        s.close()
        s.detach()