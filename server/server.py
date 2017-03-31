from database import *
from smtp import *
import socket
import glob


def main():
    # db = DataBase(DATABASE_PATH)
    # db.drop_database()
    # db.create_database()
    # db.close_database()
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(NUMBER_OF_CLIENTS)
    while True:
        (client_socket, client_address) = server_socket.accept()
        client_request = client_socket.recv(BUFFER).decode()
        if DATABASE in client_request:
            database = DataBase(DATABASE_PATH)
            if LOG_IN in client_request:
                credentials = client_request.split("#")[2:]
                match = database.check_user(credentials)
            elif REGISTER in client_request:
                credentials = client_request.split("#")[2:]
                match = database.add_user(credentials)
                if match:
                    open(DIRECTORY + credentials[0] + CHAT_FILE, "w").close()
                    friends_database = DataBase(FRIENDS_PATH + credentials[0] + FRIENDS_DATABASE)
                    friends_database.create_friends_database()
                    friends_database.close_database()
                    requests_database = DataBase(FRIENDS_PATH + credentials[0] + REQUESTS_DATABASE)
                    requests_database.create_requests_database()
                    requests_database.close_database()
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
                database = DataBase(DATABASE_PATH)
                credentials[0] = database.get_email(credentials[2])
                match = smtp_server.send_email(credentials[0], credentials[1], credentials[2])
            else:
                match = smtp_server.send_email(credentials[0], credentials[1])
        elif GET_FRAMES in client_request:
            folder = client_request.split("#")[1]
            frames_list = glob.glob(DIRECTORY + folder + "/*.*")
            length = 0
            for frame in frames_list:
                if not CHAT in frame and not DATABASE_END in frame:
                    length += 1
            client_socket.send(str(length).encode())
            for frame in frames_list:
                if not CHAT in frame and not DATABASE_END in frame:
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
            database = DataBase(DATABASE_PATH)
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
            database = DataBase(DATABASE_PATH)
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
            requests_database = DataBase(FRIENDS_PATH + folder + REQUESTS_DATABASE)
            ans = requests_database.delete_request(user)
            requests_database.close_database()
            if ans:
                if not "-not" in user:
                    friends_database = DataBase(FRIENDS_PATH + folder + FRIENDS_DATABASE)
                    friends_database.add_friend(user)
                    friends_database.close_database()
                    friends_database = DataBase(FRIENDS_PATH + user + FRIENDS_DATABASE)
                    friends_database.add_friend(folder)
                    friends_database.close_database()
                match = True
            else:
                database = DataBase(DATABASE_PATH)
                users_list = database.get_users()
                database.close_database()
                if user in users_list:
                    friends_database = DataBase(FRIENDS_PATH + folder + FRIENDS_DATABASE)
                    friends_list = friends_database.get_friends()
                    friends_database.close_database()
                    if user not in friends_list:
                        requests_database = DataBase(FRIENDS_PATH + user + REQUESTS_DATABASE)
                        requests_database.add_request(folder)
                        requests_database.close_database()
                        match = True
                    else:
                        match = False
                else:
                    match = False
        elif GET_REQUESTS in client_request:
            folder = client_request.split("#")[1]
            requests_database = DataBase(FRIENDS_PATH + folder + REQUESTS_DATABASE)
            list_of_requests = requests_database.get_requests()
            string_of_requests = ",".join(list_of_requests)
            client_socket.send(string_of_requests.encode())
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
