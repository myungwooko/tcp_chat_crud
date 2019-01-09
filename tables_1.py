# import sqlite3
# import time
# import datetime
# ts = time.time()
# st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
# print(st)
#
# # conn = sqlite3.connect('tcp_chat.db')
# conn = sqlite3.connect(':memory:')
# c    = conn.cursor()

def making_table(c):

        c.execute("DROP TABLE user")
        c.execute("DROP TABLE msg")

        c.execute("""CREATE TABLE user (
                  id   INTEGER  PRIMARY KEY,
                  name text
                  )""")

        c.execute("""CREATE TABLE msg (
                  id          INTEGER PRIMARY KEY,
                  msg         TEXT,
                  sender      TEXT,
                  receivers   TEXT,
                  created_at  date
                  )""")
        return





