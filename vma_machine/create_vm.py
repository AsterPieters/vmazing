# create-vm.py
# Create a virtual machine

# Imports
import libvirt
import argparse
import sys

# Set path
sys.path.append('/vmazing')

# Modules
from vma_storage.create_disk import create_disk

def create_vm(vm_name, vm_memory, vm_vcpus, vm_storage, network):
    """
    Create a virtual machine.
    
    Args:
        vm_name (str): Name of the virtual machine.
        vm_memory (int): Ram size in Mb.
        vm_vcpus (int): Amount of vcpu's
        vm_storage (int): Amount of disksize
    """

    # Create the disk path
    disk_name = f"boot_disk_for_{vm_name}"

    # Create the disk
    boot_disk = create_disk(disk_name, str(vm_storage))
    if not boot_disk:
        return("Failed to create virtual machine.")

    # Connect to KVM
    conn = libvirt.open('qemu:///system')

    # Create VM XML
    xml = f"""
    <domain type='kvm'>
      <name>{vm_name}</name>
      <memory unit='MiB'>{str(vm_memory)}</memory>
      <vcpu placement='static'>{vm_vcpus}</vcpu>
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
      </devices>
    </domain>
    """

    # Define VM from XML
    dom = conn.createXML(xml, 0)

    if dom is not None:
        print(f"Virtual machine {vm_name} created successfully.")
    else:
        print(f"Failed to create virtual machine {vm_name}.")

    conn.close()

if __name__ == "__main__":

    # Take arguments
    parser = argparse.ArgumentParser(description="Create a virtual machine")
    parser.add_argument("vm_name", help="Name of the virtual machine")
    parser.add_argument("vm_memory", help="Ram size in Mb")
    parser.add_argument("vm_vcpus", help="Amount of vcpu's")
    parser.add_argument("vm_storage", help="Amount of disksize")
    parser.add_argument("vm_network", help="Name of the network")
    args = parser.parse_args()

    create_vm(args.vm_name, args.vm_memory, args.vm_vcpus, args.vm_storage, args.vm_network)