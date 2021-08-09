import socket

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def conn(username, server_ip):
    HOST = server_ip
    print(HOST)
    PORT = 52002  # Porta que o Servidor esta

    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send(('{"Registro":"' + username + '"}').encode())

    resp = tcp.recv(1024)
    return resp.decode()


def search_user(username):
    msg = '{"Consulta":"' + username + '"}'
    tcp.send(msg.encode())

    resp = tcp.recv(1024)
    return resp.decode()


def get_all_users():
    msg = '{"Consulta":"''"}'
    tcp.send(msg.encode())

    resp = tcp.recv(1024)
    return resp.decode()


def close_conn(username):
    tcp.sendall(('{"Encerrar":"' + username + '"}').encode())
    tcp.close()