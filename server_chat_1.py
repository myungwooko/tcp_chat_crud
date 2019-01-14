from  socket          import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading        import Thread
import sqlite3
import time
import datetime
from table           import Table as table
import model_methods


class Server_config:
    def __init__(self):
        self.config_setting()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True) ################################## socket option 바로 사용할수 있게 / 그전꺼 끝나도 반환하는거 안기다리고 바로 쓰겠다는 말
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
        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = "Welcome %s! Here are INSTRUCTIONS 4 OUR TCP_CHAT" % name
        instruction_for_users = "Type {users}        <-- WILL SHOW YOU ALL CONNECTED USERS LIST"
        instruction_for_msg   = "Type {messages} <-- WILL SHOW YOU ALL MESSAGES LIST"
        instruction_fot_quitting = "Type {quit}           <-- WILL TERMINATE YOUR CHAT WINDOW"
        self.bytes_and_send(client, '=====================================================================================================')
        time.sleep(0.01)
        self.bytes_and_send(client, welcome)
        time.sleep(0.01)
        self.bytes_and_send(client, instruction_for_users)
        time.sleep(0.01)
        self.bytes_and_send(client, instruction_for_msg)
        time.sleep(0.01)
        print(111)
        self.bytes_and_send(client, instruction_fot_quitting)
        time.sleep(0.01)
        self.bytes_and_send(client, '=====================================================================================================')
        time.sleep(0.01)
        print(222)
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        model_methods.add_user(name)

        while True:
            msg = client.recv(self.BUFSIZ)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            if msg == bytes("{quit}", "utf8"):
                self.handle_user_quit(client, name)
                break

            elif msg == bytes("{messages}", "utf8"):
                self.showing_all_msg(client)

            elif msg == bytes("{users}", "utf8"):
                self.showing_all_users(client)

            else:
                self.broadcast(msg, name + ": ")
                model_methods.insert_msg(msg, name, self.clients, st)


    def handle_user_quit(self, client, name):
        del self.clients[client]
        model_methods.delete_user(name)
        self.broadcast(bytes("%s has left the chat." % name, "utf8"))
        client.close()

    def showing_all_msg(self, client):
        messages = model_methods.all_messages()
        messages = self.messages_to_str_list(messages)
        self.bytes_and_send(client,"< Messages List > --------------------------------------------------------------------------------------------------------")
        time.sleep(0.01)
        self.data_dispaly(client, messages, 'Message')
        time.sleep(0.01)
        self.bytes_and_send(client,"--------------------------------------------------------------------------------------------------------------------------")


    def showing_all_users(self, client):
        users = model_methods.all_users()
        users = self.users_to_str_list(users)
        self.bytes_and_send(client, "< Users List > ------------------------------------------------------------------------------------------------------------")
        time.sleep(0.01)
        self.data_dispaly(client, users, 'User')
        time.sleep(0.01)
        self.bytes_and_send(client, "--------------------------------------------------------------------------------------------------------------------------")




    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    @staticmethod
    def bytes_and_send(client, msg):
        client.send(bytes(msg, "utf8"))

    @staticmethod
    def users_to_str_list(users):
        result = []
        for user in users:
            result.append(' ' + user[1])
        return result

    @staticmethod
    def messages_to_str_list(messages):
        result = []
        for unit in messages:
            print("unit: ", unit)
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
        count = 1
        for str_list in list_form:
            self.bytes_and_send(client, f"{type} {count}: " + str_list)

            time.sleep(.01)
            count = count + 1




table = table()
host_or_not = input("Are you host? [host/client]: ")
if host_or_not == "host":
    first_checker = input("You already made the table? [yes/first]: ")
    if first_checker == 'yes':
        table.drop_table()
    table.making_table()
    Server()
