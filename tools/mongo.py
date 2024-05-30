import pymongo
import datetime
import logging
from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ignore the serverSelection errors
pymongologger = logging.getLogger("pymongo.serverSelection")
pymongologger.setLevel(logging.CRITICAL)

class MongoDBConnection:
    def __init__(self, database, collection):
        self.mongo_hosts = "mongo-service:27017"
        self.database = database

        # Connect and get the collection
        self.connect()
        self.collection = self.db[collection]

    # Decorator to do all error handling for the mongo functions
    def error_handling(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except pymongo.errors.ConnectionFailure as e:
                logger.error(f"Error connecting to MongoDB: {e}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Error occurred in monogoDB: {e}", exc_info=True)
                raise
        return wrapper

    @error_handling
    def connect(self):
        mongodb_url = f"mongodb://{self.mongo_hosts}/"
        self.client = pymongo.MongoClient(mongodb_url)
        self.db = self.client[self.database]
        return self.db, self.client
    
    @error_handling
    def fetch_documents(self, data=None):
        if data: # Fetch one document
            documents = self.collection.find_one(data)
        else: # Fetch all documents
            documents = self.collection.find()

        return documents

    @error_handling
    def create_document(self, data):
        document = {
            **data,
            "created": self.generate_timestamp()
        }

        result = self.collection.insert_one(document)
        return result

    @error_handling
    def update_document(self, id_key_value, data):
        result = self.collection.update_one(
            id_key_value,
            {"$set": data}
        )
        return result

    @error_handling
    def delete_document(self, data):
        result = self.collection.delete_one(data)
        return result

    @error_handling
    def generate_timestamp(self):
        # Get the time and date
        current_datetime = datetime.datetime.now()
        time = current_datetime.strftime("%H:%M:%S")
        date = current_datetime.strftime("%d/%m/%y")

        return f"{time} {date}"

    @error_handling
    def increment_key(self, data):
        # Get the network_id sequence
        result = self.fetch_documents({'name': data})

        # Increment and update the value
        incremented_key = result['value'] + 1
        result = self.update_document({'name': data}, {'value': incremented_key})
        return incremented_key

    @error_handling
    def close(self):
        if self.client:
            self.client.close()

class IgnoreServerSelectionLogs(logging.Filter): # Cant get this error fixed, so we just ignore it
    def filter(self, record):
        if record.name == "pymongo.serverSelection":
            return False
        return True