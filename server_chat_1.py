from  socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sqlite3
import time
import datetime
import tables
import model_methods

conn = sqlite3.connect("tcp_chat")
c = conn.cursor()
tables.making_table(c)

class Server_config:
    def __init__(self):
        self.config_setting()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(self.ADDR)
        self.sock.listen(5)
        print("Waiting for connection...")
        accepted_thread = Thread(target=self.accepted_incoming_connections)
        self.thread_start(accepted_thread)
        self.sock.close()

    def accepted_incoming_connections(self):
        pass

    @classmethod
    def config_setting(cls):
        cls.clients = {}
        cls.addresses = {}
        HOST = ''
        PORT = 33000
        cls.BUFSIZ = 1024
        cls.ADDR = (HOST,PORT)

    @staticmethod
    def thread_start(thread):
        thread.start()
        thread.join()

class Server(Server_config):
    def __init__(self):
        super().__init__()


    def accepted_incoming_connections(self):
        while True:
            client, client_address = self.sock.accept()
            print("%s %s has connected" % client_address)
            self.bytes_and_send(client, "Greetings from the cave! Now type your name and press enter!")
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()


    def handle_client(self, client):
        with sqlite3.connect("tcp_chat") as conn:   ####################################################
            c = conn.cursor()
        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = "Welcome %s! If you ever want to quit, type {quit} to exit." % name
        self.bytes_and_send(client, welcome)
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        model_methods.add_user(name)


        while True:
            msg = client.recv(self.BUFSIZ)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            if msg == bytes("{quit}", "utf8"):
                del self.clients[client]
                model_methods.delete_user(name)
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                client.close()
                break


            elif msg == bytes("{messages}", "utf8"):
                print(model_methods.all_messages())
                messages = model_methods.all_messages()
                messages = self.messages_to_str_list(messages)
                self.bytes_and_send(client, "--------------------------------------------------------------------------------------------------------------------------")
                time.sleep(0.01)
                self.data_dispaly(client, messages, 'message')
                time.sleep(0.01)
                self.bytes_and_send(client, "--------------------------------------------------------------------------------------------------------------------------")


            elif msg == bytes("{users}", "utf8"):
                print(model_methods.all_users())
                users = model_methods.all_users()
                users = self.users_to_str_list(users)
                self.bytes_and_send(client, "--------------------------------------------------------------------------------------------------------------------------")
                time.sleep(0.01)
                self.data_dispaly(client, users, 'user')
                time.sleep(0.01)
                self.bytes_and_send(client, "--------------------------------------------------------------------------------------------------------------------------")
            else:
                self.broadcast(msg, name + ": ")
                model_methods.insert_msg(msg, name, self.clients, st)


    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    @staticmethod
    def bytes_and_send(client, msg):
        client.send(bytes(msg, "utf8"))

    @staticmethod
    def users_to_str_list(users):
        result = ['Users List:']
        for user in users:
            result.append(user[1])
        return result

    @staticmethod
    def messages_to_str_list(messages):
        result = ['Messages List:']
        for unit in messages:
            message = unit[1]
            sender = unit[2]
            receiver = ""
            created_at = unit[len(unit)-1]

            count = 0
            last_idx = len(unit) - 1

            for ele in unit:
                if count >= 3 and count < last_idx:
                    if ele == sender:
                        pass
                    elif count == last_idx - 1:
                        receiver = receiver + ele
                    else:
                        receiver = receiver + ele + ", "
                else:
                    pass
                count = count + 1

            if receiver == "":
                receiver = f"{sender} is ONLY User"

            unit_result = f"<message: {message}, sender: {sender}, receiver: {receiver}, created_at: {created_at}>"
            result.append(unit_result)
        return result


    def data_dispaly(self, client, list_form, type):
        print(list_form)
        count = 0
        for str_list in list_form:
            if count != 0:
                self.bytes_and_send(client, f"{type} {count}: " + str_list)
            else:
                self.bytes_and_send(client, str_list)
            time.sleep(.01)
            count = count + 1


host_or_not = input("Are you host? [y/client]: ")
if host_or_not == "y":
    Server()

