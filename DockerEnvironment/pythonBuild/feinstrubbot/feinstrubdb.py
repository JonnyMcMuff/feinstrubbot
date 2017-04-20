from pymongo import MongoClient  # MongoDB Library

class FeinstrubDbManager:
    def __init__(self, mongo_client, users=None):
        self.mongo_client = mongo_client
        self.users = users

    def get_user_db_connection(self):
        if not (self.users is None):
            return self.users

        db = self.mongo_client.feinstaub
        users = db['users']
        print("Connected to DB")
        return users
