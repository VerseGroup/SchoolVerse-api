# mongo imports
import os
from pymongo import MongoClient

# secrets


def start_mongo():
    client = MongoClient(host = "mongodb://maltech.org:27027/", username = "schoolverseadmin", password = "D8qBzt&KzLq&kt93", connect=True)
    return client["schoolverse"]

mongo_db = start_mongo()
users = mongo_db["users"].find({"_id": "5f9b9b9b9b9b9b9b9b9b9b9b"})


for user in users:
    print(user)

