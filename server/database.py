import sqlite3
from constants import *
import os


class DataBase(object):
    def __init__(self, path):
        object.__init__(self)
        self.database = sqlite3.connect(path)

    def create_database(self):
        self.database.execute('''create table user(username text primary key
                              not null, password text not null, email text not
                              null, online int not null);''')

    def drop_database(self):
        self.database.execute("drop table if exists user")

    def create_friends_database(self):
        self.database.execute('''create table friends(user text primary key not null);''')

    def drop_friends_database(self):
        self.database.execute("drop table if exists friends")

    def create_requests_database(self):
        self.database.execute('''create table requests(user text primary key not null);''')

    def drop_requests_database(self):
        self.database.execute("drop table if exists requests")

    def create_chat_database(self):
        self.database.execute('''create table chat(too text not null,
                              frm text not null, message text not null);''')

    def drop_chat_database(self):
        self.database.execute("drop table if exists chat")

    def add_message(self, to, frm, message):
        self.database.execute("insert into chat (too, frm, message) "
                              "values ('%s', '%s', '%s')" % (to, frm, message))
        self.database.commit()

    def get_message(self, to):
        cursor = self.database.execute("select too, frm, message from chat")
        messages_list = []
        for row in cursor:
            if row[0] == to:
                messages_list.append((row[0], row[1], row[2]))
        try:
            self.database.execute("delete from chat where too = '%s'" % to)
            self.database.commit()
        except sqlite3.IntegrityError:
            pass
        return messages_list

    def get_requests(self):
        cursor = self.database.execute("select user from requests")
        requests = []
        for raw in cursor:
            requests.append(raw[0])
        return requests

    def get_friends(self):
        cursor = self.database.execute("select user from friends")
        friends = []
        for raw in cursor:
            friends.append(raw[0])
        return friends

    def delete_request(self, user):
        requests_list = self.get_requests()
        if user in requests_list:
            self.database.execute("delete from requests where user = '%s'" % user)
            self.database.commit()
            return True
        else:
            return False

    def add_friend(self, user):
        self.database.execute("insert into friends (user) values ('%s')" % user)
        self.database.commit()

    def add_request(self, user):
        self.database.execute("insert into requests (user) values ('%s')" % user)
        self.database.commit()

    def add_user(self, credentials):
        username = credentials[0]
        password = credentials[1]
        email = credentials[2]
        if not username or not password or not email:
            return False
        try:
            self.database.execute("insert into user (username, password, "
                                  "email, online) values ('%s', '%s', '%s', "
                                  "1)" % (username, password, email))
            self.database.commit()
            os.mkdir(DIRECTORY + username)
            return True
        except sqlite3.IntegrityError:
            return False

    def update_user(self, username, value):
        if value == CHANGE:
            onof = self.check_online(username)
            if onof == 1:
                value = 0
            if onof == 0:
                value = 1
        else:
            value = int(value)
        self.database.execute("update user set online = %s where "
                              "username='%s'" % (value, username))
        self.database.commit()

    def check_user(self, credentials):
        username = credentials[0]
        password = credentials[1]
        cursor = self.database.execute("select username, password from user")
        for raw in cursor:
            if raw[0] == username:
                if raw[1] == password:
                    self.update_user(username, 1)
                    return True
        else:
            return False

    def get_users(self):
        cursor = self.database.execute("select username from user")
        usernames_list = []
        for raw in cursor:
            usernames_list.append(raw[0])
        return usernames_list

    def delete_user(self, username):
        self.database.execute("delete from user where username = %s" %
                              username)
        self.database.commit()

    def check_online(self, username):
        cursor = self.database.execute("select username, online from user")
        for raw in cursor:
            if raw[0] == username:
                return raw[1]

    def change_email(self, username, email):
        try:
            self.database.execute("update user set email = '%s' "
                                  "where username = '%s'" % (email, username))
            self.database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def change_password(self, username, password):
        try:
            self.database.execute("update user set password = '%s' "
                                  "where username = '%s'" % (password, username))
            self.database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_email(self, username):
        cursor = self.database.execute("select username, email from user")
        for raw in cursor:
            if raw[0] == username:
                return raw[1]

    def get_password(self, username, email):
        cursor = self.database.execute("select username, email, password from user")
        for raw in cursor:
            if raw[0] == username and raw[1] == email:
                return raw[2]
        return False

    def close_database(self):
        self.database.close()
