from pymongo import MongoClient
from GenericFeed import config

database = MongoClient(config.MONGODB_URL).get_database("GenericFeed")