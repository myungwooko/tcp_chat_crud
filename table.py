import sqlite3


class Table:
        def __init__(self):
                self.conn = sqlite3.connect("tcp_chat")
                self.c    = self.conn.cursor()

        def making_table(self):
                self.c.execute("""CREATE TABLE user (
                                id   INTEGER  PRIMARY KEY,
                                name text
                                )""")

                self.c.execute("""CREATE TABLE msg (
                                id          INTEGER PRIMARY KEY,
                                msg         TEXT,
                                sender      TEXT,
                                receivers   TEXT,
                                created_at  date
                                )""")

        def drop_table(self):
                self.c.execute("DROP TABLE user")
                self.c.execute("DROP TABLE msg")
                self.conn.commit()




