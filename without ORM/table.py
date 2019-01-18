import sqlite3


class Table:
        def __init__(self):
                self.conn = sqlite3.connect("tcp_chat.db")
                # self.conn = sqlite3.connect(":memory:")
                self.c    = self.conn.cursor()

        def making_table(self):
                self.c.execute("""CREATE TABLE user (
                                id   INTEGER  PRIMARY KEY,
                                username TEXT,
                                unique_number INTEGER,
                                chatRoomNumber_id INTEGER NOT NULL,
                                FOREIGN KEY (chatRoomNumber_id) REFERENCES chatRoomNumber(id)
                                )""")

                self.c.execute("""CREATE TABLE msg (
                                id                 INTEGER PRIMARY KEY,
                                message            TEXT,
                                sender_id          INTEGER NOT NULL,
                                receivers_id       TEXT,
                                chatRoomNumber_id  INTEGER,
                                created_at         TIMESTAMP,
                                FOREIGN KEY (sender_id) REFERENCES user(id)
                                )""")

                self.c.execute("""CREATE TABLE chatRoomNumber (
                                  id INTEGER PRIMARY KEY,
                                  room_number INTEGER
                                  )""")
                self.conn.commit()

#
#
# import sqlite3
#
#
# conn = sqlite3.connect("tcp_chat.db")
# c    = conn.cursor()
#
#
#
# c.execute("DROP TABLE user")
# c.execute("DROP TABLE msg")
# c.execute("DROP TABLE chatRoomNumber")
#
# conn.commit()