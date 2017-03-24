from app import *
from constants import *
import time


def main():
    app = App()
    chat_receive()


def chat_receive():
    while True:
        if threading.active_count() == 2:
            my_socket = socket.socket()
            my_socket.connect((SERVER, PORT))
            username = get_username()
            if username:
                print(username)
            time.sleep(5)
        else:
            break


if __name__ == '__main__':
    main()
