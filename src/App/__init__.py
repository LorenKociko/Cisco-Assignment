from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

with open("password.txt","r") as f:
    psw = f.readline()

app.config["SECRET_KEY"] = 'b668czc68d29fd2b7f5976c54c39f6ec'
app.config['WTF_CSRF_SECRET_KEY'] = 'fe9d487ba2c9a1f13a5d72fa0d75d3fb'
app.config['MONGO_URI'] = f"mongodb+srv://cisco:{psw}@cisco.wzrhr.mongodb.net/CiscoAssigment?retryWrites=true&w=majority"


mongo_client = PyMongo(app)
db = mongo_client.db



bc_enc = Bcrypt()

# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "warning"

from App import routes
