"""
Author          :   Or Israeli
FileName        :   smtp.py
Date            :   5.5.17
Version         :   1.0
"""

import smtplib
from constants import *


class SMTP(object):
    def __init__(self):
        object.__init__(self)
        self.user = MY_EMAIL
        self.password = MY_PASSWORD
        self.to = self.user

    def send_email(self, frm, text, username=None):
        """

        The function gets the sender, the destination and the message
        and sends to the developer the message from the user.

        Args:
            frm (string): The email address of the sender.
            text (string): The body of the message.
            username (string): The username of the sender.

        Returns:
            bool: If the mail was sent or not.

        """
        if not username:
            username = "Guest"
        subject = username + " --> " + frm
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (frm, ", ".join(self.to), subject, text)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(frm, self.to, message)
            server.close()
            return True
        except smtplib.SMTPException:
            return False

    def send_password(self, to, password):
        """

        The function gets a user that forgot his password and sends
        him an email with his restore password.

        Args:
            to (string): The email address of the user.
            password (string): The password of the user.

        Returns:
            bool: If the mail was sent or not.

        """
        subject = "social-network: restore password"
        text = PASSWORD_TEXT + password
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.user, ", ".join(to), subject, text)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.user, to, message)
            server.close()
            return True
        except smtplib.SMTPException:
            return False
