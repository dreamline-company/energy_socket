import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("167.71.43.13", 8080))

def sendRealTime(): 
    sock.send(ord('<').to_bytes(1, 'little'))#start of msg 0
    sock.send(int('0',16).to_bytes(1, 'little'))#type of msg 1
    sock.send(int('1',16).to_bytes(1, 'little'))#controller_id 2
    sock.send(int('AB',16).to_bytes(1, 'little'))#slave_id 3
    sock.send(int('1',16).to_bytes(1, 'little'))#register hi 4
    sock.send(int('25',16).to_bytes(1, 'little'))#register lo 5
    sock.send(int('AB',16).to_bytes(1, 'little'))#value 6
    sock.send(int('37',16).to_bytes(1, 'little'))#value 7
    sock.send(ord('>').to_bytes(1, 'little'))#end of msg 8
    
def sendCtrl():
    sock.send(ord('<').to_bytes(1, 'little'))#start of msg 0
    sock.send(int('1',16).to_bytes(1, 'little'))#type of msg 1
    sock.send(int('4',16).to_bytes(1, 'little'))#controller_id 2
    sock.send(int('3',16).to_bytes(1, 'little'))#current_a 3
    sock.send(int('4',16).to_bytes(1, 'little'))#current_b 4
    sock.send(int('5',16).to_bytes(1, 'little'))#current_c 5
    sock.send(ord('>').to_bytes(1, 'little'))#end of msg 6
try:
    sendCtrl()
except Exception as e:
    print(e)

print(sock.recv(1024))