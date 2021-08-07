import socket
import json

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

clientes = {}

print("Servidor Iniciado")

while True:
    con, cliente = tcp.accept()
    print('Novo cliente conectado:', cliente)
    ip_cliente = cliente[0]
    port_cliente = cliente[1]

    while True:
        msg = con.recv(1024).decode()

        if "{" in msg:
            msg = json.loads(msg)

            if "Registro" in msg.keys():
                name = msg.get("Registro")
                if len(clientes) == 0:
                    clientes[name] = [ip_cliente, port_cliente]
                    con.sendall(b"Novo registro efetuado")
                    print("Clientes:")
                    for cliente in clientes:
                        print("Usuário: {}      IP: {}      Porta: {}".format(cliente, clientes[cliente][0], clientes[cliente][1]))
                else:
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
                if name in clientes:
                    con.sendall(("Usuário: "+name+"     Ip: "+str(ip_cliente)+"    Porta: "+str(port_cliente)).encode())
                else:
                    con.sendall(("Usuário não esta registrado").encode())
            elif "Encerrar" in msg.keys():
                name = msg.get("Encerrar")
                clientes.pop(name)
        if not msg: break
    
    print('Finalizando conexao do cliente', cliente)
    con.close()