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

print(int.from_bytes(round(time.time()).to_bytes(4, "little"), "little"))
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
    packet = [
        PACKET_START_CHARACTER,
        OBJECT_ID,
        EMERGENCY_PACKET_TYPE,
        str(round(time.time())).encode(),
        DATA_START_CHARACTER,
    ]
    for cell_number in sorted(cell_emergency_mapped_view.keys()):
        packet.extend(
            (
                cell_number.to_bytes(2, "little"),
                sum(cell_emergency_mapped_view[cell_number]).to_bytes(1, "little"),
                DATA_DELIMITER,
            )
        )
    packet.extend((DATA_END_CHARACTER, PACKET_END_CHARACTER))
    print(packet)
    for i in packet:
        sock.send(i)
elif s == "1":
    packet = [
        PACKET_START_CHARACTER,
        OBJECT_ID,
        REGULAR_PACKET_TYPE,
        round(time.time()).to_bytes(4, "little"),
        DATA_START_CHARACTER,
    ]
    for cell_number in sorted(cell_regular_values.keys()):
        packet.append(cell_number.to_bytes(1, "little"))
        for reg_num in sorted(cell_regular_values[cell_number].keys()):
            packet.extend(
                (
                    reg_num,
                    REGISTER_NUM_VALUE_DELIMITER,
                    cell_regular_values[cell_number][reg_num],
                    REGISTER_DELIMITER,
                )
            )
        packet.append(DATA_DELIMITER)
    packet.extend((DATA_END_CHARACTER, DATA_START_CHARACTER))
    for name, value in dict_val.items():
        packet.extend(
            (name.encode(), b':', str(value).encode(), DATA_DELIMITER)
        )
    packet.extend((DATA_END_CHARACTER, PACKET_END_CHARACTER))
    print(packet)
    for i in packet:
        sock.send(i)
print(sock.recv(1024).decode())