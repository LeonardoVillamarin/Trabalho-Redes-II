import socket
import threading
import pyaudio


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


def send_audio(udp, dest):
    py_audio = pyaudio.PyAudio()
    buffer = 1024

    #output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
    input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2, frames_per_buffer=buffer)

    while True:
        print("Enviando audio!")
        data = input_stream.read(buffer)
        # print(data)
        udp.sendto(data, dest)
        # Output stream está sendo enviado apenas para teste. Deve ser removido no futuro.
        # output_stream.write(data) # Se der uma microfonia absurda, é pq tá funcionando


def listen(udp):
    while True:
        msg, addrress = udp.recvfrom(1024)
        print("Recebi essa mensagem: " + str(msg) + " Veio desse endereço: " + str(addrress))
        if "aceito" in msg:
            print("Iniciando chamada")
            thread = threading.Thread(target=send_audio, args=(udp, addrress,))
            thread.start()


#TODO: Alguém precisa fechar esse tanto de thread aberta. Está gerendo travaentos ao encerrar o app.