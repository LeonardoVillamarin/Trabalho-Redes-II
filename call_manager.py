import socket


HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 6000          # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
msg = "Esta mensagem está vindo do cliente A para o B!"
print("Começando!")
while msg != '\x18':
    udp.sendto(msg.encode(), dest)
    msg = input()
udp.close()