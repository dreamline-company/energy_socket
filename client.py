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
from datetime import datetime

s = input()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("13.51.162.215", 8070))
# sock.connect(("192.168.0.63", 8070))
sock.connect(("localhost", 8070))
if s == "1":
    sock.send(ord("<").to_bytes(1, "little"))  # start symbol idx 0
    sock.send((1).to_bytes(1, "little"))
    sock.send((1).to_bytes(2, "little"))
    sock.send(round(time.time() * 1000).to_bytes(8, "little"))
    sock.send(ord("{").to_bytes(1, "little"))
    for name in range(10):
        sock.send(name.to_bytes(2, "little"))
        sock.send(ord(",").to_bytes(1, "little"))
    sock.send(ord("}").to_bytes(1, "little"))
    sock.send(ord(">").to_bytes(1, "little"))
elif s == "2":
    sock.send(ord("<").to_bytes(1, "little"))  # start symbol idx 0
    sock.send((2).to_bytes(1, "little"))
    sock.send((1).to_bytes(2, "little"))
    sock.send(round(time.time() * 1000).to_bytes(8, "little"))
    sock.send(ord("{").to_bytes(1, "little"))
    for cell_number in range(2):
        if True:
            sock.send(cell_number.to_bytes(1, "little"))
            for register_number in range(10):
                sock.send(register_number.to_bytes(1, "little"))
                sock.send((register_number + 10).to_bytes(1, "little"))
                sock.send(ord(";").to_bytes(1, "little"))
            sock.send(ord(",").to_bytes(1, "little"))
    sock.send(ord("}").to_bytes(1, "little"))
    sock.send(ord(">").to_bytes(1, "little"))
elif s == "3":
    sock.send(ord("<").to_bytes(1, "little"))  # start symbol idx 0
    sock.send((3).to_bytes(1, "little"))
    sock.send((1).to_bytes(2, "little"))
    sock.send(round(time.time() * 1000).to_bytes(8, "little"))
    sock.send(ord("{").to_bytes(1, "little"))
    for i in range(10):
        sock.send(i.to_bytes(1, "little"))
        sock.send((i + 10).to_bytes(1, "little"))
        sock.send(ord(",").to_bytes(1, "little"))
    sock.send(ord("}").to_bytes(1, "little"))
    sock.send(ord(">").to_bytes(1, "little"))  # end symbol idx 14

print(sock.recv(1024))
