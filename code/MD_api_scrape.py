#%%
import requests
import json
import csv
from datetime import datetime
import time
import pandas as pd
#%%
# API endpoint from the network request
url = "https://excels.marylandexcels.org/directory/search"

#%%
# Maryland zip codes with latitude/longitude coordinates
# Read the data/processed/US_zip_lat_long/US.csv file and create a dictionary of zip codes with their coordinates
md_zip_codes = pd.read_csv('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/processed/US_zip_lat_long.csv')

#%%
# Keep only the postal_code and latitude columns
md_zip_codes = md_zip_codes[['postal_code', 'admin_code1', 'latitude', 'longitude']]

# Keep only MD zip codes - admin_code1 is MD
md_zip_codes = md_zip_codes[md_zip_codes['admin_code1'] == 'MD']

#%%
# Create a dictionary of zip codes with their coordinates
md_zip_codes_dict = md_zip_codes.set_index('postal_code').to_dict(orient='index')

#%%
# Function to fetch records using zip code filtering with a radius
def fetch_records_by_zip_codes(base_url, zip_codes_dict, distance=2):
    """
    Fetches records from the API using zip code filtering with a radius.
    
    Args:
        base_url (str): The API endpoint URL
        zip_codes_dict (dict): Dictionary of zip codes with latitude/longitude coordinates
        distance (int): Search radius in miles
        
    Returns:
        list: All unique records from all zip codes combined
    """
    all_data = []
    seen_ids = set()
    total_zip_codes = len(zip_codes_dict)
    
    print(f"Starting to fetch data for {total_zip_codes} zip codes with {distance} mile radius...")
    
    # Create progress tracker
    progress_intervals = [int(total_zip_codes * p) for p in [0.25, 0.5, 0.75, 1.0]]
    
    for idx, (zip_code, coordinates) in enumerate(zip_codes_dict.items(), 1):
        print(f"Fetching data for zip code {zip_code} ({idx}/{total_zip_codes})...")
        
        # Prepare parameters for this request
        params = {
            'nameOrZip': zip_code,
            'name': '',
            'participant': 0,
            'zip': '',
            'distance': distance,
            'latitude': coordinates['latitude'],
            'longitude': coordinates['longitude'],
            'countyMode': False
        }
        
        # Send request
        try:
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                try:
                    # Parse JSON response
                    data = response.json()
                    
                    # Check if we received any data
                    if isinstance(data, list):
                        new_records = 0
                        for record in data:
                            # Use license number as unique identifier
                            record_id = record.get('license')
                            
                            if record_id not in seen_ids:
                                seen_ids.add(record_id)
                                all_data.append(record)
                                new_records += 1
                        
                        print(f"Received {len(data)} records, added {new_records} new unique records")
                        
                        # Save progress after each 50 zip codes or when we've processed 25%, 50%, 75%, and 100%
                        if idx % 50 == 0 or idx in progress_intervals:
                            # Get date for file name
                            date = datetime.now().strftime("%Y%m%d")
                            
                            # Save intermediate progress
                            progress_file = f'MD_child_care_providers_progress_{idx}_of_{total_zip_codes}_{date}.json'
                            with open(progress_file, 'w') as f:
                                json.dump(all_data, f)
                            print(f"Saved progress: {len(all_data)} records to {progress_file}")
                    else:
                        print(f"No data or invalid data format received for zip code {zip_code}")
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for zip code {zip_code}: {e}")
            else:
                print(f"Request failed with status code {response.status_code} for zip code {zip_code}")
                
        except Exception as e:
            print(f"Exception occurred while fetching data for zip code {zip_code}: {e}")
            
        # Add a small delay to avoid overwhelming the API
        time.sleep(2)  # Increased to 2 seconds to be more conservative
        
        # Print progress
        if idx in progress_intervals:
            print(f"Progress: {idx}/{total_zip_codes} zip codes processed ({int(idx/total_zip_codes*100)}%)")
    
    print(f"Completed fetching data for all zip codes. Total unique records: {len(all_data)}")
    return all_data

#%%
# Function to save data to files
def save_data(data, file_prefix):
    """
    Save data to JSON and CSV files
    
    Args:
        data (list): The data to save
        file_prefix (str): Prefix for the filenames
    """
    # Get date for file name
    date = datetime.now().strftime("%Y%m%d")
    
    # Save the data to a JSON file
    json_filename = f'{file_prefix}_{date}.json'
    with open(json_filename, 'w') as f:
        json.dump(data, f)
    print(f"Saved JSON file with {len(data)} records to {json_filename}")

    # Save the data to a CSV file
    if isinstance(data, list) and len(data) > 0:
        csv_filename = f'{file_prefix}_{date}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            # For the Maryland data, area_ratings and achievements are nested objects
            # We need to handle these specially for CSV output
            fields = list(data[0].keys())
            
            writer = csv.writer(f)
            writer.writerow(fields)  # Write the header
            
            for row in data:
                # Convert complex fields to strings for CSV compatibility
                values = []
                for field in fields:
                    value = row.get(field, '')
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value)
                    values.append(value)
                
                writer.writerow(values)
                
        print(f"Saved CSV file with {len(data)} records to {csv_filename}")
    else:
        print("No data to save to CSV")

#%%
# Main execution
if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    
    # Fetch all records using zip code filtering with a 2-mile radius
    all_records = fetch_records_by_zip_codes(url, md_zip_codes_dict, distance=2)
    
    # Save the complete dataset
    save_data(all_records, "MD_child_care_providers_complete")
    
    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\nExecution completed in {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Total unique records collected: {len(all_records)}")


#%%
