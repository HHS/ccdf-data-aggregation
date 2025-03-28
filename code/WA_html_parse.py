import pandas as pd
from bs4 import BeautifulSoup
import csv
from pathlib import Path

def extract_provider_info(html_file):
    providers = []
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Find all provider sections
        provider_sections = soup.find_all('div', class_='panel pane-default result-panel')
        
        for section in provider_sections:
            provider_info = {}
            
            # Extract provider name from h1 within a tag
            name_tag = section.find('a', href=True).find('h1')
            if name_tag:
                provider_info['name'] = name_tag.text.strip()
            
            # Find the div containing address and contact info
            info_div = section.find('div', class_='col-xs-12', style='display:block;')
            if info_div:
                # Extract address from first p tag
                address_tag = info_div.find('p')
                if address_tag:
                    # Get the text content and replace <br> with a space
                    address_text = address_tag.get_text(separator=' ', strip=True)
                    provider_info['address'] = address_text
                
                # Extract phone and email from second p tag
                contact_tag = address_tag.find_next('p')
                if contact_tag:
                    contact_text = contact_tag.text.strip()
                    # Split by " / " to separate phone and email
                    parts = contact_text.split(' / ')
                    if len(parts) >= 2:
                        provider_info['phone'] = parts[0].strip()
                        provider_info['email'] = parts[1].strip()
            
            if provider_info:
                providers.append(provider_info)
    
    return providers

def main():
    # Define input and output paths
    input_file = Path('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/WA_child_care_providers_20250328.html')
    output_file = Path('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/WA_child_care_providers_20250328.csv')
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract provider information
    print("Extracting provider information...")
    providers = extract_provider_info(input_file)
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(providers)
    df.to_csv(output_file, index=False)
    print(f"Successfully extracted {len(providers)} providers to {output_file}")

if __name__ == "__main__":
    main() 