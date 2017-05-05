"""
Author          :   Or Israeli
FileName        :   database.py
Date            :   5.5.17
Version         :   1.0
"""

import sqlite3
from constants import *
import os


class DataBase(object):
    def __init__(self, path):
        object.__init__(self)
        self.database = sqlite3.connect(path)

    def create_database(self):
        """

        The function creates a new users database table.

        """
        self.database.execute('''create table user(username text primary key
                              not null, password text unique not null, email
                              text unique not
                              null, online int not null);''')

    def drop_database(self):
        """

        The function deletes the users database table.

        """
        self.database.execute("drop table if exists user")

    def create_friends_database(self):
        """

        The function creates a new friends database table.

        """
        self.database.execute('''create table friends(user text primary key
        not null);''')

    def drop_friends_database(self):
        """

        The function deletes the friends database table.

        """
        self.database.execute("drop table if exists friends")

    def create_requests_database(self):
        """

        The function creates a new requests database table.

        """
        self.database.execute('''create table requests(user text primary key
        not null);''')

    def drop_requests_database(self):
        """

        The function deletes the requests database table.

        """
        self.database.execute("drop table if exists requests")

    def create_chat_database(self):
        """

        The function creates a new chat database table.

        """
        self.database.execute('''create table chat(too text not null,
                              frm text not null, message text not null);''')

    def drop_chat_database(self):
        """

        The function deletes the chat database table.

        """
        self.database.execute("drop table if exists chat")

    def add_message(self, to, frm, message):
        """

        The function adds a new message to the chat table.

        Args:
            to (string): The addressee of the message.
            frm (string): The sender of the message.
            message (string): The body of the message.

        """
        self.database.execute("insert into chat (too, frm, message) "
                              "values ('%s', '%s', '%s')" % (to, frm,
                                                             message))
        self.database.commit()

    def get_message(self, to):
        """

        The function finds all the messages that were sent to the user,
        returns them and deletes them from the chat database.

        Args:
            to (string): The username of the user.

        Returns:
            list: The list of the messages that were sent to the user.

        """
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
        """

        The function returns all the friendship requests that were sent
        to the user.

        Returns:
            list: The list of the friendship requests.

        """
        cursor = self.database.execute("select user from requests")
        requests = []
        for raw in cursor:
            requests.append(raw[0])
        return requests

    def get_friends(self):
        """

        The function returns all the friends of the user.

        Returns:
            list: The list of the friends.

        """
        cursor = self.database.execute("select user from friends")
        friends = []
        for raw in cursor:
            friends.append(raw[0])
        return friends

    def delete_request(self, user):
        """

        The function deletes a friendship request that was sent
        to the user by another user.

        Args:
            user (string): The user that sent the friendship request.

        Returns:
            bool: If the request was deleted or not.
        """
        requests_list = self.get_requests()
        if user in requests_list:
            self.database.execute("delete from requests where user = '%s'"
                                  % user)
            self.database.commit()
            return True
        else:
            return False

    def add_friend(self, user):
        """

        The function adds a new friend to the user's database.

        Args:
            user (string): The user that join to the friends list.

        """
        self.database.execute("insert into friends (user) values ('%s')"
                              % user)
        self.database.commit()

    def add_request(self, user):
        """

        The function adds a new request to the user's database.

        Args:
            user (string): The user that sent the friendship request.

        Returns:
            bool: If the request was added or not.

        """
        try:
            self.database.execute("insert into requests (user) values ('%s')"
                                  % user)
            self.database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_user(self, credentials):
        """

        The function adds a new user to the social network.
        It gets his credentials and registers him.

        Args:
            credentials (list): List of the 3 credentials
            (username, password and email address).

        Returns:
            bool: If the registration was successfully or not.

        """
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
        """

        The function turns the user's status from online to offline
        or from offline to online.

        Args:
            username (string): The user that want to change his status.
            value (int): Online or Offline (1 or 0).

        """
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
        """

        The function checks if the user's credentials are correct when
        he wants to log in.

        Args:
            credentials (list): List of the 2 credentials
            (username and password).

        Returns:
            bool: If the user's credentials are correct or not.

        """
        username = credentials[0]
        password = credentials[1]
        cursor = self.database.execute("select username, password from user")
        for raw in cursor:
            if raw[0] == username and not self.check_online(username):
                if raw[1] == password:
                    self.update_user(username, 1)
                    return True
        else:
            return False

    def get_users(self):
        """

        The function returns all the users that exists in the
        server's database.

        Returns:
            list: The list of all the user names.

        """
        cursor = self.database.execute("select username from user")
        usernames_list = []
        for raw in cursor:
            usernames_list.append(raw[0])
        return usernames_list

    def delete_user(self, username):
        """

        The function deletes a user from the social network.

        Args:
            username (string): The username of the user.

        """
        self.database.execute("delete from user where username = %s" %
                              username)
        self.database.commit()

    def check_online(self, username):
        """

        The function checks if the user is online or offline.

        Args:
            username (string): The username of the user.

        Returns:
            int: If the user is online or offline (1 or 0).

        """
        cursor = self.database.execute("select username, online from user")
        for raw in cursor:
            if raw[0] == username:
                return raw[1]

    def change_email(self, username, email):
        """

        The function changes the email address of the user.

        Args:
            username (string): The username of the user that want to change
                               his email address.
            email (string): The new email address.

        Returns:
            bool: If the email address was change or not.

        """
        try:
            self.database.execute("update user set email = '%s' "
                                  "where username = '%s'" % (email, username))
            self.database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def change_password(self, username, password):
        """

        The function changes the password of the user.

        Args:
            username (string): The username of the user that want to change
                               his password.
            password (string): The new password.

        Returns:
            bool: If the password was change or not.

        """
        try:
            self.database.execute("update user set password = '%s' "
                                  "where username = '%s'" % (password,
                                                             username))
            self.database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_email(self, username):
        """

        The function returns the email address of the received user.

        Args:
            username (string): The username to get his email address.

        Returns:
            string: The email address of the user.

        """
        cursor = self.database.execute("select username, email from user")
        for raw in cursor:
            if raw[0] == username:
                return raw[1]

    def get_password(self, username, email):
        """

        The function returns the password of the received user.

        Args:
            username (string): The username to get his password.
            email (string): The email address of the user.

        Returns:
            string: The password of the user.

        """
        cursor = self.database.execute("select username, email, password "
                                       "from user")
        for raw in cursor:
            if raw[0] == username and raw[1] == email:
                return raw[2]
        return False

    def close_database(self):
        """

        The function closes the database.

        """
        self.database.close()
