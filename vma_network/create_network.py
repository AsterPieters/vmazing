import subprocess
import argparse
import logging
import libvirt
import sys
import re

sys.path.append('/opt/vmazing')
from tools.mongo import MongoDBConnection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def increment_network_id():
    try:
        connection = MongoDBConnection("networks", "keys")

        # Get the network_id sequence
        document = connection.fetch_documents({'name': 'network_id_sequence'})

        # Increment and update the value
        new_network_id = document['value'] + 1
        result = connection.update_document({'name': "network_id_sequence"}, {'value': new_network_id})
        if result:
          logger.info(f"Assigned network id: {new_network_id}")

    except Exception as e:
        logger.error(f"Error incrementing network ID: {e}")
        return None

    finally:
        connection.close()
        return new_network_id

def create_network(network_name, network_description, network):
    """
    Create a network.
    
    Args:
        network_name (str): Name of the network.
        network_description (str): Description of the network
        network (str): Network

    Returns:
        str: The name if true, None if false.
    """
    # Define id and use it as virtual bridge
    network_id = increment_network_id()
    bridge_name = f"virbr{network_id}"

    # Cut off the last part of the network
    network = re.sub(r'\.\d+$', '.', network)

    # Create network XML
    xml = f"""
    <network>
      <name>network-{network_id}</name>
      <bridge name='{bridge_name}'/>
      <forward mode='nat'/>
      <ip address='{network}1' netmask='255.255.255.0'>
        <dhcp>
          <range start='{network}2' end='{network}254'/>
        </dhcp>
      </ip>
    </network>
    """

    # Not yet implemented
    hub = "vmazing-hub-01"
    network_type = "Virtual Bridge"

    data = {
        "Network Name": network_name,
        "Network Description": network_description,
        "Network Id": network_id,
        "Network": f"{network}0",
        "Hub": hub,
        "Type": network_type
    }

    # Connect to the local libvirt instance
    conn = libvirt.open()
    if conn is None:
        logger.error("Failed to connect to the hypervisor.")
        return

    else:
        logger.info("Connected to the hypervisor.")

    try:
        # Create and start the network
        network = conn.networkDefineXML(xml)
        network.setAutostart(1)
        network.create()
        logger.info("Created network.")

        # Insert the data in mongo
        connection = MongoDBConnection("networks", "virtual_networks")
        result = connection.create_document(data)

        if result:
            logger.info("Added data to mongoDB")

    except libvirt.libvirtError as e:
        logger.error("Error connecting to the hypervisor: %s" % e, file=sys.stderr)

    except Exception as e:
        logger.error(f"Something went wrong creating the virtual network: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    # Take arguments
    parser = argparse.ArgumentParser(description="Create a network")
    parser.add_argument("network_name", help="Name of the network")
    parser.add_argument("network_description", help="Description of the network")
    parser.add_argument("network", help="Network, e.g 192.168.10.0")
    args = parser.parse_args()

    create_network(args.network_name, args.network_description, args.network)
