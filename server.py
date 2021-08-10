import socket
import json
import threading


HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 5001  # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(5)

clientes = {}

print("Servidor Iniciado")


def sendall(con, origin):
    for client in clientes:
        if client != origin:
            con.send(('{"event":' + origin + " está online!}").encode())


def in_communication(client, con):
    ip_cliente = client[0]
    port_cliente = client[1]

    while True:
        msg = con.recv(1024).decode()

        if "{" in msg:
            msg = json.loads(msg)

            if "Registro" in msg.keys():
                name = msg.get("Registro")
                if name not in clientes:
                    clientes[name] = [ip_cliente, port_cliente]
                    con.send("Novo registro efetuado".encode())
                    print(clientes)
                    sendall(con, name)
                else:
                    con.send(("Usuário ja registrado").encode())
                    # if ip_cliente != clientes.get(name)[0] or port_cliente != clientes.get(name)[1]:
                    #     clientes[name] = [ip_cliente, port_cliente]
            elif "Consulta" in msg.keys():
                name = msg.get("Consulta")
                # se buscou com vazio, deve retornar todos os usuários
                # Todo: Melhorar a montagem desse json
                if len(name) == 0:
                    i = 0
                    response = '{"clients": ['
                    for client in clientes:
                        response += '{"user":"' + client + '", "ip":"' + clientes.get(client)[0] + '", "port": "'\
                                    + str(clientes.get(client)[1])
                        if i == len(clientes)-1:
                            response += '"}'
                        else:
                            response += '"},'
                        i += 1

                    response += ']}'
                    con.send(response.encode())

                # Caso contrário, retorna só a primeira ocorrência
                elif name in clientes:
                    con.send(('{"clients": [{"user":"' + name + '", "ip":"' + str(ip_cliente) + '", "port": "'
                              + str(port_cliente) + '"}]}').encode())
                else:
                    con.send('{"error": "Usuário não esta registrado"}'.encode())
            elif "Encerrar" in msg.keys():
                break
        if not msg:
            break

    print('Finalizando conexao do cliente', client)
    clientes.pop(client)
    con.close()


while True:
    con, client = tcp.accept()
    thread = threading.Thread(target=in_communication, args=(client,con,))
    thread.start()
