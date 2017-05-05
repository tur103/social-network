"""
Author          :   Or Israeli
FileName        :   private_chat.py
Date            :   5.5.17
Version         :   1.0
"""

from page import *
import socket
import speech_recognition as sr
from tkinter import messagebox
from database import *
import os


class PrivateChat(Page):

    in_chat_with = False
    in_unread = False

    def __init__(self, root, username):
        Page.__init__(self, root)
        self.root = root
        self.username = username
        self.selected_user = None

    def add_elements(self, root, title):
        """

        The function displays the private chat page.
        The user can see his friends list and choose one to start
        chatting with. The user can also see who sent him a new
        message.

        Args:
            root (Tk): The Tk window.
            title (string): The name of the page.

        """
        super(PrivateChat, self).add_elements(root, title)
        label = Label(root, font=self.font1, fg=ROYAL_BLUE,
                      text=PRIVATE_CHAT_TEXT)
        label.pack()
        label.place(x=35, y=100)
        self.add_friends_scrollbar()

    def add_friends_scrollbar(self):
        """

        The function presents the friends list of the user.
        It allows him to choose one friend and get into the chat hall
        with him. It also shows him who has sent him a new message.

        """
        sock = socket.socket()
        sock.connect((SERVER, PORT))
        request = "getfriends#" + self.username
        sock.send(request.encode())
        answer = sock.recv(FRIENDS_BUFFER).decode()
        if answer != NON:
            friends = answer.split(",")
            scroll = Scrollbar()
            scroll.pack(side="right", fill="y")
            length = len(friends)
            if length > 12:
                length = 12
            PrivateChat.in_unread = True
            global lb
            lb = Listbox(self.root, bd=10, bg=PEACHPUFF2, font=self.font1,
                         fg=ORANGE_RED, height=length,
                         selectbackground=CHOCOLATE, selectmode="single",
                         relief="sunken", width=25, yscrollcommand=scroll.set)
            i = 1
            chat_database = DataBase(
                os.path.dirname(os.path.realpath(__file__)) + "/facebook/" +
                self.username + "/chat.db")
            new_senders = chat_database.new_senders()
            chat_database.close_database()
            for raw in friends:
                new_message = ""
                if raw in new_senders:
                    new_message = "  $unread$"
                lb.insert(i, raw + new_message)
                i += 1
            lb.pack()
            lb.place(y=300, x=230)
            scroll.config(command=lb.yview)
            button_wall = Button(self.root, bg=GOLD, activebackground=GOLD,
                                 font=self.font1, fg=RED, text=OPEN_CHAT,
                                 command=self.open_chat)
            button_wall.pack()
            button_wall.place(x=650, y=220)
        sock.close()

    def open_chat(self):
        """

        The function displays the chat hall with the selected friend.
        In this page the user can see all the history chat with the friend,
        he can send a new message and record a new message for his comfort.

        """
        global lb
        index = lb.curselection()
        if index:
            PrivateChat.in_unread = False
            self.selected_user = lb.get(index)
            self.selected_user = self.selected_user.replace("  $unread$", "")
            PrivateChat.in_chat_with = self.selected_user
            self.clear_screen(self.root)
            super(PrivateChat, self).add_elements(self.root,
                                                  self.selected_user)
            scroll = Scrollbar()
            scroll.pack(side="right", fill="y")
            global chat_box
            chat_box = Text(self.root, bg=PEACHPUFF2, bd=5, font=self.font4,
                            fg=BLACK, exportselection=0, height=26,
                            insertbackground=CYAN3, insertwidth=3,
                            insertofftime=0,
                            selectbackground=GOLD, width=65,
                            wrap="word", yscrollcommand=scroll.set)
            chat_box.pack()
            chat_box.place(x=100, y=80)
            scroll.config(command=chat_box.yview)
            global message_entry
            message_entry = Entry(self.root, bg=CHOCOLATE, fg=WHITE, bd=5,
                                  font=self.font1, exportselection=0,
                                  insertbackground=GOLD, insertwidth=10,
                                  width=35)
            message_entry.pack()
            message_entry.place(x=180, y=720)
            button_record = Button(self.root, bg=ROYAL_BLUE,
                                   activebackground=ROYAL_BLUE,
                                   font=self.font1, fg=WHITE, text=RECORD,
                                   command=self.record_message)
            button_record.pack()
            button_record.place(x=20, y=713)
            button_send = Button(self.root, bg=ROYAL_BLUE,
                                 activebackground=ROYAL_BLUE,
                                 font=self.font1, fg=WHITE, text=SEND,
                                 command=self.send_message)
            button_send.pack()
            button_send.place(x=750, y=713)
            chat_database = DataBase(
                os.path.dirname(os.path.realpath(__file__)) + "/facebook/" +
                self.username + "/chat.db")
            message_list = chat_database.get_message()
            for message in message_list:
                if message[1] != "###new_message###" and \
                        ((message[0] == self.username and message[2] ==
                            self.selected_user) or message[0] ==
                            self.selected_user):
                    if message[0] == self.username:
                        sender = "me:  "
                    else:
                        sender = self.selected_user + ":  "
                    chat_box.insert(END, sender + message[1] + "\n")
            chat_box.see(END)
            chat_database.delete_new_senders(self.selected_user)
            chat_database.close_database()

    def record_message(self):
        """

        The function executes when the user press the record button.
        It records the user's words and writes them down as a status.

        """
        try:
            global message_entry
            # Record Audio
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            # Speech recognition using Google Speech Recognition
            try:
                message_entry.delete(0, END)
                message_entry.insert(0, r.recognize_google(audio))
            except sr.UnknownValueError:
                messagebox.showwarning("Failed", "sorry, what were you "
                                                 "saying?\nI didn't realize "
                                                 "it. try again")
            except sr.RequestError as e:
                messagebox.showwarning("Failed", "Could not get results from "
                                                 "Speech Recognition service;"
                                                 " {0}".format(e))
        except OSError:
            messagebox.showwarning("ERROR", "No Default Input Device "
                                            "Available")

    def send_message(self):
        """

        The function executes when the user sends a new message.
        It sends to the server his new message and displays it in the
        chat hall.

        """
        global message_entry
        message = message_entry.get()
        if message:
            request = "sendmessage#" + self.selected_user + "#" + \
                      self.username + "#" + message
            sock = socket.socket()
            sock.connect((SERVER, PORT))
            sock.send(request.encode())
            answer = sock.recv(CHECK_BUFFER).decode()
            if answer != OK:
                messagebox.showwarning("Failed", "Your message wasn't "
                                                 "sent.\nTry again later.")
            else:
                chat_database = DataBase(
                    os.path.dirname(os.path.realpath(__file__)) +
                    "/facebook/" + self.username + "/chat.db")
                chat_database.add_message(self.selected_user,
                                          self.username, message)
                chat_database.close_database()
                global chat_box
                sender = "me:  "
                chat_box.insert(END, sender + message + "\n")
                message_entry.delete(0, END)
                chat_box.see(END)

    @staticmethod
    def received_message(frm, message):
        """

        The function receives a new message that was accepted from the server
        and presents it in the chat hall.

        Args:
            frm (string): The sender of the new message.
            message (string): The message that was sent to the user.

        """
        sender = frm + ": "
        chat_box.insert(END, sender + message + "\n")
        chat_box.see(END)

    @staticmethod
    def add_unread(username):
        """

        The function updates the friends list.
        If a friend sent to the user a new message, the function
        will mark this friend's chat as unread.

        Args:
            username (string): The name of the friend that sent the new
            message.

        """
        for item in range(lb.size()):
            if lb.get(item) == username:
                lb.delete(item)
                lb.insert(item, username + "  $unread$")
                break
