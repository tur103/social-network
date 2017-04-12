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
            if get_username() and get_online():
                username = get_username()
                my_socket = socket.socket()
                my_socket.connect((SERVER, PORT))
                request = "getchat#" + username
                my_socket.send(request.encode())
                answer = my_socket.recv(CHAT_BUFFER).decode()
                if answer != NON:
                    answer = eval(answer)
                    chat_database = DataBase(directory)
                    senders_list = []
                    for row in answer:
                        chat_database.add_message(row[0], row[1], row[2])
                        if row[1] == PrivateChat.in_chat_with:
                            PrivateChat.received_message(row[1], row[2])
                        else:
                            senders_list.append(row[1])
                    senders_list = set(senders_list)
                    for sender in senders_list:
                        chat_database.add_message(username, sender, "###new_message###")
                    chat_database.close_database()
                my_socket.close()
            time.sleep(2)
        else:
            break


if __name__ == '__main__':
    main()
