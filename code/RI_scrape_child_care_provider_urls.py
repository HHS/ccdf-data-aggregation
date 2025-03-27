import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

def extract_info_from_URL(URL):
    try:
        # 1 second delay
        time.sleep(1)
        
        print(f"\nProcessing URL: {URL}")
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract information using the specified labels
        info = {}
        
        # For ProviderName handle the special case where it's in a label with class "label-txn"
        provider_name_label = soup.find('label', {'for': 'ProviderName', 'class': 'label-txn'})
        info['ProviderName'] = provider_name_label.text.strip() if provider_name_label else ''
        
        # For other fields find them by their 'for' attribute
        for field in ['ProviderFullAddress', 'ProviderTelephone']:
            label = soup.find('label', {'for': field})
            if label:
                value = label.text.strip()
                print(f"\nFound {field}: {value}")
            else:
                print(f"\nNo label found for {field}")
                value = ''
            info[field] = value
        
        # Special handling for LicenseExpires - the date is in the next label
        license_label = soup.find('label', {'for': 'LicenseExpires'})
        if license_label:
            # Find the next label in the same row
            next_label = license_label.find_next('label')
            if next_label:
                info['LicenseExpires'] = next_label.text.strip()
                print(f"\nFound LicenseExpires: {info['LicenseExpires']}")
            else:
                info['LicenseExpires'] = ''
                print("\nNo date found for LicenseExpires")
        else:
            info['LicenseExpires'] = ''
            print("\nNo label found for LicenseExpires")
            
        return info
    except Exception as e:
        print(f"Error processing URL {URL}: {str(e)}")
        return {
            'ProviderName': '',
            'ProviderFullAddress': '',
            'ProviderTelephone': '',
            'LicenseExpires': ''
        }

def main():
    # Read the input CSV file
    input_file = Path('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/RI_child_care_providers_complete_with_URLs_20250327.csv')
    df = pd.read_csv(input_file)
    
    # Create a new DataFrame to store the scraped information
    scraped_data = []
    
    # Process each URL
    for index, row in df.iterrows():
        if pd.notna(row['URL']):  # Check if URL exists
            print(f"Processing URL {index + 1}/{len(df)}")
            info = extract_info_from_URL(row['URL'])
            info['original_URL'] = row['URL']
            scraped_data.append(info)
    
    # Create a new DataFrame with the scraped information
    scraped_df = pd.DataFrame(scraped_data)
    
    # Save the results to a new CSV file
    output_file = Path('data/intermediate/RI_child_care_providers_20250327.csv')
    scraped_df.to_csv(output_file, index=False)
    print(f"Scraped information saved to {output_file}")

if __name__ == "__main__":
    main() 