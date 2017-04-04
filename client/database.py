import sqlite3


class DataBase(object):
    def __init__(self, path):
        object.__init__(self)
        self.database = sqlite3.connect(path)

    def create_chat_database(self):
        self.database.execute('''create table chat(too text primary key not null,
                              frm text not null, message text not null);''')

    def drop_chat_database(self):
        self.database.execute("drop table if exists chat")

    def add_message(self, to, frm, message):
        self.database.execute("insert into chat (too, frm, message) "
                              "values ('%s', '%s', '%s')" % (to, frm, message))
        self.database.commit()

    def close_database(self):
        self.database.close()
