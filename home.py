import json
from tkinter import *
from tkinter import messagebox
import controllers.client as client


def search_user():
    # Últimos usuários buscados
    global last_users
    if len(find_user.get()) == 0:
        msg = client.get_all_users()
        last_users = json.loads(msg)
    else:
        msg = client.search_user(find_user.get())
        last_users = json.loads(msg)

    set_users_list()


def set_users_list():
    lb_users = Listbox(window, width=40, height=21, background='#ffffff', foreground='black')
    if last_users:
        for user in last_users['clients']:
            lb_users.insert(END, user['user'])

    lb_users.place(x=40, y=200)


def set_home(username=""):
    global window
    window = Toplevel()
    window.geometry("800x600")
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

    search_user()

    window.mainloop()
