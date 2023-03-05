import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("64.226.72.254", 8080))
sock.send(b"GET / HTTP/1.1\r\nHost:64.226.72.254\r\n\r\n")
response = sock.recv(4096)
sock.close()
print(response.decode())
