import smtplib
from constants import *


class SMTP(object):
    def __init__(self):
        object.__init__(self)
        self.user = MY_EMAIL
        self.password = MY_PASSWORD
        self.to = self.user

    def send_email(self, frm, text, username=None):
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