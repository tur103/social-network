import tkinter as tk
import getpass
import glob
import os
import tkFontChooser
from constants import *
from PIL import Image, ImageTk


class ScrolledWindow(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.font4 = tkFontChooser.Font(size=STATUS_SIZE)
        self.canvas = tk.Canvas(root, borderwidth=0, height=650, width=900)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.place(y=150)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.show_wall()

    def show_wall(self):
        user_folder = getpass.getuser()
        directory = "c:/users/" + user_folder + "/downloads/facebook/*.*"
        frames_list = glob.glob(directory)
        frames_list.sort(key=os.path.getmtime)
        frames_list = frames_list[::-1]
        yplace = 5
        for frame in frames_list:
            if not CHAT in frame:
                if frame.split(".")[-1] == "txt":
                    file = open(frame, "r")
                    data = file.read()
                    file.close()
                    rows = 0
                    if len(data) > 100:
                        rows = (len(data) // 100 + 1) * 5
                        data = "\n".join([data[i: i + 100] for i in range(0, len(data), 100)])
                    tk.Label(self.frame, text=data, font=self.font4).grid(row=yplace, pady=10)
                    yplace += 5
                    yplace += rows
                else:
                    image = Image.open(frame)
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(self.frame, image=photo)
                    label.image = photo
                    label.grid(row=yplace, pady=10)
                    yplace += 5

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
