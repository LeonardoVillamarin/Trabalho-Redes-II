import time

import pyaudio
import socket
from tkinter import *
import sounds


class CallServer:
    def __init__(self, current_ip):
        self.current_client = {}
        HOST = current_ip
        PORT = 6004
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (HOST, PORT)
        self.udp.bind(orig)
        print("Socket de ligação criado")

    def init_call_server(self, window):
        print("Iniciando servidor")

        py_audio = pyaudio.PyAudio()
        buffer = 4096
        output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2,
                                      frames_per_buffer=buffer)
        while True:
            print("Iniciando o listen")
            msg, client = self.udp.recvfrom(buffer)
            print(client, str(msg))
            print("Vou testar com " + str(msg))
            if "convite" in str(msg):
                self.current_client = {"username": msg.decode().split("/")[1], "ip": str(client[0]), "port": int(client[1])}
                time.sleep(2)
                print("Gerando event")
                window.event_generate("<<newCall>>")
            elif "encerrar_ligacao" in str(msg):
                # TODO: Para de enviar o audio. A conexão não deve ser encerrada aqui
                self.udp.close()
            else:
                print("Recebendo audio!")
                # Se não é nenhuma das opações acima, então é audio que tá chegando. Preciso reproduzir.

                output_stream.write(msg)

    def answer_invitation(self, answer, dest):
        try:
            print("Resposta: " + answer)
            self.udp.sendto(answer.encode(), tuple(dest))
        except Exception as e:
            print("Deu erro:" + str(e))

