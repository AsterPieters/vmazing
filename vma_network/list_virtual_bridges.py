import subprocess

def list_virtual_bridges():
    try:
        # Run the virsh command to list virtual networks
        result = subprocess.run(['virsh', 'net-list', '--all'], capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            
            # Extract virtual bridge names from the output
            virtual_bridges = []
            for line in output_lines[2:]:  # Skip header lines
                if line.strip():  # Check for non-empty lines
                    bridge_name = line.split()[0]
                    virtual_bridges.append(bridge_name)
                    
            return virtual_bridges
        else:
            print("Error: Failed to run virsh command.")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

# Call the function to list virtual bridges
available_bridges = list_virtual_bridges()
if available_bridges:
    print("Available Virtual Bridges:")
    for bridge in available_bridges:
        print(bridge)
else:
    print("No virtual bridges found.")