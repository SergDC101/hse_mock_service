from dotenv import load_dotenv
import os

from src.mongo import MongoManager

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_BASE = os.environ.get("MONGO_BASE")

SECRET_AUTH = os.environ.get("SECRET_AUTH")

mongo_manager = MongoManager(host=MONGO_HOST, port=int(MONGO_PORT), db_name=MONGO_BASE)

def get_mongo_manager():
    return mongo_manager


