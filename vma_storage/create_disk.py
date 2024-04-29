# create-disk.py

# Imports
import subprocess
import argparse

def create_disk(disk_name, size_in_gb):
    """
    Create a disk using qemu-img.
    
    Args:
        disk_name (str): Name of the disk.
        size_gb (int): Disk size in Gb.
        
    Returns:
        bool: image_path if creation was succesfull, false otherwise
    """

    image_path = f"/vma-diskstore/{disk_name}.qcow"

    try:
        # Create disk
        subprocess.run(["qemu-img", "create", "-f", "qcow2", image_path, str(size_in_gb) + "G"])

        print(f"Disk {disk_name} created succesfully.")
        return image_path

    except Exception as e:
        print(f"Failed to create disk: {e}")
        return False

if __name__ == "__main__":

    # Take arguments
    parser = argparse.ArgumentParser(description="Create a disk")
    parser.add_argument("disk_name", help="Name of the disk to be created")
    parser.add_argument("size_in_gb", type=int, help="Size of the disk in gigabytes")
    args = parser.parse_args()

    create_disk(args.disk_name, args.size_in_gb)
