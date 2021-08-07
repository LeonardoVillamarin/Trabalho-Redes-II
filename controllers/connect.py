import socket
from tkinter import *

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def conn(username, server_ip):
    HOST = server_ip
    print(HOST)
    PORT = 5000  # Porta que o Servidor esta

    dest = (HOST, PORT)
    tcp.connect(dest)
    print("Vamos dar uma olhada nisso: ", socket.gethostname())
    tcp.sendall(('{"Registro":"' + socket.gethostname() + '"}').encode())

    resp = tcp.recv(1024)
    return resp.decode()

def sendMsg():
    msg = '{"Consulta":"' + usuario.get().split(":")[1].strip() + '"}'
    tcp.sendall(msg.encode())

    text = Label(window, text="")
    text.pack()

    resp = tcp.recv(1024)
    text["text"] = resp.decode()

    text.after(5000, text.destroy)


def closeConn():
    tcp.sendall(('{"Encerrar":"' + socket.gethostname() + '"}').encode())
    tcp.close()
