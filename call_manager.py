import socket
import threading
import pyaudio


class CallManager:

    def __init__(self, origin, dest_server, call_window, ring_sound):
        print(" Destino: " + str(dest_server))
        HOST = dest_server['ip']
        PORT = 6004
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.in_call = False
        self.ring_sound_obj = ring_sound
        self.call_window_obj = call_window
        dest = (HOST, PORT)
        thread = threading.Thread(target=self.listen, args=(self.udp,))
        thread.start()
        self.send_message(("convite/" + origin), dest)

    def send_message(self, msg, dest):
        print("Enviando mensagem: " + msg)
        self.udp.sendto(msg.encode(), dest)

    def listen(self, udp):
        py_audio = pyaudio.PyAudio()
        buffer = 4096
        output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2,
                                      frames_per_buffer=buffer)
        while True:
            try:
                msg, addrress = udp.recvfrom(buffer)
                print("Recebi essa mensagem: " + str(msg) + " Veio desse endereço: " + str(addrress))
                if "aceito" in str(msg):
                    print("Iniciando chamada")
                    self.in_call = True
                    self.ring_sound_obj.stop_all_sounds()
                    thread = threading.Thread(target=self.send_audio, args=(addrress,))
                    thread.start()

                if "rejeitado" in str(msg):
                    self.ring_sound_obj.stop_all_sounds()
                    self.call_window_obj.destroy()

                elif "encerra_ligacao" in str(msg):
                    self.call_window_obj.destroy()
                    self.in_call = False

                if self.in_call:
                    output_stream.write(msg)

            except Exception as e:
                print("Error: " + str(e))

    def send_audio(self, dest):
        try:
            py_audio = pyaudio.PyAudio()
            buffer = 1024

            input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2,
                                         frames_per_buffer=buffer)

            while self.in_call:
                print("Enviando audio!")
                data = input_stream.read(buffer, exception_on_overflow=False)
                self.udp.sendto(data, dest)

            print("Hora de finalizar a chamada!")
            self.udp.sendto("encerra_ligacao".encode(), dest)
            self.call_window_obj.destroy()

        except Exception as e:
            print(str(e))

    def end_call(self):
        self.call_window_obj.destroy()
        self.ring_sound_obj.stop_all_sounds()
        self.in_call = False

# TODO: Alguém precisa fechar esse tanto de thread aberta. Está gerendo travaentos ao encerrar o app.