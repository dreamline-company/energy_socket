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
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8070))


def send_ctrl():
    """
    The send_ctrl() function sends a sequence of bytes over the socket connection to the server.
    Each sock.send() call sends a specific value converted to bytes.
    The values represent different fields in the message,
    such as start and end symbols, message type, object number, temperature, voltage, etc.
    """
    now = datetime.now()
    sock.send(ord("<").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(int("1").to_bytes(1, "little"))  # type of msg 1
    sock.send(int("0x1", 16).to_bytes(2, "little"))  # object_number 2,3
    sock.send(ord("|").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(str(now).encode())  #
    sock.send(ord("|").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(int(256.4 * 10).to_bytes(2, "little"))  # temperature 4,5
    sock.send(int(5.2 * 10).to_bytes(2, "little"))  # voltage 6,7
    sock.send(int(22.3 * 10).to_bytes(2, "little"))  # temperature_cpu 8,9
    sock.send(int(0).to_bytes(2, "little"))  # restart_number 10,11
    sock.send(int(2).to_bytes(2, "little"))  # restart_number 10,11
    sock.send(ord("{").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(int("0xFF", 16).to_bytes(1, "little"))  # cell_number 12
    sock.send((7).to_bytes(1, "little"))  # 1byte of IO 13
    sock.send(ord("}").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(ord("{").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(int("0xAB", 16).to_bytes(1, "little"))  # cell_number 12
    sock.send((15).to_bytes(1, "little"))  # 1byte of IO 13
    sock.send(ord("}").to_bytes(1, "little"))  # start symbol idx 0
    sock.send(ord(">").to_bytes(1, "little"))  # end symbol idx 14


send_ctrl()
print(sock.recv(1024))
