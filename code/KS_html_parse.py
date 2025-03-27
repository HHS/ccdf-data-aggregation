from bs4 import BeautifulSoup
import csv
import re

# Proof of concept for Kansas data extraction
"""
Script to extract provider names and addresses from html file pulled from KS search

To do:
- Selenium to enter search criteria and pull paginated html results
    -  This will require data/raw/KS_zip_city_county.txt
- Iterate through html results and extract provider names and addresses
- Save results to csv

input: html file
output: txt file containing provider details extracted from html
output: csv file with clean provider names, addresses, and other fields

"""

# Load HTML from file
with open("/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/KS_html_source_Salina_6702.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# Extract provider names
providers = soup.find_all("a", class_="moreINFO")

# Extract addresses (assuming they are in the next div after provider name)
# TODO: Figure out how many divs are needed to get the address 
addresses = []
for provider in providers:
    parent_div = provider.find_parent("div")
    if parent_div:
        address_div = parent_div.find_next_sibling("div")
        if address_div:
            address_text = " ".join(address_div.stripped_strings)
            addresses.append((provider.text, address_text))

# Save results
for name, address in addresses:
    #print(f"Provider: {name}, Address: {address}")
    # write to txt file
    with open("/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/KS_child_care_providers.txt", "a") as file:
        file.write(f"Provider: {name}, Address: {address}\n")

# Read input string from txt file
with open("/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/KS_child_care_providers.txt", "r") as file:
    input_string = file.read()

# Split the input string by newlines
lines = input_string.strip().split('\n')

# Initialize an empty list to hold the parsed records
records = []

# Process every two lines as a provider and address
for i in range(0, len(lines), 2):
    provider_line = lines[i]
    address_line = lines[i + 1]

    # Extract the provider name from the first line (after "Provider: ")
    provider_name = provider_line.split('Provider: ')[1].split(',')[0].strip()
    
    # Extract the address from the second line (after "Address: ")
    address = address_line.split('Address: ')[1].strip()

    # Initialize default values for optional fields
    provider_type = None
    license_id = None
    capacity = None
    ages_served = None
    hours = None
    
    # Extract optional fields using regex
    type_match = re.search(r'Type: (.*?)(?= License ID|$)', provider_line)
    license_id_match = re.search(r'License ID: (\S+)', provider_line)
    capacity_match = re.search(r'Capacity : (\d+)', provider_line)
    ages_served_match = re.search(r'Ages Served : (.*?)(?= Monday|$)', provider_line)
    hours_match = re.search(r'Monday.*', provider_line)  # captures the first "Monday" line for hours
    
    if type_match:
        provider_type = type_match.group(1).strip()
    if license_id_match:
        license_id = license_id_match.group(1).strip()
    if capacity_match:
        capacity = capacity_match.group(1).strip()
    if ages_served_match:
        ages_served = ages_served_match.group(1).strip()
    if hours_match:
        hours = hours_match.group(0).strip()

    # Append the record to the list
    records.append([provider_name, address, provider_type, license_id, capacity, ages_served, hours])

# Define the CSV file path
csv_file = '/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/KS_child_care_providers.csv'

# Write to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Provider Name', 'Address', 'Type', 'License ID', 'Capacity', 'Ages Served', 'Hours'])  # CSV header
    writer.writerows(records)

print(f"Data successfully written to {csv_file}")