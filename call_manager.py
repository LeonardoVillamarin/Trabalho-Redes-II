import socket
import threading


def start_call(origin, dest_server, callback):
    print(" Destino: " + str(dest_server))
    HOST = dest_server['ip']
    PORT = 6000
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    thread = threading.Thread(target=listen, args=(udp,))
    thread.start()
    send_message("convite/" + origin + "IP/PORTA", udp, dest)


def send_message(msg, udp, dest):
    print("Enviando mensagem: " + msg)
    udp.sendto(msg.encode(), dest)


def listen(udp):
    msg, addrress = udp.recvfrom(1024)
    print("Recebi essa mensagem: " + str(msg) + " Veio desse endereço: " + str(addrress))

