import smtplib
from constants import *


class SMTP(object):
    def __init__(self):
        object.__init__(self)
        self.user = MY_EMAIL
        self.password = MY_PASSWORD
        self.frm = self.user

    def send_email(self, to, text, username=None):
        if not username:
            username = "Guest"
        subject = username
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.frm, ", ".join(to), subject, text)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.frm, to, message)
            server.close()
            return True
        except smtplib.SMTPException:
            return False
