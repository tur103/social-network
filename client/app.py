import threading
from auth_page import *


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        """

        The function closes the app window.

        """
        self.root.quit()

    def run(self):
        """

        The function creates the Tk window and calls for the first
        page's display.

        """
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        auth_page = AuthPage(self.root)
        menubutton_auth = auth_page.set_menu_button(self.root)
        menubutton_auth.pack()
        menubutton_auth.place(x=LEFTT)
        self.root.mainloop()
