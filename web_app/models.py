from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, name, password, active=True):
        self.id = id
        self.name = name
        self.password = password
        self.active = active
