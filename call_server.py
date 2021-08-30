import pyaudio
import threading


def start_protocol():
    print("Iniciando configuração do input/output stream")
    py_audio = pyaudio.PyAudio()
    buffer = 1024  # 127.0.0.1

    output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
    input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2, frames_per_buffer=buffer)
    # reactor.callInThread(self.record)

    thread = threading.Thread(target=record, args=(input_stream, buffer, output_stream))
    thread.start()


def record(input_stream, buffer, output_stream):
    print("Iniciando leitura do microfone")
    while True:
        data = input_stream.read(buffer)
        print(data)
        # transport.write(data, another_client) #Enviar data
        # Output stream está sendo enviado apenas para teste. Deve ser removido no futuro.
        output_stream.write(data) # Se der uma microfonia absurda, é pq tá funcionando


#TODO: Chamar esse método sempre que receber uma nova data do servidor
# def listen_audio(output_stream, data):
#     output_stream.write(data)


#port = randint(1000, 3000)
#print("Working on port: ", port)

# reactor.listenUDP(port, Client())
# reactor.run()
start_protocol()