from page import *


class HomePage(Page):
    def __init__(self, root):
        Page.__init__(self, root)

    def add_elements(self, root, title):
        super(HomePage, self).add_elements(root, title)
        label1 = Label(root, font=self.font1, fg=FIREBRICK1, text=HOME_PAGE_TEXT1, pady=35)
        label1.pack()
        label1 = Label(root, font=self.font1, fg=GOLD, text=HOME_PAGE_TEXT2, justify="left")
        label1.pack()
