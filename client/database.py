import sqlite3


class DataBase(object):
    def __init__(self, path):
        object.__init__(self)
        self.database = sqlite3.connect(path)

    def create_chat_database(self):
        self.database.execute('''create table chat(too text not null,
                              frm text not null, message text not null);''')

    def drop_chat_database(self):
        self.database.execute("drop table if exists chat")

    def add_message(self, to, frm, message):
        self.database.execute("insert into chat (too, frm, message) "
                              "values ('%s', '%s', '%s')" % (to, frm, message))
        self.database.commit()

    def get_message(self):
        cursor = self.database.execute("select frm, message from chat")
        messages_list = []
        for row in cursor:
            messages_list.append((row[0], row[1]))
        return messages_list

    def close_database(self):
        self.database.close()
