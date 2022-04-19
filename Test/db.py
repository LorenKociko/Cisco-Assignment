from encodings import utf_8
import pymongo
from pymongo import MongoClient
import re


# with open("password.txt","r") as f:
#     psw = f.readline()

connection_sting = f"mongodb+srv://cisco:C1sco12345@cisco.wzrhr.mongodb.net/Cisco_Assigment?retryWrites=true&w=majority"
cluster = MongoClient(connection_sting)

db = cluster["Cisco_Assigment"]
user_collection = db["user"]

user = {"name":"TesT","score":5}
user_collection.insert_one(user)

r = user_collection.find_one({"name":"test"})
username = "TesT"
user = user_collection.find_one({"name": re.compile('^' + username + '$', re.IGNORECASE)})
print(user)

