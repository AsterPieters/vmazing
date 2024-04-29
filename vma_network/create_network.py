# create_network.py
# Create a network

# Imports
import subprocess
import argparse
import libvirt
import redis
import sys

def get_virtual_bridge_id():
  """
  Get the id from redis and increment it
  """

  # Connect to Redis
  redis_host = 'localhost'
  redis_port = 6379
  redis_password = None
  redis_db = 0

  r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

  # Retrieve the key
  key = 'network_bridge_id'
  old_value = r.get(key)

  # Increment by one
  new_value = int(old_value) + 1
  r.set(key, new_value)

  # Check if the key exists and print the value
  if new_value is not None:
      return new_value
  else:
      return False

def create_network(network_name, network_id):
    """
    Create a network.
    
    Args:
        network_name (str): Name of the network.
        subnet (str): Subnet in CIDR notation.
        
    Returns:
        str: The name if true, None if false.
    """
    # Connect to KVM
    conn = libvirt.open('qemu:///system')

    bridge_id = get_virtual_bridge_id()
    bridge_name = f"virbr{bridge_id}"

    # Create network XML
    xml = f"""
    <network>
      <name>{network_name}</name>
      <bridge name='{bridge_name}'/>
      <forward mode='nat'/>
      <ip address='192.168.{network_id}.1' netmask='255.255.255.0'>
        <dhcp>
          <range start='192.168.{network_id}.2' end='192.168.{network_id}.254'/>
        </dhcp>
      </ip>
    </network>
    """

    try:
        # Create and start the network
        network = conn.networkDefineXML(xml)
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
  parser.add_argument("network_id", help="Network ID")
  args = parser.parse_args()

  create_network(args.network_name, args.network_id)