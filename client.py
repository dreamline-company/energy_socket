"""
The code you provided establishes a TCP connection to a server using the socket module. 
It then defines a function send_ctrl() to send a series of messages over the socket connection. 
The messages appear to be a specific protocol with predefined values.

The code then enters an infinite loop where it repeatedly calls send_ctrl() 
and prints the received data from the server using sock.recv(1024).

It's important to note that this code snippet does not include 
error handling or proper termination of the socket connection, 
which should be implemented in a real-world scenario.

If you have any specific questions or concerns regarding this code, please let me know.

Author: Amirkhan Orazbay
Date: 02.06.2023
"""
import socket
import re
import time
import struct
from const import *

print(str(round(time.time())).encode())
s = input()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((s, 8070))
cell_emergency_mapped_view = {1: [1, 2], 2: [3, 4]}
cell_regular_values = {}
dict_val = {"t_air": 22.2, "reset": 13, "VP": 225.2, "t_cpu": 22.2, "stat": 255}
s = input()
IS_FILE_DONWLOAD = False
IS_FILE_SUCCESS = False
new_file_name = ""
if s == "2":
    sock.send(b"<521700136071{0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,13:0,16:128,17:128,18:128,}>")
elif s == "1":
    sock.send(
        b"<211697310471{16|0014:32768;0030:32768;0032:32768;0034:32768;0036:32768;,17|0014:32768;0030:32768;0032:32768;0034:32768;0036:32768;,18|0014:32768;0030:32768;0032:32768;0034:32768;0036:32768;,}{reset:0,t_cpu:32.06463,VP:24.242,t_air:28.375,stat:0,}>"
    )


print(sock.recv(1024).decode())

sock.close()
