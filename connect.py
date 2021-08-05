import socket

HOST = input("IP do Servidor: ")   # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

tcp.sendall(('{"Registro":"'+socket.gethostname()+'"}').encode())

resp = tcp.recv(1024)
print(resp.decode())

opcao = int(input("1. Buscar usuário\n2. Desconectar\n"))
if opcao == 1:
        nomeUsuario = input("Digite o nome do usuário: ")
        msg = '{"Consulta":"'+nomeUsuario+'"}'
        tcp.sendall(msg.encode())
        
while opcao != 2:
    resp = tcp.recv(1024)
    print(resp.decode())
    opcao = int(input("1. Buscar usuário\n2. Desconectar\n"))
    if opcao == 1:
        nomeUsuario = input("Digite o nome do usuário: ")
        msg = '{"Consulta":"'+nomeUsuario+'"}'
        tcp.sendall(msg.encode())
tcp.sendall(('{"Encerrar":"'+socket.gethostname()+'"}').encode())
tcp.close()