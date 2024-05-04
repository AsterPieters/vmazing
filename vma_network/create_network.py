# create_network.py
# Create a network

# Imports
import subprocess
import argparse
import libvirt
import sys

# Set path
sys.path.append('/opt/vmazing')

# Custom modules
from tools._redis import redis_conn, redis_increment

def create_network(network_name):
    """
    Create a network.
    
    Args:
        network_name (str): Name of the network.
        
    Returns:
        str: The name if true, None if false.
    """
    # Connect to KVM
    conn = libvirt.open('qemu:///system')

    # Define bridge
    network_bridge_id = redis_increment("network_bridge_id")
    bridge_name = f"virbr{network_bridge_id}"

    # Define network
    network_third_octet = redis_increment("network_third_octet")
    network = f"192.168.{network_third_octet}"

    # Define id
    network_id = redis_increment("network_id")
    network_name = f"network-{network_id}"
    # Create network XML
    xml = f"""
    <network>
      <name>{network_name}</name>
      <bridge name='{bridge_name}'/>
      <forward mode='nat'/>
      <ip address='{network}.1' netmask='255.255.255.0'>
        <dhcp>
          <range start='{network}.2' end='{network}.254'/>
        </dhcp>
      </ip>
    </network>
    """

    try:
        # Create and start the network
        network = conn.networkDefineXML(xml)
        network.setAutostart(1)
        network.create()
        print(f"Network {network_name} created and started successfully.")

    except libvirt.libvirtError as e:
        print('Failed to create network: %s' % e, file=sys.stderr)
    finally:
        conn.close()

if __name__ == '__main__':
  
  # Take arguments
  parser = argparse.ArgumentParser(description="Create a network")
  parser.add_argument("network_name", help="Name of the network")
  args = parser.parse_args()

  create_network(args.network_name)