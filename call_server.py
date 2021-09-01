import pyaudio
import threading
from time import sleep

import socket


# def start_protocol(current_client, target_client):
#     print("Iniciando chamada de " + str(current_client) + " para: " + str(target_client))
#     py_audio = pyaudio.PyAudio()
#     buffer = 1024  # 127.0.0.1
#
#     output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
#     input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2, frames_per_buffer=buffer)
#
#     thread = threading.Thread(target=record, args=(input_stream, buffer, output_stream))
#     thread.start()
#
#     thread = threading.Thread(target=start_ring, args=(py_audio, buffer,))
#     thread.start()
#
#
# def record(input_stream, buffer, output_stream):
#     print("Iniciando leitura do microfone")
#     while True:
#         data = input_stream.read(buffer)
#         # print(data)
#         # transport.write(data, another_client) #Enviar data
#         # Output stream está sendo enviado apenas para teste. Deve ser removido no futuro.
#         # output_stream.write(data) # Se der uma microfonia absurda, é pq tá funcionando
#
#
# def start_ring(py_audio, buffer):
#     print("Vou falar")
#     ring_output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=2092, channels=2,
#                                        frames_per_buffer=buffer)
#     while True:
#         for n in range(600):
#             ring_output_stream.write("\x00\x30\x5a\x76\x7f\x76\x5a\x30\x00\xd0\xa6\x8a\x80\x8a\xa6\xd0")
#         sleep(3)

#TODO: Chamar esse método sempre que receber uma nova data do servidor
# def listen_audio(output_stream, data):
#     output_stream.write(data)

#TODO: Adicionar uns states pra cuidar do ciclo de vida dessas threads


#port = randint(1000, 3000)
#print("Working on port: ", port)

# reactor.listenUDP(port, Client())
# reactor.run()
#start_protocol()

HOST = '127.0.0.1'              # Endereco IP do Servidor
PORT = 6000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)
print("Começando servidor B!")
while True:
    msg, cliente = udp.recvfrom(1024)
    print(cliente, msg.decode())
udp.close()
