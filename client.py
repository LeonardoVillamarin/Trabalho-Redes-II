import socket
import threading



def listen_server(callback):
    try:
        while True:
            resp = tcp.recv(1024)
            callback(resp.decode())
    except Exception as e:
        print("Conexão finalizada")


def start_listener(callback):
    thread = threading.Thread(target=listen_server, args=(callback,))
    thread.start()


def conn(username, server_ip):
    global tcp
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = server_ip
    print(HOST)
    PORT = 5000

    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send(('{"Registro":"' + username + '"}').encode())

    resp = tcp.recv(1024)
    msg = resp.decode()
    if 'Usuário ja registrado' in msg:
        tcp.close()

    return msg


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