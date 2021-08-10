import socket
import threading

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def listen_server(callback):
    while True:
        resp = tcp.recv(1024)
        callback(resp.decode())


def start_listener(callback):
    thread = threading.Thread(target=listen_server, args=(callback,))
    thread.start()


def conn(username, server_ip):
    HOST = server_ip
    print(HOST)
    PORT = 5001

    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send(('{"Registro":"' + username + '"}').encode())

    resp = tcp.recv(1024)
    return resp.decode()


def search_user(username):
    msg = '{"Consulta":"' + username + '"}'
    tcp.send(msg.encode())


def get_all_users():
    msg = '{"Consulta":"''"}'
    tcp.send(msg.encode())


def close_conn(username=" "):
    try:
        tcp.send(('{"Encerrar":"' + username + '"}').encode())
        tcp.close()
    except:
        print("______")