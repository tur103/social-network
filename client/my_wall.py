from page import *
from tkinter import filedialog
import socket
import time
from tkinter import messagebox
from scrolled_window import *
import speech_recognition as sr
Image.LOAD_TRUNCATED_IMAGES = True


class MyWall(Page):
    def __init__(self, root, username):
        Page.__init__(self, root)
        self.root = root
        self.username = username

    def add_elements(self, root, title):
        ScrolledWindow(self.root).pack(side="bottom", fill="both", expand=True)
        global entry_status
        super(MyWall, self).add_elements(root, title)
        entry_status = Entry(self.root, bg=CHOCOLATE, fg=WHITE, bd=5, font=self.font1,
                             exportselection=0, insertbackground=GOLD, insertwidth=10, width=35)
        entry_status.pack()
        entry_status.place(x=122, y=80)
        button_status = Button(root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                               font=self.font1, fg=WHITE, text=UPLOAD_STATUS,
                               command=self.upload_status)
        button_status.pack()
        button_status.place(x=660, y=70)
        button_picture = Button(root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                                font=self.font1, fg=WHITE, text=UPLOAD_PICTURE,
                                command=self.upload_picture)
        button_picture.pack()
        button_picture.place(x=650, y=10)
        button_record = Button(root, bg=ROYAL_BLUE, activebackground=ROYAL_BLUE,
                               font=self.font1, fg=WHITE, text=RECORD,
                               command=self.record_status)
        button_record.pack()
        button_record.place(x=0, y=70)

    def upload_picture(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if file_path[-3:].lower() in FORMATS_LIST:
                user_folder = getpass.getuser()
                directory = "c:/users/" + user_folder + "/downloads/facebook/" + file_path.split("/")[-1]
                chosen_file = open(file_path, "rb")
                data = chosen_file.read()
                chosen_file.close()
                new_file = open(directory, "wb")
                new_file.write(data)
                new_file.close()
                image = Image.open(directory)
                image = image.resize((200, 200), Image.ANTIALIAS)
                image.save(directory)
                new_file = open(directory, "rb")
                data = new_file.read()
                new_file.close()
                sock = socket.socket()
                sock.connect((SERVER, PORT))
                request = "uploadpicture#" + self.username + "#" + file_path.split("/")[-1]
                sock.send(request.encode())
                time.sleep(1)
                sock.send(data)
                sock.close()
                self.clear_screen(self.root)
                self.add_elements(self.root, MY_WALL)
            else:
                messagebox.showwarning("ERROR!", "this file is not match to "
                                       "the following formats:\nJPG, PNG")

    def upload_status(self):
        global entry_status
        message = entry_status.get()
        if message:
            name = "status-" + message.split(" ")[0] + message.split(" ")[-1]
            request = "uploadstatus#" + self.username + "#" + name
            user_folder = getpass.getuser()
            directory = "c:/users/" + user_folder + "/downloads/facebook/" + name + ".txt"
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
            self.clear_screen(self.root)
            self.add_elements(self.root, MY_WALL)

    def record_status(self):
        global entry_status
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            entry_status.delete(0, END)
            entry_status.insert(0, r.recognize_google(audio))
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
