#%%
import requests
import json
import csv
from datetime import datetime
import time
import pandas as pd

#%%
# API endpoint from the network request
url = "https://www.nechildcarereferral.org/api/childcare/filter"

#%%
# Function to fetch all records in a single request (pagination is avoided with PageSize=0) 
def fetch_all_records(base_url):
    """
    Fetches all records from the Nebraska childcare API in a single request.
    
    Args:
        base_url (str): The API endpoint URL
        
    Returns:
        list: All unique records
    """
    all_data = []
    seen_ids = set()
    
    # Using PageSize=0 to get all records in a single request
    params = {
        'PageSize': 0,
        'PageNumber': 1,
        'OpenAccept': True,
        'OpenNotAccept': False,
        'Closed': False,
        'Infant': False,
        'Toddler': False,
        'Preschool': False,
        'SchoolAge': False,
        'ProviderType': '1,2,3,4,5,6,7,8,9,10'  # All provider types
    }
    
    print("Starting to fetch records from Nebraska childcare API...")
    
    try:
        # Send request
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            try:
                # Parse JSON response
                data = response.json()
                
                # Check if we received any data
                if isinstance(data, list) and len(data) > 0:
                    for record in data:
                        # Use provider ID as unique identifier
                        record_id = record.get('id')
                        
                        if record_id not in seen_ids:
                            seen_ids.add(record_id)
                            all_data.append(record)
                    
                    print(f"Received {len(data)} records, added {len(all_data)} unique records")
                else:
                    print("No data received or empty response.")
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
        else:
            print(f"Request failed with status code {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred while fetching data: {e}")
    
    print(f"Completed fetching data. Total unique records: {len(all_data)}")
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
            # Get all possible fields from the first record
            fields = list(data[0].keys())
            
            # Check for nested objects and add their fields
            nested_fields = []
            for key, value in data[0].items():
                if isinstance(value, dict) and value is not None:
                    for nested_key in value.keys():
                        nested_fields.append(f"{key}_{nested_key}")
            
            writer = csv.writer(f)
            writer.writerow(fields + nested_fields)  # Write the header with both top-level and nested fields
            
            for row in data:
                # Get values for top-level fields
                values = []
                for field in fields:
                    value = row.get(field, '')
                    
                    # Skip nested objects for now, handle them separately
                    if not isinstance(value, dict) and not isinstance(value, list):
                        values.append(value)
                    else:
                        # Convert complex non-dict objects to strings
                        if not isinstance(value, dict):
                            values.append(json.dumps(value) if value is not None else '')
                        else:
                            values.append('')  # Placeholder for dict fields
                
                # Add values from nested objects
                for key, value in row.items():
                    if isinstance(value, dict) and value is not None:
                        for nested_key, nested_value in value.items():
                            if not isinstance(nested_value, dict) and not isinstance(nested_value, list):
                                values.append(nested_value)
                            else:
                                values.append(json.dumps(nested_value) if nested_value is not None else '')
                
                writer.writerow(values)
                
        print(f"Saved CSV file with {len(data)} records to {csv_filename}")
    else:
        print("No data to save to CSV")

#%%
# Main execution
if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    
    # Fetch all records
    all_records = fetch_all_records(url)
    
    # Save the complete dataset
    save_data(all_records, "NE_child_care_providers_complete")
    
    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\nExecution completed in {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Total unique records collected: {len(all_records)}")