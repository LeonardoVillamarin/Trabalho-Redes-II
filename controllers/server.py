import socket
import json

HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 52002  # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(5)

clientes = {}

print("Servidor Iniciado")

while True:
    con, cliente = tcp.accept()
    ip_cliente = cliente[0]
    port_cliente = cliente[1]

    while True:
        msg = con.recv(1024).decode()

        if "{" in msg:
            msg = json.loads(msg)

            if "Registro" in msg.keys():
                name = msg.get("Registro")
                if name not in clientes:
                    clientes[name] = [ip_cliente, port_cliente]
                    con.sendall(b"Novo registro efetuado")
                    print(clientes)
                else:
                    con.sendall(("Usuário ja registrado").encode())
                    if ip_cliente != clientes.get(name)[0] or port_cliente != clientes.get(name)[1]:
                        clientes[name] = [ip_cliente, port_cliente]
            elif "Consulta" in msg.keys():
                name = msg.get("Consulta")
                # se buscou com vazio, deve retornar todos os usuários
                if len(name) == 0:
                    response = '{"clients": ['
                    for client in clientes:
                        response += '{"user":"' + str(client) + '", "ip":"' + clientes.get(client)[0] + '", "port": "'\
                                    + str(clientes.get(client)[1]) + '"}'
                    response += ']}'
                    #TODO: Acrescentar uma virgula a cada iteração para o caso em que temos mais de um usuário
                    con.send(response.encode())

                # Caso contrário, retorna só a primeira ocorrência
                elif name in clientes:
                    con.send(('{"clients": [{"user":"' + name + '", "ip":"' + str(ip_cliente) + '", "port": "'
                              + str(port_cliente) + '"}]}').encode())
                else:
                    con.send('{"error": "Usuário não esta registrado"'.encode())
            elif "Encerrar" in msg.keys():
                name = msg.get("Encerrar")
                clientes.pop(name)
        if not msg:
            break

    print('Finalizando conexao do cliente', cliente)
    con.close()
