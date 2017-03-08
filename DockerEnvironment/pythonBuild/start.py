from pymongo import MongoClient # MongoDB Library
import datetime # used to create a sample document with timestamp
import pprint # pretty printer for the mongodb data
def main():
    client = MongoClient()
    # Use the name of the image in docker-compose here i.e. database as host
    client = MongoClient('database', 27017)
    # Get the mongo database
    db = client['test-database']
    # get a mongo db collection
    collection = db['test-collection']
    # Create a document
    post = {"author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()}
    # Inserting a document
    collection.insert_one(post).inserted_id
    # Use for example findOne to retrieve a document
    print("The following document has been inserted: \n")
    pprint.pprint(collection.find_one({"author": "Mike"}))
if __name__ == '__main__':
    main()
