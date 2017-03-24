from app import *
from constants import *
import time


def main():
    app = App()
    chat_receive()


def chat_receive():
    user_folder = getpass.getuser()
    directory = "c:/users/" + user_folder + "/downloads/facebook/chat.txt"
    while True:
        if threading.active_count() == 2:
            if get_username():
                username = get_username()
                my_socket = socket.socket()
                my_socket.connect((SERVER, PORT))
                request = "getchat#" + username
                my_socket.send(request.encode())
                answer = my_socket.recv(CHAT_BUFFER).decode()
                if answer != NO:
                    my_file = open(directory, "a")
                    my_file.write(answer)
                    my_file.close()
                my_socket.close()
            time.sleep(5)
        else:
            break


if __name__ == '__main__':
    main()
