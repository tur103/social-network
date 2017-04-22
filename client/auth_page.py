from pages_menu import *
from tkinter import *
from tkinter import messagebox
import os
import ctypes


class AuthPage(Page):
    def __init__(self, root):
        Page.__init__(self, root)
        self.root = root
        self.socket = None
        self.username = ""

    def set_menu_button(self, root):
        """

        The function sets the menu button for switching between pages.

        Args:
            root (Tk): The Tk window.

        Returns:
            Menubutton: The menu button widget.

        """
        menubutton = super(AuthPage, self).set_menu_button(root)
        self.log_in_page()
        menubutton.menu.add_command(label=LOG_IN, command=self.log_in_page)
        menubutton.menu.add_command(label=REGISTER, command=self.register_page)
        menubutton.menu.add_command(label=FORGOT_PASSWORD, command=self.forgot_password_page)
        menubutton.menu.add_command(label=CONTACT_US, command=self.contact_us_page)
        return menubutton

    def log_in_page(self):
        """

        The function presents the log in page in the window.

        """
        self.clear_screen(self.root)
        self.add_elements(self.root, LOG_IN)
        text = Label(self.root, bd=0, font=self.font1, text=LOG_IN_TEXT, pady=100)
        text.pack()
        self.display_structure()
        l = Label(self.root, pady=20)
        l.pack()
        button = Button(self.root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                        font=self.font1, fg=WHITE, text=LOG_IN,
                        command=self.log_in_user)
        button.pack()

    def register_page(self):
        """

        The function presents the register page in the window.

        """
        self.clear_screen(self.root)
        self.add_elements(self.root, REGISTER)
        text = Label(self.root, bd=0, font=self.font1, text=REGISTER_TEXT, pady=40)
        text.pack()
        self.display_structure()
        global entry_email
        label_email = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1, text=EMAIL, pady=20)
        label_email.pack()
        entry_email = Entry(self.root,  bg=GREEN, bd=5, font=self.font1,
                            exportselection=0, fg=RED, insertbackground=CYAN, insertwidth=10)
        entry_email.pack()
        l = Label(self.root, pady=20)
        l.pack()
        button = Button(self.root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                        font=self.font1, fg=WHITE, text=REGISTER,
                        command=self.register_user)
        button.pack()

    def contact_us_page(self):
        """

        The function presents the page where the users can send
        email to the developer of the program. By that they could
        keep on contact and share their desires.

        """
        self.clear_screen(self.root)
        self.add_elements(self.root, CONTACT_US)
        text = Label(self.root, bd=0, font=self.font1, text=CONTACT_US_TEXT, pady=60)
        text.pack()
        label_address = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1, text=EMAIL)
        label_address.pack()
        global entry_address
        entry_address = Entry(self.root, bg=GREEN, bd=5, font=self.font1,
                              exportselection=0, fg=RED, insertbackground=CYAN, insertwidth=10)
        entry_address.pack()
        label_message = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1, text=MESSAGE, pady=20)
        label_message.pack()
        global entry_message
        entry_message = Text(self.root, bg=GREEN, bd=5, font=self.font1,
                             fg=RED, exportselection=0, height=6,
                             insertbackground=CYAN, insertwidth=10, selectbackground=MAGENTA, width=40,
                             wrap="word")
        entry_message.pack()
        l = Label(self.root, pady=5)
        l.pack()
        button = Button(self.root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                        font=self.font1, fg=WHITE, text=SEND_EMAIL,
                        command=self.email_user)
        button.pack()

    def forgot_password_page(self):
        """

        The function presents the page of the forgetting password.
        User who forgot his password can restore it by give
        his details. The password will arrive to his email.

        """
        self.clear_screen(self.root)
        self.add_elements(self.root, FORGOT_PASSWORD)
        text = Label(self.root, bd=0, font=self.font1, text=FORGOT_PASSWORD_TEXT, pady=100)
        text.pack()
        global entry_username
        global entry_email
        label_username = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1,
                               text=USERNAME, pady=20)
        label_username.pack()
        entry_username = Entry(self.root,  bg=GREEN, bd=5, font=self.font1,
                               exportselection=0, fg=RED, insertbackground=CYAN, insertwidth=10)
        entry_username.pack()
        label_email = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1, text=EMAIL, pady=20)
        label_email.pack()
        entry_email = Entry(self.root, bg=GREEN, bd=5, font=self.font1,
                            exportselection=0, fg=RED, insertbackground=CYAN, insertwidth=10)
        entry_email.pack()
        l = Label(self.root, pady=20)
        l.pack()
        button = Button(self.root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                        font=self.font1, fg=WHITE, text=FORGOT_PASSWORD,
                        command=self.forgot_password)
        button.pack()

    def display_structure(self):
        """

        The function displays the graphic widgets that help to create
        the pages of the program.

        """
        global entry_username
        global entry_password
        label_username = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1,
                               text=USERNAME, pady=20)
        label_username.pack()
        entry_username = Entry(self.root,  bg=GREEN, bd=5, font=self.font1,
                               exportselection=0, fg=RED, insertbackground=CYAN, insertwidth=10)
        entry_username.pack()
        label_password = Label(self.root, fg=CHOCOLATE, bd=0, font=self.font1, text=PASSWORD, pady=20)
        label_password.pack()
        entry_password = Entry(self.root, bg=GREEN, bd=5, font=self.font1,
                               exportselection=0, fg=RED, show="*", insertbackground=CYAN, insertwidth=10)
        entry_password.pack()

    def log_in_user(self):
        """

        The function executes when the user press the login button.
        It gets his credentials and sends a login request to the server.
        If it matches it will get him into his account but if not, well...
        try again :).

        """
        global entry_username
        global entry_password
        request = "database#login#" + entry_username.get() + "#" + entry_password.get()
        self.make_socket()
        self.socket.send(request.encode())
        answer = self.socket.recv(CHECK_BUFFER).decode()
        self.socket.close()
        if answer == OK:
            save_username(entry_username.get())
            self.enter(entry_username.get())
        else:
            messagebox.showwarning("INVALID", "Invalid username or password")

    def register_user(self):
        """

        The function executes when the user press the register button.
        It gets his credentials and sends a register request to the server.
        If the server approve it, he will get into his new account.

        """
        global entry_username
        global entry_password
        global entry_email
        if entry_username.get() and entry_password.get() and entry_email.get():
            request = "database#register#" + entry_username.get() + "#" + entry_password.get() + "#" + entry_email.get()
            self.make_socket()
            self.socket.send(request.encode())
            answer = self.socket.recv(CHECK_BUFFER).decode()
            self.socket.close()
            if answer == OK:
                save_username(entry_username.get())
                self.enter(entry_username.get())
            else:
                messagebox.showwarning("INVALID", "Invalid username, password or email")
        else:
            messagebox.showwarning("INVALID", "Some of the details are missing")

    def forgot_password(self):
        """

        The function executes when the user press the forgot password button.
        It gets his details and sends a forgot password request to the server.
        If the server approve it, he will get his password to his email.

        """
        global entry_username
        global entry_email
        if entry_username.get() and entry_email.get():
            request = "forgot#" + entry_username.get() + "#" + entry_email.get()
            self.make_socket()
            self.socket.send(request.encode())
            answer = self.socket.recv(CHECK_BUFFER).decode()
            self.socket.close()
            if answer == OK:
                self.forgot_password_page()
                messagebox.showwarning("SUCCESS!", "Your password was sent to your email successfully")
            else:
                messagebox.showwarning("INVALID", "Invalid username or email")
        else:
            messagebox.showwarning("INVALID", "Some of the details are missing")

    def enter(self, username):
        """

        The function enters the user into his account and leads him to the
        home page.

        Args:
            username (string): The username of the account.

        """
        set_online(1)
        self.get_frames(username)
        self.clear_all_screen(self.root)
        menubutton = super(AuthPage, self).set_menu_button(self.root)
        add_menu(self.root, menubutton)
        home_page()

    def get_frames(self, username):
        """

        The function asks from the server for all his media the user has
        shared in his account (statuses and pictures).
        The server checks which media frames the clients' computer already has
        and sends to it only those which it doesn't have to save time and
        resources.

        Args:
            username (string): The username of the account.

        """
        directory = os.path.dirname(os.path.realpath(__file__)) + "/facebook"
        if not os.path.exists(directory):
            os.mkdir(directory)
            ctypes.windll.kernel32.SetFileAttributesW(directory, 0x02)
        directory += "/" + username
        if not os.path.exists(directory):
            os.mkdir(directory)
        directory += "/"
        self.make_socket()
        request = GET_FRAMES + "#" + username
        self.socket.send(request.encode())
        frames = self.socket.recv(NAME_BUFFER).decode()
        try:
            frames = int(frames)
            for frame in range(frames):
                name = self.socket.recv(NAME_BUFFER).decode()
                if name != OK and not os.path.exists(directory + name):
                    self.socket.send(OK.encode())
                    data = self.socket.recv(WALL_BUFFER)
                    new_file = open(directory + name, "wb")
                    new_file.write(data)
                    new_file.close()
                else:
                    self.socket.send(NON.encode())
        except ValueError:
            #The user didn't update media yet
            pass
        self.socket.close()

    def email_user(self):
        """

        The function executes when the user press the email button.
        It gets his email address and message and sends an email
        request to the server.

        """
        global entry_address
        global entry_message
        if entry_address.get() and entry_message.get("1.0", END + "-1c"):
            request = "contact#" + entry_address.get() + "#" + entry_message.get("1.0", END)
            self.make_socket()
            self.socket.send(request.encode())
            answer = self.socket.recv(CHECK_BUFFER).decode()
            self.socket.close()
            if answer == OK:
                messagebox.showwarning("SUCCESS!", "Your email was sent successfully")
                self.contact_us_page()
            else:
                messagebox.showwarning("ERROR", "Your email was not sent from some reason.\nTry again later")
        else:
            messagebox.showwarning("INVALID", "Some of the details are missing")

    def make_socket(self):
        """

        The function makes a socket connection with the server.

        """
        self.socket = socket.socket()
        self.socket.connect((SERVER, PORT))
