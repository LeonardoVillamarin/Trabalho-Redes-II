import time
import pyaudio
import socket
import threading


class CallServer:
    def __init__(self, current_ip, sound_obj):
        self.current_client = {}
        self.in_call = False
        self.sound_obj = sound_obj
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
                self.current_client = {"username": msg.decode().split("/")[1], "ip": str(client[0]),
                                       "port": int(client[1])}
                time.sleep(2)
                print("Gerando event")
                self.sound_obj.play_incoming_call_sound()
                thread = threading.Thread(target=window.event_generate, args=("<<newCall>>",))
                thread.start()
                print("depois do event")
            elif "encerrar_ligacao" in str(msg):
                self.in_call = False
                print("Encerra ligação")
            else:
                print("Recebendo audio!")
                output_stream.write(msg)

    def answer_invitation(self, answer, dest):
        try:
            print("Resposta: " + answer)
            self.udp.sendto(answer.encode(), tuple([dest["ip"], dest["port"]]))

            if 'aceito' in answer:
                self.in_call = True
                thread = threading.Thread(target=self.send_audio, args=(self.udp, tuple([dest["ip"], dest["port"]]),))
                thread.start()

        except Exception as e:
            print("Deu erro:" + str(e))

    def send_audio(self, udp, dest):
        try:
            py_audio = pyaudio.PyAudio()
            buffer = 1024

            input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2,
                                         frames_per_buffer=buffer)
            while self.in_call:
                print("Enviando audio!")
                data = input_stream.read(buffer, exception_on_overflow = False)
                udp.sendto(data, dest)

            print("A chamada deve ser finalizada aqui!")

        except Exception as e:
            print(str(e))

