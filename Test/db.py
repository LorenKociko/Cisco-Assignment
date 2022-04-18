from encodings import utf_8
import pymongo
from pymongo import MongoClient


with open("password.txt","r") as f:
    psw = f.readline()

connection_sting = f"mongodb+srv://cisco:{psw}@cisco.wzrhr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
cluster = MongoClient(connection_sting)

db = cluster["Cisco_Assigment"]
user_collection = db["user"]

user = {"name":"test","score":5}
user_collection.insert_one(user)

r = user_collection.find_one({"name":"test"})
print(r)