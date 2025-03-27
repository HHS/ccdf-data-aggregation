import requests
import json
import csv
from datetime import datetime
import time
import pandas as pd

# API endpoint for Rhode Island child care providers
url = "https://earlylearningprograms.dhs.ri.gov/Provider/GetProviderInfoList"

# Rhode Island zip codes with latitude/longitude coordinates
# Read the same zip code file used for Maryland
ri_zip_codes = pd.read_csv('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/processed/US_zip_lat_long.csv')

# Keep only the postal_code and latitude columns
ri_zip_codes = ri_zip_codes[['postal_code', 'admin_code1', 'latitude', 'longitude']]

# Keep only RI zip codes - admin_code1 is RI
ri_zip_codes = ri_zip_codes[ri_zip_codes['admin_code1'] == 'RI']

# Create a dictionary of zip codes with their coordinates
ri_zip_codes_dict = ri_zip_codes.set_index('postal_code').to_dict(orient='index')

# def fetch_records_by_zip_codes(base_url, zip_codes_dict, distance=2):
#     """
#     Fetches records from the RI API using zip code filtering.
    
#     Args:
#         base_url (str): The API endpoint URL
#         zip_codes_dict (dict): Dictionary of zip codes with latitude/longitude coordinates
#         distance (int): Search radius (not directly used, but kept for consistency)
        
#     Returns:
#         list: All unique records from all zip codes combined
#     """
#     all_data = []
#     seen_ids = set()
#     total_zip_codes = len(zip_codes_dict)
    
#     print(f"Starting to fetch data for {total_zip_codes} zip codes...")
    
#     # Create progress tracker
#     progress_intervals = [int(total_zip_codes * p) for p in [0.25, 0.5, 0.75, 1.0]]
    
#     # Prepare headers for the request
#     headers = {
#         'accept': 'application/json, text/javascript, */*; q=0.01',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'x-requested-with': 'XMLHttpRequest',
#         'origin': 'https://earlylearningprograms.dhs.ri.gov',
#         'referer': 'https://earlylearningprograms.dhs.ri.gov/'
#     }
    
#     for idx, (zip_code, coordinates) in enumerate(zip_codes_dict.items(), 1):
#         print(f"Fetching data for zip code {zip_code} ({idx}/{total_zip_codes})...")
        
#         # Prepare form data for the POST request
#         form_data = {
#             'draw': '2',
#             'columns[0][data]': '0',
#             'columns[0][name]': '',
#             'columns[0][searchable]': 'true',
#             'columns[0][orderable]': 'true',
#             'columns[0][search][value]': '',
#             'columns[0][search][regex]': 'false',
#             'columns[1][data]': 'City',
#             'columns[1][name]': 'City',
#             'columns[1][searchable]': 'true',
#             'columns[1][orderable]': 'true',
#             'columns[1][search][value]': '',
#             'columns[1][search][regex]': 'false',
#             'columns[2][data]': 'Setting',
#             'columns[2][name]': 'Setting',
#             'columns[2][searchable]': 'true',
#             'columns[2][orderable]': 'true',
#             'columns[2][search][value]': '',
#             'columns[2][search][regex]': 'false',
#             'columns[3][data]': 'CCAP',
#             'columns[3][name]': 'Accepts CCAP',
#             'columns[3][searchable]': 'true',
#             'columns[3][orderable]': 'true',
#             'columns[3][search][value]': '',
#             'columns[3][search][regex]': 'false',
#             'columns[4][data]': 'Availability',
#             'columns[4][name]': 'Availability',
#             'columns[4][searchable]': 'true',
#             'columns[4][orderable]': 'true',
#             'columns[4][search][value]': '',
#             'columns[4][search][regex]': 'false',
#             'columns[5][data]': 'Status',
#             'columns[5][name]': 'Program Status',
#             'columns[5][searchable]': 'true',
#             'columns[5][orderable]': 'true',
#             'columns[5][search][value]': '',
#             'columns[5][search][regex]': 'false',
#             'columns[6][data]': '6',
#             'columns[6][name]': '',
#             'columns[6][searchable]': 'true',
#             'columns[6][orderable]': 'true',
#             'columns[6][search][value]': '',
#             'columns[6][search][regex]': 'false',
#             'order[0][column]': '0',
#             'order[0][dir]': 'asc',
#             'start': '0',
#             'length': '-1',
#             'search[value]': '',
#             'search[regex]': 'false',
#             'ProviderName': '',
#             'City': '',
#             'Zipcode': '02809',
#             'Infants': 'false',
#             'Toddlers': 'false',
#             'PreSchool': 'false',
#             'SchoolAge': 'false',
#             'CenterBased': 'false',
#             'FamilyHome': 'false',
#             'SchoolBased': 'false',
#             'DHS': 'false',
#             'BSR': 'false',
#             'RIDE': 'false',
#             'CCAP': 'false',
#             'NAFCC': 'false',
#             'COA': 'false',
#             'NAEYC': 'false'
#         }
        
