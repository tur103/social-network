import os
HOST = "0.0.0.0"
PORT = 8820
NUMBER_OF_CLIENTS = 1
BUFFER = 1024
IMAGE_BUFFER = 3000000
TEXT_BUFFER = 100
CHECK_BUFFER = 2

DATABASE_PATH = "database.db"
SERVER_CHAT = "chat.db"
FRIENDS_DATABASE = "/friends.db"
REQUESTS_DATABASE = "/requests.db"
CHAT_DATABASE = "/chat.db"
FRIENDS_END = "friends.db"
REQUESTS_END = "requests.db"

OK = "OK"
NO = "NO"
NOT = "not"

DATABASE = "database"
LOG_IN = "login"
REGISTER = "register"
CHANGE = "change"
CONTACT = "contact"
GET_FRAMES = "getframes"
UPLOAD_PICTURE = "uploadpicture"
UPLOAD_STATUS = "uploadstatus"
GET_CHAT = "getchat"
ADD_FRIEND = "addfriend"
GET_REQUESTS = "getrequests"
GET_FRIENDS = "getfriends"
SEND_MESSAGE = "sendmessage"

DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/users_database/"

MY_EMAIL = "tur103103@gmail.com"
MY_PASSWORD = "103103103"
EMAIL = "email"
PASSWORD = "password"
FORGOT = "forgot"
CHAT_FILE = "/chat.txt"
FRIENDS = "/friends.txt"
REQUESTS = "/requests.txt"

CHAT = "chat"
REQUEST = "request"
FRIEND = "friend"

PASSWORD_TEXT = "Hello dear user! This is an email to restore your " \
                "password from the social-network software. " \
                "Your password is -->  "
