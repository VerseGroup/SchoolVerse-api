# mongo imports
import os
from pymongo import MongoClient

# secrets


def start_mongo():
    client = MongoClient(host = "mongodb://maltech.org:27027/", username = "schoolverseadmin", password = "D8qBzt&KzLq&kt93", connect=True)
    return client["schoolverse"]



