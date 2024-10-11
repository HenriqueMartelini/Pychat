import os
from dotenv import load_dotenv
from pymongo import MongoClient
import bcrypt
from cryptography.fernet import Fernet
from databases.entities import User, Message
import datetime

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

class MongoHandler:
    def __init__(self, connection_string=os.getenv("MONGO_URI"), database_name="pychat"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.database = None
        self.fernet = Fernet(SECRET_KEY)

    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.database = self.client[self.database_name]
        except Exception as e:
            print(f"Falha na conexão com o Banco de Dados: {e}")
            self.client = None

    def add_user(self, username, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.database["users"].insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        print("Usuário adicionado com sucesso!")

    def authenticate(self, email, password) -> bool:
        user_data = self.database["users"].find_one({"email": email})
        if user_data:
            user = User(user_data['username'], user_data['email'], user_data['password'])
            if user.check_password(password):
                return True
        return False

    def send_message(self, sender, recipient, subject, body):
        encrypted_body = self.fernet.encrypt(body.encode()).decode()
        message = Message(sender, recipient, subject, encrypted_body, datetime.datetime.now())
        self.database["messages"].insert_one(message.convert_to_dict())
        print("Mensagem enviada com sucesso!")

    def get_last_message(self, user):
        message_data = self.database["messages"].find_one({"recipient": user}, sort=[("datetime", -1)])
        if message_data:
            message = Message(
                sender=message_data["sender"],
                recipient=message_data["recipient"],
                subject=message_data["subject"],
                body=message_data["body"],
                datetime=datetime.datetime.fromisoformat(message_data["datetime"])
            )
            return message
        return None