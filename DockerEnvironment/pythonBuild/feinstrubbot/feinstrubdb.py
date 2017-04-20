from pymongo import MongoClient  # MongoDB Library

class FeinstrubDbManager:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def get_user_db_connection(self):
        db = self.mongo_client.feinstaub
        users = db['users']
        print("Connected to DB", self.users)
        return users
