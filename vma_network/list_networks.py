import sys

# Set path
sys.path.append('/opt/vmazing')

from tools.mongo import MongoDBConnection

connection = MongoDBConnection("networks", "virtual_networks")
documents = connection.fetch_documents()

for document in documents:
    for key, value in document.items():
        print(f"{key}: {value}")
    print("\n --- \n")

connection.close()