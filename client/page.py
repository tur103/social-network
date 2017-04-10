from tkinter import *
import tkFontChooser
from constants import *


class Page(object):
    def __init__(self, root):
        object.__init__(self)
        root.title(TITLE)
        root.geometry(PAGE_SIZE)
        root.iconbitmap(default=ICON)
        self.font1 = tkFontChooser.Font(size=MENU_SIZE, weight=BOLD)
        self.font2 = tkFontChooser.Font(size=TEXT_SIZE, weight=BOLD)
        self.font3 = tkFontChooser.Font(size=TITLE_SIZE, weight=BOLD)
        self.font4 = tkFontChooser.Font(size=STATUS_SIZE)

    def set_menu_button(self, root):
        menubutton = Menubutton(root, activebackground=MAGENTA,
                                activeforeground=CYAN, cursor=PLUS_CURSOR,
                                bg=ORANGE_RED, fg=CYAN, disabledforeground=BLACK,
                                highlightcolor=WHITE, text=MENU_TITLE, bd=10,
                                relief=RAISED, font=self.font1)
        menubutton.menu = Menu(menubutton, font=self.font2,
                               activeforeground=BLUE, disabledforeground=RED,
                               selectcolor=GREEN)
        menubutton["menu"] = menubutton.menu
        return menubutton

    def clear_screen(self, root):
        for widget in root.winfo_children():
            if MENU_BUTTON not in repr(widget):
                widget.destroy()

    def clear_all_screen(self, root):
        for widget in root.winfo_children():
            widget.destroy()

    def add_elements(self, root, title):
        label = Label(root, font=self.font3, fg=PURPLE, text=title)
        label.pack()
