from home_layout import *
from tkinter import *
from tkinter import messagebox


def valid_information():
    if len(name.get()) > 0 and len(ip.get()) > 0:
        return True
    return False


def start_connection():
    if not valid_information():
        messagebox.showerror("Error", "Preencha todas as informações solicitadas.")
        return

    resp = client.conn(name.get(), ip.get())
    print(resp)
    if 'Novo registro efetuado' in resp:
        set_home(name.get())

    elif 'Usuário ja registrado' in resp:
        messagebox.showinfo("Atenção", "Usuário já registrado. Tente outro nome.")
        client.close_conn()

    else:
        messagebox.showerror("Error", "Erro ao fazer requisição: " + resp)


window = Tk()
window.geometry("530x600")
window.configure(background='#EFEFEF')
window.title("Calls UFF")

# Header
header_img = PhotoImage(file="assets/images/header.png")
header = Label(window, image=header_img, background='#EFEFEF')
header.place(x=15, y=15)

# Descrição
desc = Label(window, text="Antes de começar,", background='#EFEFEF', fg='black', font=("Arial", 20, "bold"))
desc.place(x=40, y=290)

desc = Label(window, text="precisamos de algumas informações", background='#EFEFEF', fg='black',
             font=("Arial", 20, "bold"))
desc.place(x=40, y=320)

# Content
view_img = PhotoImage(file="assets/images/view_background.png")
view = Label(window, image=view_img, background='#EFEFEF', )
view.place(x=15, y=360)

desc = Label(window, text="IP do servidor: ", background='#ffffff', fg='black', font=("Arial", 16))
desc.place(x=40, y=380)
ip = Entry(window, width=50, bg="white", fg="black", bd=1)
ip.place(x=40, y=410)

desc = Label(window, text="Nome de usuário: ", background='#ffffff', fg='black', font=("Arial", 16))
desc.place(x=40, y=440)
name = Entry(window, width=50, bg="white", fg="black", bd=1)
name.place(x=40, y=470)

# Todo: Botão com uma borda zoada d+. Preciso descobrir de onde isso vem.
button = Button(window, text="Conectar", command=start_connection, background='#EFEFEF', activeforeground='#EFEFEF', bd=0,
                bg='#EFEFEF', highlightcolor='#EFEFEF')
button.place(x=220, y=550)

window.mainloop()
