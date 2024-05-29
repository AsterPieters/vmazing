import sys
import logging
import libvirt
import argparse

sys.path.append('/opt/vmazing')
from tools.mongo import MongoDBConnection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def delete_network(network_name):

    conn = libvirt.open()
    if conn is None:
        print('Failed to open connection to the hypervisor.')
        return

    else:
        logger.info("Connected to the hypervisor.")

    try:
        # Find the network by name
        network = conn.networkLookupByName(network_name)
        if network is None:
            logger.error(f"Network {network_name} not found.")
            return False

        # Destroy the network if it's active
        if network.isActive():
            network.destroy()
            logger.info(f"Network {network_name} destroyed.")

        # Undefine the network
        network.undefine()
        logger.info(f"Network {network_name} undefined.")

    except libvirt.libvirtError as e:
        logger.error(f"Error while deleting network {network_name}: {e}")
        return False

    finally:
        conn.close()

    # Delete data from mongodb
    network_id = network_name.removeprefix("network-")
    connection = MongoDBConnection("networks", "virtual_networks")
    result = connection.delete_document({"Network Id": int(network_id)})
    if result:
        logger.info("Deleted data from mongoDB")
    else:
        logger.error("Error deleting data from mongodb")
        
if __name__ == "__main__":

    # Take arguments
    parser = argparse.ArgumentParser(description="Delete a network")
    parser.add_argument("network_name", help="Name of the network")
    args = parser.parse_args()

    delete_network(args.network_name)