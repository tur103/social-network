from page import *
import socket
import speech_recognition as sr
from tkinter import messagebox
from database import *
import os


class PrivateChat(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.root = root
        self.username = username

    def add_elements(self, root, title):
        super(PrivateChat, self).add_elements(root, title)
        label = Label(root, font=self.font1, fg=ROYAL_BLUE, text=PRIVATE_CHAT_TEXT)
        label.pack()
        label.place(x=35, y=100)
        self.add_friends_scrollbar()

    def add_friends_scrollbar(self):
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
            global lb
            lb = Listbox(self.root, bd=10, bg=PEACHPUFF2, font=self.font1,
                         fg=ORANGE_RED, height=length, selectbackground=CHOCOLATE,
                         selectmode="single", relief="sunken", width=20, yscrollcommand=scroll.set)
            i = 1
            for raw in friends:
                lb.insert(i, raw)
                i += 1
            lb.pack()
            lb.place(y=300, x=250)
            scroll.config(command=lb.yview)
            button_wall = Button(self.root, bg=GOLD, activebackground=GOLD,
                                 font=self.font1, fg=RED, text=OPEN_CHAT,
                                 command=self.open_chat)
            button_wall.pack()
            button_wall.place(x=650, y=220)
        sock.close()

    def open_chat(self):
        global lb
        index = lb.curselection()
        if index:
            selected_user = lb.get(index)
            self.clear_screen(self.root)
            super(PrivateChat, self).add_elements(self.root, selected_user)
            scroll = Scrollbar()
            scroll.pack(side="right", fill="y")
            chat_box = Text(self.root, bg=PEACHPUFF2, bd=5, font=self.font4,
                            fg=BLACK, exportselection=0, height=26,
                            insertbackground=CYAN3, insertwidth=3, insertofftime=0,
                            selectbackground=GOLD, width=65,
                            wrap="word", yscrollcommand=scroll.set)
            chat_box.pack()
            chat_box.place(x=100, y=80)
            scroll.config(command=chat_box.yview)
            global message_entry
            message_entry = Entry(self.root, bg=CHOCOLATE, fg=WHITE, bd=5, font=self.font1,
                                  exportselection=0, insertbackground=GOLD, insertwidth=10, width=35)
            message_entry.pack()
            message_entry.place(x=180, y=720)
            button_record = Button(self.root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                                   font=self.font1, fg=WHITE, text=RECORD,
                                   command=self.record_message)
            button_record.pack()
            button_record.place(x=20, y=713)
            button_send = Button(self.root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                                 font=self.font1, fg=WHITE, text=SEND,
                                 command=self.send_message)
            button_send.pack()
            button_send.place(x=750, y=713)
            chat_database = DataBase(os.path.dirname(os.path.realpath(__file__)) + "/facebook/chat.db")
            message_list = chat_database.get_message()
            for message in message_list:
                if message[0] == self.username or message[0] == selected_user:
                    if message[0] == self.username:
                        sender = "me:  "
                    else:
                        sender = selected_user + ":  "
                    chat_box.insert(END, sender + message[1])
            chat_box.see(END)


    def record_message(self):
        global message_entry
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            message_entry.delete(0, END)
            message_entry.insert(0, r.recognize_google(audio))
        except sr.UnknownValueError:
            messagebox.showwarning("Failed", "sorry, what were you saying?\nI didn't realize it. try again")
        except sr.RequestError as e:
            messagebox.showwarning("Failed", "Could not get results from Speech Recognition service; {0}".format(e))

    def send_message(self):
        global message_entry

