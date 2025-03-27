import csv
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse

def extract_data_from_urls(csv_file_path, json_output_path, csv_output_path):
    """
    Extract JSON data from a list of URLs and save specified fields to CSV.
    
    Args:
        csv_file_path (str): Path to input CSV file containing URLs
        json_output_path (str): Path to save the complete JSON data
        csv_output_path (str): Path to save extracted fields in CSV format
    """
    # Read URLs from CSV file
    urls = []
    try:
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            # Skip header if present
            header = next(reader, None)
            for row in reader:
                if row and len(row) > 0:  # Ensure row is not empty
                    urls.append(row[0].strip())  # URL is the only column
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # List to store all extracted JSON data
    all_json_data = []
    
    # List to store extracted specific fields
    extracted_fields = []
    
    # Process each URL
    for i, url in enumerate(urls):
        try:
            print(f"Processing URL {i+1}/{len(urls)}: {url}")
            
            # Add a delay to avoid overloading the server
            if i > 0:
                time.sleep(1)
                
            # Check if URL is valid
            if not url.startswith(('http://', 'https://')):
                print(f"Invalid URL format: {url}, skipping...")
                continue
                
            # Make HTTP request
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the script tag containing JSON data
            script_tag = soup.find('script', id='__NEXT_DATA__')
            
            if not script_tag:
                print(f"Script tag not found in {url}, skipping...")
                continue
                
            # Extract and parse JSON data
            json_data = json.loads(script_tag.string)
            
            # Store the complete JSON data
            all_json_data.append(json_data)
            
            # Extract specific fields from pageProps
            if 'props' in json_data and 'pageProps' in json_data['props']:
                page_props = json_data['props']['pageProps']
                
                # Extract required fields
                name = page_props.get('name', '')
                address_lines = page_props.get('addressLines', [])
                address = '; '.join(address_lines) if address_lines else ''
                phone_number = page_props.get('phoneNumber', '')
                vendor_id = page_props.get('vendorId', '')
                
                # Add to extracted fields list
                extracted_fields.append({
                    'name': name,
                    'addressLines': address,
                    'phoneNumber': phone_number,
                    'vendorId': vendor_id,
                    'source_url': url
                })
            else:
                print(f"pageProps not found in JSON from {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"HTTP request error for {url}: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON parsing error for {url}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {url}: {e}")
    
    # Save all JSON data to file
    try:
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_json_data, f, indent=2, ensure_ascii=False)
        print(f"All JSON data saved to {json_output_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
    
    # Save extracted fields to CSV
    try:
        df = pd.DataFrame(extracted_fields)
        df.to_csv(csv_output_path, index=False)
        print(f"Extracted fields saved to {csv_output_path}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

if __name__ == "__main__":
    # File paths
    input_csv = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/OK_child_care_provider_urls_20250327.csv"  # CSV file containing URLs
    json_output = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/OK_child_care_providers_20250327.json"  # Output JSON file
    csv_output = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/OK_child_care_providers_20250327.csv"  # Output CSV file
    
    # Run the extraction process
    extract_data_from_urls(input_csv, json_output, csv_output)