from home_page import *
from my_wall import *
from settings_page import *
import socket
import auth_page


def add_menu(root, menubutton):
        global global_root
        global_root = root
        menubutton.menu.add_command(label=HOME_PAGE, command=home_page)
        menubutton.menu.add_command(label=MY_WALL, command=my_wall)
        menubutton.menu.add_command(label=SEARCH_FRIENDS, command=home_page)
        menubutton.menu.add_command(label=PRIVATE_CHAT, command=home_page)
        menubutton.menu.add_command(label=GROUP_CHAT, command=home_page)
        menubutton.menu.add_command(label=DOWNLOAD_MOVIE, command=home_page)
        menubutton.menu.add_command(label=DOWNLOAD_YOUTUBE, command=home_page)
        menubutton.menu.add_command(label=SETTINGS, command=settings_page)
        menubutton.menu.add_checkbutton(label=OFFLINE, command=offline)
        menubutton.menu.add_command(label=LOG_OUT, command=log_out)
        menubutton.pack()
        menubutton.place(x=LEFTT)


def home_page():
        home = HomePage(global_root)
        home.clear_screen(global_root)
        home.add_elements(global_root, HOME_PAGE)


def my_wall():
    wall = MyWall(global_root, username)
    wall.clear_screen(global_root)
    wall.add_elements(global_root, MY_WALL)


def settings_page():
    sett = SettingsPage(global_root, username)
    sett.clear_screen(global_root)
    sett.add_elements(global_root, SETTINGS_PAGE)


def offline():
    sock = socket.socket()
    sock.connect((SERVER, PORT))
    request = "database#change#" + username + "#change"
    sock.send(request.encode())
    sock.close()


def log_out():
    auth = auth_page.AuthPage(global_root)
    menubutton_auth = auth.set_menu_button(global_root)
    menubutton_auth.pack()
    menubutton_auth.place(x=LEFTT)


def save_username(user):
    global username
    username = user
