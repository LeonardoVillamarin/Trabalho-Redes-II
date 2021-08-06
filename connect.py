import socket
from tkinter import *

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
        HOST = str(ip.get()).split(":")[1].strip()
        print(HOST)
        PORT = 5000            # Porta que o Servidor esta
        
        button.destroy()
        ip.destroy()
        
        dest = (HOST, PORT)
        tcp.connect(dest)

        tcp.sendall(('{"Registro":"'+socket.gethostname()+'"}').encode())

        resp = tcp.recv(1024)
        text["text"] = resp.decode()
        text.after(2000, text.destroy)

        global usuario
        usuario = Entry(window, width=50, bg="white", fg="black")
        usuario.pack(padx=100, pady=20)
        usuario.insert(0, "Digite o nome do usuário: ")

        button2 = Button(window, text="Enviar", command=sendMsg)
        button2.pack(padx=10, pady=10, side=LEFT)

        button3 = Button(window, text="Desconectar", command=closeConn)
        button3.pack(padx=10, pady=10,side=RIGHT)

def sendMsg():
        msg = '{"Consulta":"'+usuario.get().split(":")[1].strip()+'"}'
        tcp.sendall(msg.encode())

        text = Label(window, text="")
        text.pack()

        resp = tcp.recv(1024)
        text["text"] = resp.decode()

        text.after(5000, text.destroy)

def closeConn():
        tcp.sendall(('{"Encerrar":"'+socket.gethostname()+'"}').encode())
        tcp.close()
        window.destroy()

window = Tk()
window.geometry("500x500")
window.title("Trabalho Part I")

ip = Entry(window, width=50, bg="white", fg="black")
ip.pack(padx= 100, pady= 30)
ip.insert(0, "Digite o IP: ")

text = Label(window, text="")
text.pack(padx= 100, pady= 30)
button = Button(window, text="Confirmar", command=conn)
button.pack(padx= 100, pady= 30)

window.mainloop()

