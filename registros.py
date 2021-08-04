import socket


HOST = '192.168.0.50'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

clientes = []

print("Servidor Iniciado")

while True:
    con, cliente = tcp.accept()
    print('Novo cliente conectado:', cliente)

    while True:
        msg = con.recv(1024)
        msg = msg.decode()

        print("Clientes Cadastrados: ")
        print(clientes)
        if len(clientes) == 0:
            print("Cliente não registrado")
            clientes.append([msg, cliente[0], cliente[1]])
            print("Efetuado cadastro do novo cliente")
            con.sendall(b"Novo registro efetuado")
        else:
            for cliente in clientes:
                if msg not in cliente:
                    print("Cliente não registrado")
                    clientes.append([msg, cliente[0], cliente[1]])
                    print("Efetuado cadastro do novo cliente")
                    con.sendall(b"Novo registro efetuado")
                else:
                    print("Cliente já registrado")
                    con.sendall(b"Cliente ja registrado")
        if not msg: break
    print('Finalizando conexao do cliente', cliente)
    con.close()