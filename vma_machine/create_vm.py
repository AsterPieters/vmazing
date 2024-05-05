# create-vm.py
# Create a virtual machine

# Imports
import libvirt
import argparse
import sys

# Set path
sys.path.append('/opt/vmazing')

# Custom modules
from vma_storage.create_disk import create_disk

def create_vm(name, memory, vcpus, boot_disk_size, network):
    """
    Create a virtual machine.
    
    Args:
        name (str): Name of the virtual machine.
        memory (int): Ram size in Mb.
        vcpus (int): Amount of vcpu's
        boot_disk_size (int): Size of bootdisk
        network (str): Name of the network to run in
    """

    # Create the disk path
    disk_name = f"boot_disk_for_{name}"

    # Create the disk
    boot_disk = create_disk(disk_name, str(boot_disk_size))
    if not boot_disk:
        return("Failed to create virtual machine.")

    # Connect to KVM
    conn = libvirt.open('qemu:///system')

    # Create VM XML
    xml = f"""
    <domain type='kvm'>
      <name>{name}</name>
      <memory unit='MiB'>{str(memory)}</memory>
      <vcpu placement='static'>{vcpus}</vcpu>
      <os>
        <type arch='x86_64' machine='pc-i440fx-2.12'>hvm</type>
        <boot dev='hd'/>
      </os>
      <devices>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='{boot_disk}'/>
          <target dev='vda' bus='virtio'/>
        </disk>
        <interface type='network'>
          <source network='{network}'/>
        </interface>
        <graphics type='vnc' port='5900' autoport='yes' keymap='en-us'/>
      </devices>
    </domain>
    """

    # Define VM from XML
    dom = conn.createXML(xml, 0)

    if dom is not None:
        print(f"Virtual machine {name} created successfully.")
    else:
        print(f"Failed to create virtual machine {name}.")

    conn.close()

if __name__ == "__main__":

    # Take arguments
    parser = argparse.ArgumentParser(description="Create a virtual machine")
    parser.add_argument("name", help="Name of the virtual machine")
    parser.add_argument("memory", help="Ram size in Mb")
    parser.add_argument("vcpus", help="Amount of vcpu's")
    parser.add_argument("boot_disk_size", help="Amount of disksize")
    parser.add_argument("network", help="Name of the network")
    args = parser.parse_args()

    create_vm(args.name, args.memory, args.vcpus, args.boot_disk_size, args.network)