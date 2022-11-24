# mongo imports
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


# secrets


def start_mongo():
    MONGO_URL = os.getenv("PRODUCTION_MONGO_URL")
    MONGO_USERNAME = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASS")

    client = MongoClient(host = MONGO_URL, username = MONGO_USER, password = MONGO_PASS, connect=True)
    return client["schoolverse"]



