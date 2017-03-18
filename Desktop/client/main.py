from auth_page import *
from constants import *


root = Tk()


def main():
    auth_page = AuthPage(root)
    menubutton_auth = auth_page.set_menu_button(root)
    menubutton_auth.pack()
    menubutton_auth.place(x=LEFTT)
    root.mainloop()


if __name__ == '__main__':
    main()
