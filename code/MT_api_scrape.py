import requests
import json
import csv
from datetime import datetime
import time
import pandas as pd

# API endpoint for Montana child care providers
url = "https://webapp.sanswrite.com/MontanaDPHHS/ChildCare/search-identifiers"

# Headers for the request
headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://webapp.sanswrite.com',
    'referer': 'https://webapp.sanswrite.com/MontanaDPHHS/ChildCare/?iframe',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def fetch_all_records(base_url, headers, results_per_page=50):
    """
    Fetches all records from the Montana API using pagination.
    
    Args:
        base_url (str): The API endpoint URL
        headers (dict): Headers for the request
        results_per_page (int): Number of results per page
        
    Returns:
        list: All records from all pages combined
    """
    all_data = []
    current_page = 1
    total_pages = None
    
    print(f"Starting to fetch data from Montana API...")
    
    while total_pages is None or current_page <= total_pages:
        print(f"Fetching page {current_page}...")
        
        # Prepare the request payload
        payload = {
            "searchPrams": {
                "columnQueryPairs": {
                    "number": "",
                    "name": "",
                    "city": "",
                    "state": "",
                    "zip": ""
                },
                "orderBy": "name",
                "ascending": True,
                "pageNumber": current_page,
                "resultsPerPage": results_per_page
            }
        }
        
        # Send the request
        try:
            response = requests.post(base_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                try:
                    # Parse JSON response
                    response_data = response.json()
                    
                    # Set total_pages if this is the first request
                    if total_pages is None:
                        total_rows = response_data.get('pagination', {}).get('totalRows', 0)
                        total_pages = response_data.get('pagination', {}).get('numberOfPages', 0)
                        print(f"Total records: {total_rows}, Total pages: {total_pages}")
                    
                    # Extract the data from the response
                    page_data = response_data.get('data', [])
                    all_data.extend(page_data)
                    
                    print(f"Received {len(page_data)} records from page {current_page}")
                    
                    # Save progress after every 5 pages
                    if current_page % 5 == 0:
                        date = datetime.now().strftime("%Y%m%d")
                        progress_file = f'MT_child_care_providers_progress_{current_page}_of_{total_pages}_{date}.json'
                        with open(progress_file, 'w') as f:
                            json.dump(all_data, f)
                        print(f"Saved progress: {len(all_data)} records to {progress_file}")
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON response: {e}")
                    break
            else:
                print(f"Request failed with status code {response.status_code}")
                break
                
        except Exception as e:
            print(f"Exception occurred while fetching data: {e}")
            break
        
        # Move to the next page
        current_page += 1
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(1)
    
    print(f"Completed fetching data. Total records: {len(all_data)}")
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
    
    # Fetch all records 
    all_records = fetch_all_records(url, headers)
    
    # Save the complete dataset
    save_data(all_records, "MT_child_care_providers_complete")
    
    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\nExecution completed in {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Total records collected: {len(all_records)}")