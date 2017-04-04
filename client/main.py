from app import *
from constants import *
import time
from database import *


def main():
    app = App()
    chat_receive()


def chat_receive():
    directory = os.path.dirname(os.path.realpath(__file__)) + "/facebook/chat.db"
    while True:
        if threading.active_count() == 2:
            if get_username():
                username = get_username()
                my_socket = socket.socket()
                my_socket.connect((SERVER, PORT))
                request = "getchat#" + username
                my_socket.send(request.encode())
                answer = my_socket.recv(CHAT_BUFFER).decode()
                if answer != NON:
                    answer = eval(answer)
                    chat_database = DataBase(directory)
                    for row in answer:
                        chat_database.add_message(row[0], row[1], row[2])
                    chat_database.close_database()
                my_socket.close()
            time.sleep(5)
        else:
            break


if __name__ == '__main__':
    main()
