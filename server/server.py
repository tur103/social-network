from database import *
from smtp import *
import socket
import glob
import os


def main():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(NUMBER_OF_CLIENTS)
    while True:
        (client_socket, client_address) = server_socket.accept()
        client_request = client_socket.recv(BUFFER).decode()
        if DATABASE in client_request:
            database = DataBase()
            if LOG_IN in client_request:
                credentials = client_request.split("#")[2:]
                match = database.check_user(credentials)
            elif REGISTER in client_request:
                credentials = client_request.split("#")[2:]
                match = database.add_user(credentials)
                if match:
                    open(DIRECTORY + credentials[0] + CHAT_FILE, "w").close()
                    if not os.path.exists(DIRECTORY + credentials[0] + FRIENDS):
                        open(DIRECTORY + credentials[0] + FRIENDS, "w").close()
                    if not os.path.exists(DIRECTORY + credentials[0] + REQUESTS):
                        open(DIRECTORY + credentials[0] + REQUESTS, "w").close()
            elif CHANGE in client_request:
                credentials = client_request.split("#")[2:]
                database.update_user(credentials[0], credentials[1])
                match = NOT
            else:
                match = False
            database.close_database()
        elif CONTACT in client_request:
            smtp_server = SMTP()
            credentials = client_request.split("#")[1:]
            if len(credentials) == 3:
                database = DataBase()
                credentials[0] = database.get_email(credentials[2])
                match = smtp_server.send_email(credentials[0], credentials[1], credentials[2])
            else:
                match = smtp_server.send_email(credentials[0], credentials[1])
        elif GET_FRAMES in client_request:
            folder = client_request.split("#")[1]
            frames_list = glob.glob(DIRECTORY + folder + "/*.*")
            client_socket.send(str(len(frames_list)).encode())
            for frame in frames_list:
                name = frame.split("\\")[-1]
                client_socket.send(name.encode())
                file = open(frame, "rb")
                data = file.read()
                file.close()
                client_socket.send(data)
                match = NOT
        elif UPLOAD_PICTURE in client_request:
            folder = client_request.split("#")[1] + "/"
            name = client_request.split("#")[2]
            data = client_socket.recv(IMAGE_BUFFER)
            new_file = open(DIRECTORY + folder + name, "wb")
            new_file.write(data)
            new_file.close()
            match = NOT
        elif UPLOAD_STATUS in client_request:
            folder = client_request.split("#")[1] + "/"
            name = client_request.split("#")[2]
            data = client_socket.recv(TEXT_BUFFER).decode()
            new_file = open(DIRECTORY + folder + name + ".txt", "w")
            new_file.write(data)
            new_file.close()
            match = NOT
        elif CHANGE in client_request:
            database = DataBase()
            if EMAIL in client_request:
                username = client_request.split("#")[2]
                email = client_request.split("#")[3]
                match = database.change_email(username, email)
            elif PASSWORD in client_request:
                username = client_request.split("#")[2]
                password = client_request.split("#")[3]
                match = database.change_password(username, password)
        elif FORGOT in client_request:
            smtp_server = SMTP()
            database = DataBase()
            username = client_request.split("#")[1]
            email = client_request.split("#")[2]
            password = database.get_password(username, email)
            if password:
                match = smtp_server.send_password(email, password)
            else:
                match = False
        elif GET_CHAT in client_request:
            user = client_request.split("#")[1]
            my_file = open(DIRECTORY + user + CHAT_FILE, "r")
            data = my_file.read()
            if data:
                client_socket.send(data.encode())
            else:
                client_socket.send(NO.encode())
            my_file.close()
            open(DIRECTORY + user + CHAT_FILE, "w").close()
            match = NOT
        elif ADD_FRIEND in client_request:
            folder = client_request.split("#")[1]
            user = client_request.split("#")[2]
            request_file = open(DIRECTORY + folder + REQUESTS, "r")
            data = request_file.read()
            if user in data:
                data = data.replace(user + "\n", "")
                request_file.close()
                request_file = open(DIRECTORY + folder + REQUESTS, "w")
                request_file.write(data)
                request_file.close()
                if not "-not" in user:
                    friends_file = open(DIRECTORY + folder + FRIENDS, "a")
                    friends_file.write(user + "\n")
                    friends_file.close()
                    friends_file = open(DIRECTORY + user + FRIENDS, "a")
                    friends_file.write(folder + "\n")
                    friends_file.close()
                match = True
            else:
                database = DataBase()
                users_list = database.get_users()
                if user in users_list:
                    request_file = open(DIRECTORY + user + REQUESTS, "a")
                    request_file.write(folder + "\n")
                    request_file.close()
                    match = True
                else:
                    match = False
        elif GET_REQUESTS in client_request:
            folder = client_request.split("#")[1]
            request_file = open(DIRECTORY + folder + REQUESTS)
            data = request_file.read()
            request_file.close()
            client_socket.send(data.encode())
            match = NOT
        else:
            match = False
        if match == NOT:
            pass
        elif match:
            client_socket.send(OK.encode())
        else:
            client_socket.send(NO.encode())
        client_socket.close()


if __name__ == '__main__':
    main()
