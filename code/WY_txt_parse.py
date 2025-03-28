import csv
import re

def parse_providers(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Prepare data for CSV
    providers = []
    current_provider = None
    current_name = None
    current_address = []
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            if current_provider and current_name and current_address:
                providers.append([current_provider, current_name, ' '.join(current_address)])
                current_provider = None
                current_name = None
                current_address = []
            continue
            
        # Check if line starts with a provider number
        match = re.match(r'#(\d+)\s+(.+)', line)
        if match:
            # If we have a previous provider, save it
            if current_provider and current_name and current_address:
                providers.append([current_provider, current_name, ' '.join(current_address)])
            
            # Start new provider
            current_provider = match.group(1)
            current_name = match.group(2)
            current_address = []
        elif current_provider:
            # Add to current address
            current_address.append(line)
    
    # Add the last provider if exists
    if current_provider and current_name and current_address:
        providers.append([current_provider, current_name, ' '.join(current_address)])
    
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['provider_number', 'provider_name', 'address'])  # Header
        writer.writerows(providers)

if __name__ == "__main__":
    input_file = "data/raw/WY_child_care_providers_20250328.txt"
    output_file = "data/intermediate/WY_child_care_providers_20250328.csv"
    parse_providers(input_file, output_file)
    print(f"Successfully converted {input_file} to {output_file}") 