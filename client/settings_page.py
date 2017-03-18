from page import *
import socket
from tkinter import messagebox


class SettingsPage(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.root = root
        self.username = username

    def add_elements(self, root, title):
        super(SettingsPage, self).add_elements(root, title)
        global entry_email
        label_email = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1,
                            text=CHANGE_EMAIL, pady=20)
        label_email.pack()
        entry_email = Entry(self.root, bg=GOLD, fg=ORANGE_RED, bd=5, font=self.font1,
                            exportselection=0, insertbackground=ROYAL_BLUE, insertwidth=10)
        entry_email.pack()
        self.insert_space()
        button_email = Button(root, bg=RED, activebackground=RED,
                              font=self.font1, fg=WHITE, text=CHANGE_EMAIL,
                              command=self.change_email)
        button_email.pack()
        global entry_password
        global entry_new_password
        label_password = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1,
                               text=CHANGE_PASSWORD, pady=20)
        label_password.pack()
        entry_password = Entry(self.root, bg=GOLD, fg=ORANGE_RED, bd=5, font=self.font1,
                               exportselection=0, insertbackground=ROYAL_BLUE, insertwidth=10, show="*")
        entry_password.pack()
        label_new_password = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1,
                                   text=CONFIRM_PASSWORD, pady=20)
        label_new_password.pack()
        entry_new_password = Entry(self.root, bg=GOLD, fg=ORANGE_RED, bd=5, font=self.font1,
                                   exportselection=0, insertbackground=ROYAL_BLUE, insertwidth=10, show="*")
        entry_new_password.pack()
        self.insert_space()
        button_password = Button(root, bg=RED, activebackground=RED,
                                 font=self.font1, fg=WHITE, text=CHANGE_PASSWORD,
                                 command=self.change_password)
        button_password.pack()

    def change_email(self):
        global entry_email
        request = "change#email#" + self.username + "#" + entry_email.get()
        my_socket = socket.socket()
        my_socket.connect((SERVER, PORT))
        my_socket.send(request.encode())
        answer = my_socket.recv(CHECK_BUFFER).decode()
        my_socket.close()
        if answer == OK:
            self.clear_screen(self.root)
            self.add_elements(self.root, SETTINGS_PAGE)
            messagebox.showwarning("Changed!", "Your email was changed successfully")
        else:
            messagebox.showwarning("Error", "Your email was not changed\n"
                                   "Try again later")

    def change_password(self):
        global entry_password
        global entry_new_password
        if entry_password.get() == entry_new_password.get():
            request = "change#password#" + self.username + "#" + entry_password.get()
            my_socket = socket.socket()
            my_socket.connect((SERVER, PORT))
            my_socket.send(request.encode())
            answer = my_socket.recv(CHECK_BUFFER).decode()
            my_socket.close()
            if answer == OK:
                self.clear_screen(self.root)
                self.add_elements(self.root, SETTINGS_PAGE)
                messagebox.showwarning("Changed!", "Your password was changed successfully")
            else:
                messagebox.showwarning("Error", "Your password was not changed\n"
                                       "Try again later")
        else:
            messagebox.showwarning("Invalid", "The two passwords are not identical")

    def insert_space(self):
        Label(self.root).pack()
