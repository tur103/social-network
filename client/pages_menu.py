"""
Author          :   Or Israeli
FileName        :   pages_menu.py
Date            :   5.5.17
Version         :   1.0
"""

from home_page import *
from my_wall import *
from settings_page import *
from add_friends import *
import auth_page
from search_friends import *
from private_chat import *


def add_menu(root, menubutton):
    """

    The function sets the menu options of pages to the menu button.

    Args:
        root (Tk): The Tk window
        menubutton (Menubutton): The menu button widget that holds the menu.

    """
    global global_root
    global deselect
    deselect = IntVar()
    global_root = root
    menubutton.menu.add_command(label=HOME_PAGE, command=home_page)
    menubutton.menu.add_command(label=MY_WALL, command=my_wall)
    menubutton.menu.add_command(label=SEARCH_FRIENDS, command=search_friends)
    menubutton.menu.add_command(label=PRIVATE_CHAT, command=private_chat)
    menubutton.menu.add_command(label=ADD_FRIENDS, command=add_friends)
    menubutton.menu.add_command(label=SETTINGS, command=settings_page)
    menubutton.menu.add_checkbutton(label=OFFLINE, command=offline,
                                    variable=deselect)
    menubutton.menu.add_command(label=LOG_OUT, command=log_out)
    menubutton.pack()
    menubutton.place(x=LEFTT)


def home_page():
    """

    The function switches the page for the home page.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    home = HomePage(global_root)
    home.clear_screen(global_root)
    home.add_elements(global_root, HOME_PAGE)


def my_wall():
    """

    The function switches the page for the my wall page.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    wall = MyWall(global_root, username)
    wall.clear_screen(global_root)
    wall.add_elements(global_root, MY_WALL)


def search_friends():
    """

    The function switches the page for the search friends page.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    search = SearchFriends(global_root, username)
    search.clear_screen(global_root)
    search.add_elements(global_root, SEARCH_FRIENDS)


def private_chat():
    """

    The function switches the page for the private chat page.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    chat = PrivateChat(global_root, username)
    chat.clear_screen(global_root)
    chat.add_elements(global_root, PRIVATE_CHAT)


def add_friends():
    """

    The function switches the page for the add friends page.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    add = AddFriends(global_root, username)
    add.clear_screen(global_root)
    add.add_elements(global_root, ADD_FRIENDS)


def settings_page():
    """

    The function switches the page for the settings page.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    sett = SettingsPage(global_root, username)
    sett.clear_screen(global_root)
    sett.add_elements(global_root, SETTINGS_PAGE)


def offline(value=None):
    """

    The function executes when the user press the offline button.
    It tells the server to consider this account as offline so
    the user will not get any messages.

    Args:
        value (int): Whether to get offline or online.

    """
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
    """

    The function executes when the user press the log out button.
    It will log him out from his account and set him offline.

    """
    PrivateChat.in_chat_with = False
    PrivateChat.in_unread = False
    offline(0)
    deselect.set(0)
    global username
    username = None
    set_online(0)
    auth = auth_page.AuthPage(global_root)
    menubutton_auth = auth.set_menu_button(global_root)
    menubutton_auth.pack()
    menubutton_auth.place(x=LEFTT)


def save_username(user):
    """

    The function saves the username of the current account.

    Args:
        user (string): The username of the current account.

    """
    global username
    username = user


def get_username():
    """

    The function returns the username of the current account.

    Returns:
        string: The username of the current account.

    """
    global username
    try:
        return username
    except NameError:
        return None


def set_online(state):
    """

    The function saves the current state of the account.
    online or offline.

    Args:
        state (int): Online or offline (0 or 1).

    """
    global online
    online = state


def get_online():
    """

    The function returns the state of the account.
    online or offline.

    Returns:
        int: Online or offline (0 or 1).

    """
    global online
    try:
        return online
    except NameError:
        return None
