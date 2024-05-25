import pymongo
import datetime
from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference

# Access mongo and connect to the database
def conn_mongo(database_name):
    mongo_hosts = "mongo-service"
    mongodb_url = f"mongodb://{mongo_hosts}/"

    try:
        client = pymongo.MongoClient(mongodb_url, replicaSet="rs0")
        db = client[database_name]
        return db, client
    except Exception as e:
        print(f"An error occurred: {e}")

    except pymongo.errors.ConnectionFailure as e:
        # Handle connection failure errors
        print(f"Error connecting to MongoDB: {e}")
        return None, None

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return None, None


def generate_timestamp():
    # Get the time
    current_datetime = datetime.datetime.now()

    # Format it in time and date
    time = current_datetime.strftime("%H:%M:%S")
    date = current_datetime.strftime("%d/%m/%y")

    return f"{time} {date}"


def initialize_database(database):
    db, client = conn_mongo(database)

    database_names = client.list_database_names()
    print(database_name)

    client.close()

# Insert data into a collection of the database
def mongo_insert(database, collection, data):

    db, client = conn_mongo(database)

    collection = db[collection]

    document = {

        **data,
        "created": generate_timestamp()

    }

    result = collection.insert_one(document)
    client.close()

    # Check the result
    print("Inserted document ID:", result.inserted_id)

def mongo_delete(database, collection, name):
    
    db, client = conn_mongo(database)

    collection = db[collection]

    result = collection.delete_one({ 'name': name })
    client.close()

    # Check the result
    print("Deleted document ID:", result)

def document_edit(database, collection, identifier, identifier_value, identifier_of_value_to_be_changed, value):

    db, client = conn_mongo(database)

    collection = db[collection]

    # Update the document
    collection.update_one(
        {identifier: identifier_value},
        {"$set": {identifier_of_value_to_be_changed: value}}
    )

    client.close()

def list_collections(database, collection):
    
    db, client = conn_mongo(database)

    collection = db[collection]

    documents = collection.find()

    # Step 5: Print out the documents
    for document in documents:
        print(document)

def find_one(database, collection, data):
    
    db, client = conn_mongo(database)
    collection = db[collection]
    documents = collection.find_one(data)

    client.close()
    return documents