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

    def connect(self):
        mongodb_url = f"mongodb://{self.mongo_hosts}/"
        try:
            self.client = pymongo.MongoClient(mongodb_url)

            self.db = self.client[self.database]
            return self.db, self.client
        
        except pymongo.errors.ConnectionFailure as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            return None, None
        
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return None, None

    def fetch_documents(self, data=None):
        if data: # Fetch one document
            documents = self.collection.find_one(data)
        else: # Fetch all documents
            documents = self.collection.find()

        return documents

    def create_document(self, data):
        document = {
            **data,
            "created": self.generate_timestamp()
        }

        result = self.collection.insert_one(document)
        return result

    def update_document(self, id_key_value, data):
        result = self.collection.update_one(
            id_key_value,
            {"$set": data}
        )
        return result

    def delete_document(self, data):
        result = self.collection.delete_one(data)
        return result

    def generate_timestamp(self):
        # Get the time and date
        current_datetime = datetime.datetime.now()
        time = current_datetime.strftime("%H:%M:%S")
        date = current_datetime.strftime("%d/%m/%y")

        return f"{time} {date}"

    def close(self):
        if self.client:
            self.client.close()

class IgnoreServerSelectionLogs(logging.Filter): # Cant get this error fixed, so we just ignore it
    def filter(self, record):
        if record.name == "pymongo.serverSelection":
            return False
        return True