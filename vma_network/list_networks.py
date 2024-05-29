import sys
import logging
import argparse

sys.path.append('/opt/vmazing')
from tools.mongo import MongoDBConnection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def list_networks(network_id=None, verbose=False):
    """
    List network(s).
    
    Args:
        network_id (optional) (int): Id of the network, use if only listing one.
        verbose (optional) (int): Print verbose output

    Returns:
        str: All network(s) info.
    """

    try:
        # Connect to mongo
        connection = MongoDBConnection("networks", "virtual_networks")

        # List one network
        if network_id:
            documents = connection.fetch_documents({"Network Id": int(network_id)})

        # List multiple networks
        else:
            documents = connection.fetch_documents()

        # Print the output
        if verbose:
            
            if network_id:
                for key, value in documents.items():
                    print(f"{key}: {value}")
            else:
                for document in documents:
                    for key, value in document.items():
                        print(f"{key}: {value}")
                    print("") # Separate networks
        else:
            return documents
            logger.info("Fetched data from mongoDB.")

    except Exception as e:
        logger.error(f"Error fetching data from mongo. {e}")
        return

    finally:
        connection.close()

if __name__ == '__main__':
    # Take arguments
    parser = argparse.ArgumentParser(description="List network info")
    parser.add_argument("--network_id", help="Id of the network", required=False)
    parser.add_argument("--verbose", help="Print verbose output", required=False, action='store_true')
    args = parser.parse_args()

    list_networks(args.network_id, args.verbose)
