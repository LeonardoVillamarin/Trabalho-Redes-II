import socket
from typing import ByteString 

HOST = '192.168.0.50'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

tcp.sendall(socket.gethostname().encode())
resp = tcp.recv(1024)
print(resp.decode())

msg = input("Para Desconectar: x\n")

while msg != 'x':
    resp = tcp.recv(1024)
    print(resp.decode())
    tcp.sendall(msg.encode())
    msg = input("Para Desconectar: x\n")
tcp.close()