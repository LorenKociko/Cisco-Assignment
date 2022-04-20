import datetime
import uuid
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, username, email, password, _id=None):

        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
    # @staticmethod
    # def is_authenticated():
    #     return True

    # @staticmethod
    # def is_active():
    #     return True

    # @staticmethod
    # def is_anonymous():
    #     return False

    # def get_id(self):
    #     return self._id
