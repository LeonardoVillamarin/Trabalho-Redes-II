import json
from time import sleep
from tkinter import *
from tkinter import messagebox
import call_manager
import call_server
import client as client
import sounds


def event_callback(e):
    """
    É chamado pelo client sempre que se recebe uma resposta do servidor. Tem a responsabilidade de identificar o tipo
    de resposta e tratar conforme necessário.
    :param e: evento de resposta (Em geral é uma string representando a resposta do servidor já decodificada.
    """
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

    except Exception as e:
        log("Erro ao processar resposta do servidor" + str(e))


def search_user():
    """
    Chamando ao clicar no botão de busca.
    Checa se existe algo no form field (Entry) de busca e chama os métodos do client de acordo com o dado recebido.
    """
    if len(find_user.get()) == 0:
        client.get_all_users()
    else:
        client.search_user(find_user.get())


def close_conn():
    """
    Chamando ao clicar no botão de sair.
    Solicita fechamento de conexão.
    """
    client.close_conn()
    exit(0)


def immediately(e):
    """
    Callback de eventos do listBox.
    Chamado automaticamente quando um usuário da lista é selecionado.
    """
    print("LB USERS: " + str(lb_users))
    index = lb_users.curselection()[0]
    global call_view_title
    global call_view_desc
    global call_btn
    call_btn['state'] = "active"

    # Limpa valores antigos antes de atualizar
    try:
        if call_view_title and call_view_desc:
            call_view_title.destroy()
            call_view_desc.destroy()
    except:
        log("Adicionando dados a view")

    call_view_title = Label(window, text=last_users['clients'][index]['user'], background='white', fg='black',
                            font=("Arial", 20, "bold"))
    call_view_title.place(x=500, y=400)
    call_view_desc = Label(window, text='IP: ' + last_users['clients'][index]['ip'] + 'Porta: ' +
                                        last_users['clients'][index]['port'], background='white', fg='black',
                           font=("Arial", 16))
    call_view_desc.place(x=500, y=430)


def set_users_list():
    """
    Atualiza lista de usuários
    """
    global lb_users
    lb_users = Listbox(window, width=40, height=21, background='#ffffff', foreground='black')
    if last_users:
        for user in last_users['clients']:
            lb_users.insert(END, user['user'])

    lb_users.place(x=40, y=200)
    lb_users.bind("<<ListboxSelect>>", immediately)


def log(message):
    """
    Adiciona mensagem de log ao logcat
    :param message: Messagem a ser adicionada
    """
    global lb_logcat
    lb_logcat.insert(END, message)


def set_logcat():
    """
    Definindo logcat na interface
    """
    global lb_logcat
    lb_logcat = Listbox(window, width=77, height=5, background='black', foreground='white')
    lb_logcat.insert(END, "Log:")
    lb_logcat.place(x=40, y=600)


def init_call():
    global call_window
    call_window = Toplevel()
    call_window.geometry("300x300")
    call_window.configure(background='#EFEFEF')
    call_window.title("Realizando chamada")
    call_manager.start_call(current_user, last_users['clients'][lb_users.curselection()[0]])
    call_window.mainloop()


def receive_call_popup():
    print("Recebendo chamada deste cliente: " + str(call_server_obj.current_client))

    if call_server_obj.current_client == {}:
        return

    origin = {"ip": call_server_obj.current_client["ip"], "port": call_server_obj.current_client["port"]}

    global call_window
    call_window = Toplevel()
    call_window.geometry("300x180")
    call_window.configure(background='#EFEFEF')
    call_window.title("Recebendo chamada")
    Label(call_window, text="Recebendo chamada de", background='#EFEFEF', fg='black', font=("Arial", 18)).pack(side="top")
    Label(call_window, text=call_server_obj.current_client["username"], background='#EFEFEF', fg='black', font=("Arial", 26, "bold")).pack()

    photo_accept = PhotoImage(master=call_window, file="assets/images/accept_call_btn.png")
    Button(call_window, text='Click Me !', image=photo_accept, command=lambda: answer_call(call_server_obj, call_window, "aceito", origin)).place(x=90, y=100)

    photo_reject = PhotoImage(master=call_window, file="assets/images/reject_call_btn.png")
    Button(call_window, text='Click Me !', image=photo_reject, command=lambda: answer_call(call_server_obj, call_window, "rejeitado", origin)).place(x=150, y=100)
    # sounds.play_incoming_call_sound()
    call_window.mainloop()


def answer_call(call_server_obj, popup, answer, origin):
    sounds.stop_incoming_call_sound()
    popup.destroy()
    call_server_obj.answer_invitation(answer, origin)


def set_home(current_ip, username=""):
    """
    Entry Point da home.
    Responsável por implementar toda a estrutura da interface gráfica
    :param current_ip: Ip atual
    :param username: Nome do usuário conectado
    """
    global window
    global current_user
    current_user = username
    window = Toplevel()
    window.geometry("800x740")
    window.configure(background='#EFEFEF')
    window.title("Calls UFF")

    Label(window, text="Olá, " + username.split(" ")[0].strip() + '.', background='#EFEFEF', fg='black',
                 font=("Arial", 24, "bold")).place(x=40, y=40)
    Label(window, text="Com quem vamos falar hoje?", background='#EFEFEF', fg='black', font=("Arial", 20))\
        .place(x=40, y=70)

    Label(window, text="Nome do usuário: ", background='#EFEFEF', fg='black', font=("Arial", 16)).place(x=40, y=115)
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
    global call_btn
    call_btn = Button(window, text="Chamar", command=init_call, bd=0, width=27, state="disabled",
                      highlightcolor='#EFEFEF')
    call_btn.place(x=460, y=535)

    set_logcat()
    search_user()
    global call_server_obj
    call_server_obj = call_server.CallServer(current_ip)
    client.start_listener(call_server_obj, event_callback, window)
    window.bind("<<newCall>>", receive_call_popup)
    window.mainloop()