#         # Send request
#         try:
#             response = requests.post(base_url, headers=headers, data=form_data)
            
#             if response.status_code == 200:
#                 try:
#                     # Parse JSON response
#                     data = response.json()
                    
#                     # Check if we received any data
#                     if isinstance(data, dict) and 'data' in data:
#                         new_records = 0
#                         for record in data['data']:
#                             # Use ProviderId as unique identifier
#                             record_id = record.get('ProviderId')
                            
#                             if record_id and record_id not in seen_ids:
#                                 seen_ids.add(record_id)
#                                 all_data.append(record)
#                                 new_records += 1
                        
#                         print(f"Received {len(data['data'])} records, added {new_records} new unique records")
                        
#                         # Save progress after each 50 zip codes or when we've processed 25%, 50%, 75%, and 100%
#                         if idx % 50 == 0 or idx in progress_intervals:
#                             # Get date for file name
#                             date = datetime.now().strftime("%Y%m%d")
                            
#                             # Save intermediate progress
#                             progress_file = f'RI_child_care_providers_progress_{idx}_of_{total_zip_codes}_{date}.json'
#                             with open(progress_file, 'w') as f:
#                                 json.dump(all_data, f)
#                             print(f"Saved progress: {len(all_data)} records to {progress_file}")
#                     else:
#                         print(f"No data or invalid data format received for zip code {zip_code}")
                        
#                 except json.JSONDecodeError as e:
#                     print(f"Error parsing JSON for zip code {zip_code}: {e}")
#             else:
#                 print(f"Request failed with status code {response.status_code} for zip code {zip_code}")
                
#         except Exception as e:
#             print(f"Exception occurred while fetching data for zip code {zip_code}: {e}")
            
#         # Add a small delay to avoid overwhelming the API
#         time.sleep(2)  # Increased to 2 seconds to be more conservative
        
#         # Print progress
#         if idx in progress_intervals:
#             print(f"Progress: {idx}/{total_zip_codes} zip codes processed ({int(idx/total_zip_codes*100)}%)")
    
#     print(f"Completed fetching data for all zip codes. Total unique records: {len(all_data)}")
#     return all_data

