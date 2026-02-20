from dotenv import load_dotenv
import os

from src.mongo import MongoManager

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

MONGO_LINK = f"mongodb://{os.environ.get("MONGO_HOST")}:{os.environ.get("MONGO_PORT")}/"
MONGO_BASE = os.environ.get("MONGO_BASE")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
