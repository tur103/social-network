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
                            exportselection=0, insertbackground=ROYAL_BLUE)
        entry_email.pack()
        button_email = Button(root, bg=RED, activebackground=RED,
                              font=self.font1, fg=WHITE, text=CHANGE_EMAIL,
                              command=self.change_email)
        button_email.pack()

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
            messagebox.showwarning("INVALID", "Invalid username, password or email")
        else:
            messagebox.showwarning("INVALID", "Invalid username, password or email")
