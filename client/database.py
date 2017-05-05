"""
Author          :   Or Israeli
FileName        :   database.py
Date            :   5.5.17
Version         :   1.0
"""

import sqlite3


class DataBase(object):
    def __init__(self, path):
        object.__init__(self)
        self.database = sqlite3.connect(path)

    def create_chat_database(self):
        """

        The function creates a new table of the chat database.

        """
        self.database.execute('''create table chat(too text not null,
                              frm text not null, message text not null);''')

    def drop_chat_database(self):
        """

        The function deletes the table of the chat database.

        """
        self.database.execute("drop table if exists chat")

    def add_message(self, to, frm, message):
        """

        The function adds new message to the user's chat database.

        Args:
            to (string): The name of the addressee of the message.
            frm (string): The name of the sender of the message.
            message (string): The message that was sent.

        """
        self.database.execute("insert into chat (too, frm, message) "
                              "values ('%s', '%s', '%s')" % (to, frm,
                                                             message))
        self.database.commit()

    def get_message(self):
        """

        The function returns all the messages and their senders
        from a user's chat database.

        Returns:
            list: The list of all the senders and messages.

        """
        cursor = self.database.execute("select frm, message, too from chat")
        messages_list = []
        for row in cursor:
            messages_list.append((row[0], row[1], row[2]))
        return messages_list

    def new_senders(self):
        """

        The function returns all the users that have sent a message
        to the current account which he still hasn't read.

        Returns:
            list: The list of the new senders.

        """
        cursor = self.database.execute("select frm, message from chat")
        senders_list = []
        for row in cursor:
            if row[1] == "###new_message###":
                senders_list.append(row[0])
        return senders_list

    def delete_new_senders(self, user):
        """

        The function deletes a user from the list of the new senders when
        the current user just read his messages.

        Args:
            user (string): The friend that the user just read his messages.

        """
        try:
            self.database.execute("delete from chat where message = "
                                  "'###new_message###' "
                                  "and frm = '%s'" % user)
            self.database.commit()
        except sqlite3.IntegrityError:
            pass

    def close_database(self):
        """

        The function closes the database.

        """
        self.database.close()
