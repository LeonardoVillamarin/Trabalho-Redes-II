import json
from tkinter import *
from tkinter import messagebox
import client as client


def event_callback(e):
    log(e)
    try:
        msg = json.loads(e)
        if 'clients' in msg:
            global last_users
            last_users = msg
            set_users_list()
        elif 'event' in msg:
            search_user()
        elif 'error' in msg:
            messagebox.showerror("Error", msg['error'])

    except:
        log("Erro ao processar resposta do servidor")


def search_user():
    # Últimos usuários buscados
    if len(find_user.get()) == 0:
        client.get_all_users()
    else:
        client.search_user(find_user.get())


def close_conn():
    client.close_conn()
    exit(0)


# Callback de event do click no listBox
def immediately(e):
    index = lb_users.curselection()[0]
    global call_view_title
    global call_view_desc

    # Limpa valores antigos antes de atualizar
    try:
        if call_view_title and call_view_desc:
            call_view_title.destroy()
            call_view_desc.destroy()
    except:
        log("Adicionando dados a view")

    call_view_title = Label(window, text=last_users['clients'][index]['user'], background='white', fg='black',
                            font=("Arial", 20, "bold"))
    call_view_title.place(x=555, y=350)
    call_view_desc = Label(window, text='IP: ' + last_users['clients'][index]['ip'] + 'Porta: ' +
                                        last_users['clients'][index]['port'], background='white', fg='black',
                           font=("Arial", 16))
    call_view_desc.place(x=520, y=380)


def set_users_list():
    global lb_users
    lb_users = Listbox(window, width=40, height=21, background='#ffffff', foreground='black')
    if last_users:
        for user in last_users['clients']:
            lb_users.insert(END, user['user'])

    lb_users.place(x=40, y=200)
    lb_users.bind("<<ListboxSelect>>", immediately)


def log(message):
    global lb_logcat
    lb_logcat.insert(END, message)


def set_logcat():
    global lb_logcat
    lb_logcat = Listbox(window, width=77, height=5, background='black', foreground='white')
    lb_logcat.insert(END, "Log:")
    lb_logcat.place(x=40, y=600)


def set_home(username=""):
    global window
    window = Toplevel()
    window.geometry("800x740")
    window.configure(background='#EFEFEF')
    window.title("Calls UFF")

    desc = Label(window, text="Olá, " + username.split(" ")[0].strip() + '.', background='#EFEFEF', fg='black',
                 font=("Arial", 24, "bold"))
    desc.place(x=40, y=40)
    desc = Label(window, text="Com quem vamos falar hoje?", background='#EFEFEF', fg='black', font=("Arial", 20))
    desc.place(x=40, y=70)

    desc = Label(window, text="Nome do usuário: ", background='#EFEFEF', fg='black', font=("Arial", 16))
    desc.place(x=40, y=115)
    global find_user
    find_user = Entry(window, width=30, bg="white", fg="black", bd=1)
    find_user.place(x=40, y=140)

    button = Button(window, text="Buscar", command=search_user, background='#EFEFEF', activeforeground='#EFEFEF',
                    bd=0,
                    bg='#EFEFEF', highlightcolor='#EFEFEF')
    button.place(x=330, y=140)

    call_img = PhotoImage(file="assets/images/background_calls.png")
    call_background = Label(window, image=call_img, background='#EFEFEF')
    call_background.place(x=420, y=180)

    button = Button(window, text="Sair", command=close_conn,
                    bd=0,
                    bg='red', highlightcolor='#EFEFEF')
    button.place(x=700, y=10)

    set_logcat()
    search_user()
    client.start_listener(event_callback)
    window.mainloop()
