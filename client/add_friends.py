"""
Author          :   Or Israeli
FileName        :   add_friends.py
Date            :   5.5.17
Version         :   1.0
"""

from page import *
import socket
from tkinter import messagebox


class AddFriends(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.username = username
        self.root = root

    def add_elements(self, root, title):
        """

        The function displays the page of the adding new friends.
        It presents the description of the page, a place to write
        the username of the friends and buttons for accept and decline
        the user's receiving friendship requests.

        Args:
            root (Tk): The tk window.
            title (string): The name of the page.

        """
        super(AddFriends, self).add_elements(root, title)
        label1 = Label(root, font=self.font1, fg=FIREBRICK1,
                       text=ADD_PAGE_TEXT)
        label1.pack()
        label1.place(x=20, y=60)
        global entry_username
        entry_username = Entry(root, bg=CHOCOLATE, fg=WHITE, bd=5,
                               font=self.font1, exportselection=0,
                               insertbackground=GOLD, insertwidth=10,
                               width=20)
        entry_username.pack()
        entry_username.place(x=250, y=250)
        button_username = Button(root, bg=ROYAL_BLUE,
                                 activebackground=ROYAL_BLUE,
                                 font=self.font1, fg=WHITE, text=ADD_FRIENDS,
                                 command=self.add_friend)
        button_username.pack()
        button_username.place(x=650, y=250)
        button_accept = Button(root, bg=ROYAL_BLUE,
                               activebackground=ROYAL_BLUE,
                               font=self.font1, fg=WHITE, text=ACCEPT,
                               command=self.accept_friend)
        button_accept.pack()
        button_accept.place(x=50, y=600)
        button_decline = Button(root, bg=ROYAL_BLUE,
                                activebackground=ROYAL_BLUE,
                                font=self.font1, fg=WHITE, text=DECLINE,
                                command=self.decline_friend)
        button_decline.pack()
        button_decline.place(x=650, y=600)
        self.show_requests()

    def accept_friend(self):
        """

        The function executes when the user press the accept button.
        It gets the marked username that the user chose and send to the
        server a request to accept his friendship request.

        """
        try:
            index = lb.curselection()
            if index:
                user = lb.get(index)
                request = "addfriend#" + self.username + "#" + user
                sock = socket.socket()
                sock.connect((SERVER, PORT))
                sock.send(request.encode())
                answer = sock.recv(CHECK_BUFFER).decode()
                if answer == OK:
                        messagebox.showwarning("SUCCESS!", "Congratulations "
                                                           "for the new "
                                                           "friendship!")
                        self.clear_screen(self.root)
                        self.add_elements(self.root, ADD_FRIENDS)
                else:
                    messagebox.showwarning("ERROR!", "Your accept wasn't "
                                                     "sent. Try again later.")
        except NameError:
            pass

    def decline_friend(self):
        """

        The function executes when the user press the decline button.
        It gets the marked username that the user chose and send to the
        server a request to decline his friendship request.

        """
        try:
            index = lb.curselection()
            if index:
                user = lb.get(index) + "-not"
                request = "addfriend#" + self.username + "#" + user
                sock = socket.socket()
                sock.connect((SERVER, PORT))
                sock.send(request.encode())
                answer = sock.recv(CHECK_BUFFER).decode()
                if answer == OK:
                        messagebox.showwarning("SUCCESS!", "Your decline was "
                                                           "sent "
                                                           "successfully")
                        self.clear_screen(self.root)
                        self.add_elements(self.root, ADD_FRIENDS)
                else:
                    messagebox.showwarning("ERROR!", "Your decline wasn't "
                                                     "sent. Try again later.")
        except NameError:
            pass

    def add_friend(self):
        """

        The function executes when the user press the add friends button.
        It gets the username that the user typed in the box line and send
        to the server a request friendship for this user.

        """
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
                    messagebox.showwarning("SUCCESS!", "Your friendship "
                                                       "request was sent "
                                                       "successfully")
                    self.clear_screen(self.root)
                    self.add_elements(self.root, ADD_FRIENDS)
                else:
                    messagebox.showwarning("ERROR!", "Your friendship "
                                                     "request was not sent\n"
                                                     "1) this username is "
                                                     "invalid\n"
                                                     "2) You already sent "
                                                     "friendship request for "
                                                     "this username")
        else:
            messagebox.showwarning("ERROR!", "Your cannot "
                                             "friendship yourself!")

    def show_requests(self):
        """

        The function asks from the server the list of all the friendship
        request that were sent to the user.
        It displays the list in the page so the user could see all of them.

        """
        sock = socket.socket()
        sock.connect((SERVER, PORT))
        request = "getrequests#" + self.username
        sock.send(request.encode())
        answer = sock.recv(FRIENDS_BUFFER).decode()
        if answer and answer != OK:
            requests = answer.split(",")
            scroll = Scrollbar()
            scroll.pack(side="right", fill="y")
            length = len(requests)
            if length > 12:
                length = 12
            global lb
            lb = Listbox(self.root, bd=10, bg=PEACHPUFF2, font=self.font1,
                         fg=ORANGE_RED, height=length, selectbackground=GREEN,
                         selectmode="single", relief="sunken", width=20,
                         yscrollcommand=scroll.set)
            i = 1
            for raw in requests:
                lb.insert(i, raw)
                i += 1
            lb.pack()
            lb.place(y=320, x=250)
            scroll.config(command=lb.yview)
        sock.close()
