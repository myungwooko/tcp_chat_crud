import sqlite3


def add_user(username, unique_number, chat_room_number_id):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute("""INSERT INTO user(username, unique_number, chatRoomNumber_id) 
                     VALUES(:username, :unique_number, :chatRoomNumber_id)""",
                  {'username': username, 'unique_number': unique_number, 'chatRoomNumber_id': chat_room_number_id})
        conn.commit()


def insert_msg(msg, sender, clients, chatRoomNumber_id, st):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        msg = msg.decode("utf8")
        sender_id = user_id_by_tuple(sender)
        receivers_ids = ""
        pre_receivers = clients.values()
        last_idx = len(pre_receivers) - 1
        counter = 0
        for receiver in pre_receivers:
            receiver_id = user_id_by_tuple(receiver)
            if counter != last_idx:
                receivers_ids = receivers_ids + str(receiver_id) + ", "
                counter = counter + 1
            else:
                receivers_ids = receivers_ids + str(receiver_id)

        c.execute("""INSERT INTO msg(message, sender_id, receivers_id, chatRoomNumber_id, created_at) 
                     VALUES(:message, :sender_id, :receivers_id, :chatRoomNumber_id, :created_at)""",
                     {'message': msg, 'sender_id': sender_id, 'receivers_id': receivers_ids,
                      'chatRoomNumber_id': chatRoomNumber_id, 'created_at': st})
        conn.commit()

def add_new_chatroom_id(unique_number):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO chatRoomNumber(room_number) VALUES(:room_number)", {'room_number': unique_number})
        conn.commit()

def getting_chatroom_id():
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM chatRoomNumber where id = (SELECT MAX(id) from chatRoomNumber)")
        return c.fetchone()[0]

def user_id_by_tuple(tuple):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute(f"SELECT id FROM user WHERE username = '{tuple[0]}' AND unique_number = '{tuple[1]}' ")
        return c.fetchone()[0]

def getting_username_by_id(str_or_int):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        id = int(str_or_int)
        c.execute(f"SELECT username FROM user WHERE id='{id}'")
        result = c.fetchone()
        result = result[0]
        return result
        # return c.fetchone()[0]


def all_users(chatRoomNumber_id):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute(f"SELECT username FROM user WHERE chatRoomNumber_id = {chatRoomNumber_id}")
        return c.fetchall()


def delete_user(name):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM user where username = '{name}'")
        conn.commit()

def all_messages(chatRoomNumber_id):
    with sqlite3.connect("tcp_chat.db") as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM msg WHERE chatRoomNumber_id = '{chatRoomNumber_id}'")
        return c.fetchall()




