from page import *
from tkinter import filedialog
import getpass
import glob
from PIL import Image, ImageTk
import socket
import time
import os
Image.LOAD_TRUNCATED_IMAGES = True


class MyWall(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.root = root
        self.username = username

    def add_elements(self, root, title):
        global entry_status
        super(MyWall, self).add_elements(root, title)
        entry_status = Entry(self.root, bg=CHOCOLATE, fg=WHITE, bd=5, font=self.font1,
                             exportselection=0, insertbackground=GOLD, insertwidth=10, width=40)
        entry_status.pack()
        entry_status.place(x=10, y=80)
        button_status = Button(root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                               font=self.font1, fg=WHITE, text=UPLOAD_STATUS,
                               command=self.upload_status)
        button_status.pack()
        button_status.place(x=650, y=70)
        button_picture = Button(root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                                font=self.font1, fg=WHITE, text=UPLOAD_PICTURE,
                                command=self.upload_picture)
        button_picture.pack()
        button_picture.place(x=650, y=10)
        self.show_frames()

    def upload_picture(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            user_folder = getpass.getuser()
            directory = "c:/users/" + user_folder + "/downloads/facebook/" + file_path.split("/")[-1]
            chosen_file = open(file_path, "rb")
            data = chosen_file.read()
            chosen_file.close()
            new_file = open(directory, "wb")
            new_file.write(data)
            new_file.close()
            sock = socket.socket()
            sock.connect((SERVER, PORT))
            request = "uploadpicture#" + self.username + "#" + file_path.split("/")[-1]
            sock.send(request.encode())
            time.sleep(1)
            sock.send(data)
            sock.close()
            self.show_frames()

    def upload_status(self):
        global entry_status
        message = entry_status.get()
        if message:
            request = "uploadstatus#" + self.username + "#" + message[0] + message[-1]
            user_folder = getpass.getuser()
            directory = "c:/users/" + user_folder + "/downloads/facebook/" + message[0] + message[-1] + ".txt"
            new_file = open(directory, "w")
            new_file.write(message)
            new_file.close()
            sock = socket.socket()
            sock.connect((SERVER, PORT))
            sock.send(request.encode())
            time.sleep(1)
            sock.send(message.encode())
            sock.close()
            entry_status.delete(0, END)
            self.show_frames()

    def show_frames(self):
        user_folder = getpass.getuser()
        directory = "c:/users/" + user_folder + "/downloads/facebook/*.*"
        frames_list = glob.glob(directory)
        frames_list.sort(key=os.path.getmtime)
        frames_list = frames_list[::-1]
        xplace = 300
        yplace = 150
        for frame in frames_list:
            if not CHAT in frame:
                if frame.split(".")[-1] == "txt":
                    file = open(frame, "r")
                    data = file.read()
                    file.close()
                    label = Label(self.root, text=data, font=self.font1)
                    label.pack()
                    label.place(x=xplace, y=yplace)
                    yplace += 70
                else:
                    image = Image.open(frame)
                    image = image.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    label = Label(self.root, image=photo)
                    label.image = photo
                    label.pack()
                    label.place(x=xplace, y=yplace)
                    yplace += 230
