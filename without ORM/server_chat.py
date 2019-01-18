from  socket          import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading        import Thread
import time
import datetime
from table           import Table as table
import model_methods
# from sqlalchemy import create_engine




# engine = create_engine('sqlite:///tcp_chat.db', echo=True)





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
            unique_number = client_address[1]
            self.bytes_and_send(client, "Greetings from the cave! Now type your name and press enter!")
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client, unique_number)).start()

    def handle_client(self, client, unique_number):
        name = client.recv(self.BUFSIZ).decode("utf8")
        self.handle_greeting(name, client)
        if len(self.clients.values()) == 0:
            self.clients[client] = (name, unique_number)
            model_methods.add_new_chatroom_id(unique_number)
        else:
            self.clients[client] = (name, unique_number)

        chatRoomNumber_id = model_methods.getting_chatroom_id()
        model_methods.add_user(name, unique_number, chatRoomNumber_id)
        self.clients[client] = (name, unique_number)

        while True:
            msg = client.recv(self.BUFSIZ)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            if msg == bytes("{quit}", "utf8"):
                self.handle_user_quit(client, name)
                break

            elif msg == bytes("{messages}", "utf8"):
                self.showing_all_msg(client, chatRoomNumber_id)

            elif msg == bytes("{users}", "utf8"):
                self.showing_all_users(client, self.clients, chatRoomNumber_id)

            else:
                self.broadcast(msg, name + ": ")
                model_methods.insert_msg(msg, (name, unique_number), self.clients, chatRoomNumber_id, st)

    def handle_greeting(self, name, client):
        welcome = "Welcome %s! Here are INSTRUCTIONS 4 OUR TCP_CHAT" % name
        instruction_for_users = "Type {users}        <-- WILL SHOW YOU ALL CONNECTED USERS LIST"
        instruction_for_msg   = "Type {messages} <-- WILL SHOW YOU ALL MESSAGES LIST ** receiver doesn't repeat sender itself **"
        instruction_fot_quitting = "Type {quit}           <-- WILL TERMINATE YOUR CHAT WINDOW"
        self.bytes_and_send(client, '=====================================================================================================')
        time.sleep(0.01)
        self.bytes_and_send(client, welcome)
        time.sleep(0.01)
        self.bytes_and_send(client, instruction_for_users)
        time.sleep(0.01)
        self.bytes_and_send(client, instruction_for_msg)
        time.sleep(0.01)
        self.bytes_and_send(client, instruction_fot_quitting)
        time.sleep(0.01)
        self.bytes_and_send(client, '=====================================================================================================')
        time.sleep(0.01)
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf8"))

    def handle_user_quit(self, client, name):
        del self.clients[client]
        self.broadcast(bytes("%s has left the chat." % name, "utf8"))
        client.close()

    def showing_all_msg(self, client, chatRoomNumber_id):
        messages = model_methods.all_messages(chatRoomNumber_id)
        messages = self.messages_to_str_list(messages)
        self.bytes_and_send(client,"< Messages List > --------------------------------------------------------------------------------------------------------")
        time.sleep(0.01)
        self.data_display(client, messages, 'Message')
        time.sleep(0.01)
        self.bytes_and_send(client,"--------------------------------------------------------------------------------------------------------------------------")


    def showing_all_users(self, client, clients, chatRoomNumber_id):
        users_name_unique = list(clients.values())
        users = []
        for ele in users_name_unique:
            id = model_methods.user_id_by_tuple(ele)
            username = model_methods.getting_username_by_id(id)
            users.append(username)
        users = self.users_to_str_list(users)
        self.bytes_and_send(client, "< Users List > ------------------------------------------------------------------------------------------------------------")
        time.sleep(0.01)
        self.data_display(client, users, 'User')
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
            result.append(user)
        return result

    @staticmethod
    def messages_to_str_list(messages):
        result = []
        for unit in messages:
            print("unit: ", unit)
            message = unit[1]
            sender_id = unit[2]
            sender = model_methods.getting_username_by_id(sender_id)
            receiver_result = ""
            created_at = unit[len(unit)-1]
            count = 0

            for ele in unit:
                if count == 3:
                    users_list = ele.split(', ')
                    del_index = users_list.index(str(sender_id))
                    del users_list[del_index]
                    last_idx = len(users_list) - 1
                    index = 0
                    for receiver_id in users_list:
                        username = model_methods.getting_username_by_id(receiver_id)
                        if index != last_idx:
                            receiver_result = receiver_result + username + ', '
                            index = index + 1
                        else:
                            receiver_result = receiver_result + username
                    break
                count = count + 1

            if receiver_result == "":
                receiver_result = f"{sender} is ONLY User"
            unit_result = f"<message: {message} & sender: {sender} & receiver: {receiver_result} & created_at: {created_at}>"
            result.append(unit_result)
        return result

    def data_display(self, client, list_form, type):
        count = 1
        for one_str in list_form:
            self.bytes_and_send(client, f"{type} {count}: " + one_str)
            time.sleep(.01)
            count = count + 1

table = table()
host_or_not = input("Are you host? [host/client]: ")
if host_or_not == "host":
    table_checker = input("You already made the table? [yes/first]: ")
    if table_checker == 'yes':
        pass
    else:
        table.making_table()
    Server()

