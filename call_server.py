import time

import pyaudio
import socket
from tkinter import *
import sounds


def init_call_server(current_ip, callback, window):
    HOST = current_ip
    PORT = 6000
    global udp
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (HOST, PORT)
    udp.bind(orig)
    print("Iniciando servidor")

    py_audio = pyaudio.PyAudio()
    buffer = 1024  # 127.0.0.1
    time.sleep(2)
    window.event_generate("<<newCall>>", data="params") #Todo: How send params to gui?
    while True:
        msg, client = udp.recvfrom(1024)
        print(client, msg.decode())
        if "convite" in msg.decode():
            json_resp = '{"convite":"' + str(msg) + '","client": "' + str(client) + '"}'
            callback(json_resp)  # Manda para view. Ela chama um método para responder

        elif "encerrar_ligacao" in msg.decode():
            # TODO: Para de enviar o audio. A conexão não deve ser encerrada aqui
            udp.close()

        else:
            print("Recebendo audio!")
            # Se não é nenhuma das opações acima, então é audio que tá chegando. Preciso reproduzir.
            output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
            output_stream.write(msg)


def answer_invitation(answer, dest):
    try:
        print("Resposta: " + answer)
        udp.sendto(answer.encode(), tuple(dest))
    except Exception as e:
        print("Deu erro:" + str(e))


def receive_call_popup(name="user", origin="('25.53.56.165', 57927)"):
    global call_window
    call_window = Toplevel()
    call_window.geometry("300x180")
    call_window.configure(background='#EFEFEF')
    call_window.title("Recebendo chamada")
    Label(call_window, text="Recebendo chamada de", background='#EFEFEF', fg='black', font=("Arial", 18)).pack(side="top")
    Label(call_window, text=name, background='#EFEFEF', fg='black', font=("Arial", 26, "bold")).pack()

    # photo_accept = PhotoImage(master=call_window, file="assets/images/accept_call_btn.png")
    # Button(call_window, text='Click Me !', image=photo_accept, command=lambda: answer_call(call_window, "aceito", origin)).place(x=90, y=100)

    # photo_reject = PhotoImage(master=call_window, file="assets/images/reject_call_btn.png")
    # Button(call_window, text='Click Me !', image=photo_reject, command=lambda: answer_call(call_window, "rejeitado", origin)).place(x=150, y=100)
    sounds.play_incoming_call_sound()
    call_window.mainloop()


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

# TODO: Chamar esse método sempre que receber uma nova data do servidor
# def listen_audio(output_stream, data):
#     output_stream.write(data)

# TODO: Adicionar uns states pra cuidar do ciclo de vida dessas threads


# port = randint(1000, 3000)
# print("Working on port: ", port)

# reactor.listenUDP(port, Client())
# reactor.run()
# start_protocol()
