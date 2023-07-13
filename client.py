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
import time

s = input()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("13.51.162.215", 8070))
# sock.connect(("192.168.0.63", 8070))
sock.connect(("192.168.1.2", 8070))
emergency_packet_data = {16: b'\x89\xc3\x00\x00', 17: b'\x89\xc3\x00\x00'}
cell_regular_values = {}
dict_val = {'t2': 0, 're': 0, 'v1': 0, 't1': 0, 'ms': 255}
if s == "2":
    sock.send(bytearray([ord("<")]) + (1).to_bytes(2, "little") + bytearray(
        [2]) + round(time.time()).to_bytes(4, "little") + bytearray([ord("{")]))
    for cell_number, cell_value in emergency_packet_data.items():
        sock.send(cell_number.to_bytes(2, "little"))
        sock.send(cell_value)
        sock.send(ord(",").to_bytes(1, "little"))
    sock.send(bytearray([ord("}"), ord(">")]))
elif s == "1":
    sock.send(bytearray([ord("<")]) + (1).to_bytes(2, "little") + bytearray(
        [1]) + round(time.time()).to_bytes(4, "little") + bytearray([ord("{")]))
    for cell_number, cell_value in cell_regular_values.items():
        sock.send(cell_number.to_bytes(1, "little"))
        for reg_num, reg_value in cell_value.items():
            sock.send(reg_num.to_bytes(2, "little"))
            sock.send(ord(':').to_bytes(1, "little"))
            sock.send(reg_value)
            sock.send(ord(";").to_bytes(1, "little"))
        sock.send(ord(",").to_bytes(1, "little"))
    sock.send(bytearray([ord("}"), ord("{")]))
    for name, value in dict_val.items():
        sock.send(name.encode())
        sock.send(str(value).encode())
        sock.send(ord(',').to_bytes(1, "little"))
    sock.send(bytearray([ord("}"), ord(">")]))
print(sock.recv(1024))