def fetch_records_by_zip_codes(base_url, zip_codes_dict, distance=2):
    """
    Fetches records from the RI API using zip code filtering.
    
    Args:
        base_url (str): The API endpoint URL
        zip_codes_dict (dict): Dictionary of zip codes with latitude/longitude coordinates
        distance (int): Search radius (not directly used, but kept for consistency)
        
    Returns:
        list: All unique records from all zip codes combined
    """
    all_data = []
    seen_ids = set()
    total_zip_codes = len(zip_codes_dict)
    
    print(f"Starting to fetch data for {total_zip_codes} zip codes...")
    
    # Create progress tracker
    progress_intervals = [int(total_zip_codes * p) for p in [0.25, 0.5, 0.75, 1.0]]
    
    # Prepare headers for the request
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://earlylearningprograms.dhs.ri.gov',
        'referer': 'https://earlylearningprograms.dhs.ri.gov/'
    }
    
    for idx, (zip_code, coordinates) in enumerate(zip_codes_dict.items(), 1):
        print(f"Fetching data for zip code {zip_code} ({idx}/{total_zip_codes})...")
        
        # Ensure zip_code is a string and padded to 5 digits if needed
        zip_code_str = str(zip_code).zfill(5)
        
        # Prepare form data for the POST request
        form_data = {
            'draw': '2',
            'columns[0][data]': '0',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': 'City',
            'columns[1][name]': 'City',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': 'Setting',
            'columns[2][name]': 'Setting',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': 'CCAP',
            'columns[3][name]': 'Accepts CCAP',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': 'Availability',
            'columns[4][name]': 'Availability',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'columns[5][data]': 'Status',
            'columns[5][name]': 'Program Status',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'true',
            'columns[5][search][value]': '',
            'columns[5][search][regex]': 'false',
            'columns[6][data]': '6',
            'columns[6][name]': '',
            'columns[6][searchable]': 'true',
            'columns[6][orderable]': 'true',
            'columns[6][search][value]': '',
            'columns[6][search][regex]': 'false',
            'order[0][column]': '0',
            'order[0][dir]': 'asc',
            'start': '0',
            'length': '-1',
            'search[value]': '',
            'search[regex]': 'false',
            'ProviderName': '',
            'City': '',
            'Zipcode': zip_code_str,  # Dynamically set zip code
            'Infants': 'false',
            'Toddlers': 'false',
            'PreSchool': 'false',
            'SchoolAge': 'false',
            'CenterBased': 'false',
            'FamilyHome': 'false',
            'SchoolBased': 'false',
            'DHS': 'false',
            'BSR': 'false',
            'RIDE': 'false',
            'CCAP': 'false',
            'NAFCC': 'false',
            'COA': 'false',
            'NAEYC': 'false'
        }
        
        # Send request
        try:
            response = requests.post(base_url, headers=headers, data=form_data)
            
            # Add more detailed error logging
            if response.status_code != 200:
                print(f"Error for zip code {zip_code_str}:")
                print(f"Status Code: {response.status_code}")
                #print(f"Response Content: {response.text}")
                #print(f"Request Headers: {headers}")
                #print(f"Form Data: {form_data}")
                continue  # Skip to next iteration instead of halting completely
            
            try:
                # Parse JSON response
                data = response.json()
                
                # Check if we received any data
                if isinstance(data, dict) and 'data' in data:
                    new_records = 0
                    for record in data['data']:
                        # Use ProviderId as unique identifier
                        record_id = record.get('ProviderId')
                        
                        if record_id and record_id not in seen_ids:
                            seen_ids.add(record_id)
                            all_data.append(record)
                            new_records += 1
                    
                    print(f"Received {len(data['data'])} records, added {new_records} new unique records")
                    
                    # Save progress logic remains the same...
                else:
                    print(f"No data or invalid data format received for zip code {zip_code_str}")
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for zip code {zip_code_str}: {e}")
                print(f"Response content: {response.text}")
        
        except Exception as e:
            print(f"Exception occurred while fetching data for zip code {zip_code_str}: {e}")
            
        # Add a small delay to avoid overwhelming the API
        time.sleep(2)  # Increased to 2 seconds to be more conservative
        
        # Print progress logic remains the same...
    
    print(f"Completed fetching data for all zip codes. Total unique records: {len(all_data)}")
    return all_data

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
            # Use the keys of the first record as fields
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

# Main execution
if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    
    # Fetch all records using zip code filtering
    all_records = fetch_records_by_zip_codes(url, ri_zip_codes_dict)
    
    # Save the complete dataset
    save_data(all_records, "RI_child_care_providers_complete")
    
    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\nExecution completed in {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Total unique records collected: {len(all_records)}")