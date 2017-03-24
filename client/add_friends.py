from page import *
import socket
from tkinter import messagebox


class AddFriends(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.username = username
        self.root = root

    def add_elements(self, root, title):
        super(AddFriends, self).add_elements(root, title)
        label1 = Label(root, font=self.font1, fg=FIREBRICK1, text=ADD_PAGE_TEXT)
        label1.pack()
        label1.place(x=50, y=60)
        global entry_username
        entry_username = Entry(root, bg=CHOCOLATE, fg=WHITE, bd=5, font=self.font1,
                               exportselection=0, insertbackground=GOLD, insertwidth=10, width=20)
        entry_username.pack()
        entry_username.place(x=250, y=200)
        button_username = Button(root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                                 font=self.font1, fg=WHITE, text=ADD_FRIENDS,
                                 command=self.add_friend)
        button_username.pack()
        button_username.place(x=650, y=200)
        self.show_requests()

    def add_friend(self):
        global entry_username
        username = entry_username.get()
        if self.username != username:
            if username:
                request = "addfriend#" + self.username + "#" + username
                sock = socket.socket()
                sock.connect((SERVER, PORT))
                sock.send(request.encode())
                answer = sock.recv(CHECK_BUFFER).decode()
                if answer == OK:
                    messagebox.showwarning("SUCCESS!", "Your friendship request was sent successfully")
                    self.clear_screen(self.root)
                    self.add_elements(self.root, ADD_FRIENDS)
                else:
                    messagebox.showwarning("ERROR!", "Your friendship request was not sent\n"
                                                     "1) this username is invalid\n"
                                                     "2) You already sent friendship request for this username")
        else:
            messagebox.showwarning("ERROR!", "Your cannot friendship yourself!")

    def show_requests(self):
        sock = socket.socket()
        sock.connect((SERVER, PORT))
        request = "getrequests#" + self.username
        sock.send(request.encode())
        answer = sock.recv(CHAT_BUFFER).decode()
        if answer and answer != OK:
            xplace = 380
            yplace = 280
            requests = answer.split("\n")
            for raw in requests:
                label = Label(self.root, font=self.font1, text=raw)
                label.pack()
                label.place(x=xplace, y=yplace)
                yplace += 70
        sock.close()
