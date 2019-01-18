from  socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


class host_and_port:
    def __init__(self, host, port):
        self.host = host
        self.port = port


class Setting_Tkinter(host_and_port):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.top = tkinter.Tk()
        self.top.title("Chatter")
        messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()
        scrollbar = tkinter.Scrollbar(messages_frame)
        self.msg_list = tkinter.Listbox(messages_frame, height=23, width=69, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        messages_frame.pack()
        entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()
        send_button = tkinter.Button(self.top, text="Send", command=self.send)
        send_button.pack()
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)


class Client(Setting_Tkinter):

    def __init__(self, host, port):
        super().__init__(host, port)
        ADDR = (self.host, self.port)
        self.BUFSIZ = 1024
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        receive_thread = Thread(target = self.receive)
        receive_thread.start()
        tkinter.mainloop()

    def receive(self):###################################################################################### button에 연결
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(tkinter.END, msg)
            except OSError:
                break

    def send(self, event=None):
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            self.top.quit()


    def on_closing(self, event=None):#################################################################### x 눌러서 끄는 경우
        self.my_msg.set("{quit}")
        self.send()

        # ## without Tkinter
# class Client(Setting_Tkinter):
#     def __init__(self, host, port):
#         self.sock = socket(AF_INET, SOCK_STREAM)
#         self.sock.connect((host,port))
#
#
#         iThread = Thread(target=self.sendMsg)
#         iThread.daemon = True
#         iThread.start()
#         while True:
#             data = self.sok.recv(1024)
#             if not data:
#                 break
#             print(str(data,"utf8"))
#
#R
#     def send(self):
#         while True:
#             self.sock.send(bytes(input(""), "utf8"))


host_or_not = input("Are you host? [host/client]: ")
if host_or_not == "client":
    HOST = input("Enter Host? ")
    PORT = input("Enter Port? ")
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)
    Client(HOST, PORT)

