import csv
import os

# Define input and output file paths
input_file = "data/raw/US_zip_lat_long/US.txt"
output_file = "data/processed/US_zip_lat_long.csv"

# Define column names from readme
columns = [
    "country_code",
    "postal_code",
    "place_name",
    "admin_name1",
    "admin_code1",
    "admin_name2",
    "admin_code2",
    "admin_name3",
    "admin_code3",
    "latitude",
    "longitude",
    "accuracy"
]

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Read tab-separated file and write to CSV
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    # Create CSV writer
    writer = csv.writer(outfile)
    
    # Write header
    writer.writerow(columns)
    
    # Process each line
    for line in infile:
        # Split by tab and write to CSV
        writer.writerow(line.strip().split('\t'))

print(f"Successfully converted {input_file} to {output_file}") 