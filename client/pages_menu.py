from home_page import *
from my_wall import *
from settings_page import *
from add_friends import *
import auth_page
from search_friends import *
from private_chat import *


def add_menu(root, menubutton):
        global global_root
        global_root = root
        menubutton.menu.add_command(label=HOME_PAGE, command=home_page)
        menubutton.menu.add_command(label=MY_WALL, command=my_wall)
        menubutton.menu.add_command(label=SEARCH_FRIENDS, command=search_friends)
        menubutton.menu.add_command(label=PRIVATE_CHAT, command=private_chat)
        menubutton.menu.add_command(label=ADD_FRIENDS, command=add_friends)
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


def search_friends():
    search = SearchFriends(global_root, username)
    search.clear_screen(global_root)
    search.add_elements(global_root, SEARCH_FRIENDS)


def private_chat():
    chat = PrivateChat(global_root, username)
    chat.clear_screen(global_root)
    chat.add_elements(global_root, PRIVATE_CHAT)


def add_friends():
    add = AddFriends(global_root, username)
    add.clear_screen(global_root)
    add.add_elements(global_root, ADD_FRIENDS)


def settings_page():
    sett = SettingsPage(global_root, username)
    sett.clear_screen(global_root)
    sett.add_elements(global_root, SETTINGS_PAGE)


def offline(value=None):
    global username
    sock = socket.socket()
    sock.connect((SERVER, PORT))
    if value == 0:
        request = "database#change#" + username + "#" + str(value)
    else:
        request = "database#change#" + username + "#change"
    sock.send(request.encode())
    sock.close()
    on = get_online()
    if on:
        set_online(0)
    else:
        set_online(1)


def log_out():
    offline(0)
    global username
    username = None
    set_online(0)
    auth = auth_page.AuthPage(global_root)
    menubutton_auth = auth.set_menu_button(global_root)
    menubutton_auth.pack()
    menubutton_auth.place(x=LEFTT)


def save_username(user):
    global username
    username = user


def get_username():
    global username
    try:
        return username
    except NameError:
        return None


def set_online(state):
    global online
    online = state


def get_online():
    global online
    try:
        return online
    except NameError:
        return None
