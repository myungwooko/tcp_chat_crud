import sqlite3

# tried to use singleton -> but when I used this, met error like this => (sqlite, not same object error)
# class Datalayer():
#     _cur = None     #Cursor which would be used by all methods
#     def __new__(cls, *args, **kwargs):
#         if not cls._cur:
#             conn=sqlite3.connect("tcp_chat")
#             cls._cur = conn
#         return cls._cur

def add_user(name):
    with sqlite3.connect("tcp_chat") as conn:
        c = conn.cursor()
    # conn = Datalayer()
    # c = conn.cursor()
        c.execute("INSERT INTO user(name) VALUES(:name)", {'name': name})
        conn.commit()

def insert_msg(msg, name, clients, st):
    with sqlite3.connect("tcp_chat") as conn:
        c = conn.cursor()
    # conn = Datalayer()
    # c = conn.cursor()
        msg = msg.decode("utf8")
        receivers = ""
        pre_receivers = clients.values()
        last_idx = len(pre_receivers) - 1
        counter = 0
        for receiver in pre_receivers:
            if counter != last_idx:
                receivers = receivers + receiver + ", "
                counter = counter + 1
            else:
                receivers = receivers + receiver

        c.execute("""INSERT INTO msg(msg, sender, receivers, created_at) 
                     VALUES(:msg, :sender, :receivers, :created_at)""",
                     {'msg': msg, 'sender': name, 'receivers': receivers, 'created_at': st})
        conn.commit()


def all_users():
    with sqlite3.connect("tcp_chat") as conn:
        c = conn.cursor()
    # conn = Datalayer()
    # c = conn.cursor()
        c.execute("SELECT * FROM user")
        users = c.execute("SELECT * FROM user")
        return c.fetchall()



def delete_user(name):
    with sqlite3.connect("tcp_chat") as conn:
        c = conn.cursor()
    # conn = Datalayer()
    # c = conn.cursor()
        c.execute(f"DELETE FROM user where name = '{name}'")
        conn.commit()

def all_messages():
    with sqlite3.connect("tcp_chat") as conn:
        c = conn.cursor()
    # conn = Datalayer()
    # c = conn.cursor()
        c.execute("SELECT * FROM msg")
        return c.fetchall()




