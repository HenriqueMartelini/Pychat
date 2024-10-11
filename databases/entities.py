import datetime
import bcrypt

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def convert_to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
        }

class Message:
    def __init__(self, sender, recipient, subject, body, datetime: datetime.datetime):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.datetime = datetime

    def convert_to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'subject': self.subject,
            'body': self.body,
            'datetime': self.datetime.isoformat()
        }