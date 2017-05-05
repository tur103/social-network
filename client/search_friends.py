"""
Author          :   Or Israeli
FileName        :   search_friends.py
Date            :   5.5.17
Version         :   1.0
"""

from page import *
import socket
from scrolled_window import *


class SearchFriends(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.root = root
        self.username = username

    def add_elements(self, root, title):
        """

        The function displays the search friends page.
        The user can choose one friend from his friends list
        and see his wall.

        Args:
            root (Tk): The Tk window.
            title (string): The name of the page.

        """
        super(SearchFriends, self).add_elements(root, title)
        label = Label(root, font=self.font1, fg=FIREBRICK1, text=SEARCH_FRIENDS_TEXT)
        label.pack()
        label.place(x=150, y=100)
        self.add_friends_scrollbar()

    def add_friends_scrollbar(self):
        """

        The function presents the friends list of the user.
        It allows him to choose one friend and see his wall.

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
            global lb
            lb = Listbox(self.root, bd=10, bg=PEACHPUFF2, font=self.font1,
                         fg=ORANGE_RED, height=length, selectbackground=GREEN,
                         selectmode="single", relief="sunken", width=20, yscrollcommand=scroll.set)
            i = 1
            for raw in friends:
                lb.insert(i, raw)
                i += 1
            lb.pack()
            lb.place(y=300, x=250)
            scroll.config(command=lb.yview)
            button_wall = Button(self.root, bg=GOLD, activebackground=GOLD,
                                 font=self.font1, fg=RED, text=SHOW_WALL,
                                 command=self.show_wall)
            button_wall.pack()
            button_wall.place(x=650, y=220)
        sock.close()

    def show_wall(self):
        """

        The function gets the selected friend and displays his wall.

        """
        global lb
        index = lb.curselection()
        if index:
            selected_user = lb.get(index)
            self.get_frames(selected_user)
            ScrolledWindow(self.root, selected_user).pack(side="bottom", fill="both", expand=True)

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
        directory = os.path.dirname(os.path.realpath(__file__)) + "/facebook/" + username
        if not os.path.exists(directory):
            os.mkdir(directory)
        directory += "/"
        sock = socket.socket()
        sock.connect((SERVER, PORT))
        request = GET_FRAMES + "#" + username
        sock.send(request.encode())
        frames = sock.recv(NAME_BUFFER).decode()
        try:
            frames = int(frames)
            for frame in range(frames):
                name = sock.recv(NAME_BUFFER).decode()
                if name != OK and not CHAT_DATABASE in name and \
                        not os.path.exists(directory + name):
                    sock.send(OK.encode())
                    data = sock.recv(WALL_BUFFER)
                    new_file = open(directory + name, "wb")
                    new_file.write(data)
                    new_file.close()
                else:
                    sock.send(NON.encode())
        except ValueError:
            #The user didn't update media yet
            pass
        sock.close()
