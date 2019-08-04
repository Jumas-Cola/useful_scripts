import sqlite3
import os


class ConnectDB:
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(self.curr_dir, 'log.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS log(
            ID INTEGER PRIMARY KEY,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );""")

    def check(self, id):
        sql = 'SELECT * FROM log WHERE id=?'
        self.cursor.execute(sql, [(id)])
        res = self.cursor.fetchall()
        return True if res else False

    def insert(self, id):
        self.cursor.execute('INSERT INTO log (id) VALUES (?)', (id,))
        self.conn.commit()
        return 0
