import pandas as pd
from bs4 import BeautifulSoup
import os
from datetime import datetime
def extract_center_data():
    # Read the HTML file
    with open('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/WV_html_source_all_child_care_providers.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table
    table = soup.find('table', {'id': 'center_table'})
    
    # Initialize lists to store data
    centers = []
    
    # Extract data from each row
    for row in table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) >= 6:  # Ensure row has enough columns
            # Extract center name and URL from the link
            center_link = cols[0].find('a')
            center_name = center_link.text.strip() if center_link else ''
            url = center_link.get('href', '') if center_link else ''
            
            # Extract other data
            city = cols[1].text.strip()
            postal = cols[2].text.strip()
            county = cols[3].text.strip()
            phone = cols[4].text.strip()
            contact = cols[5].text.strip()
            
            # Add to list
            centers.append({
                'Center Name': center_name,
                'URL': url,
                'City': city,
                'Postal Code': postal,
                'County': county,
                'Phone': phone,
                'Contact': contact
            })
    
    # Create DataFrame
    df = pd.DataFrame(centers)
    
    # Create output directory if it doesn't exist
    os.makedirs('data/intermediate', exist_ok=True)
    
    # get date for filename
    date = datetime.now().strftime("%Y%m%d")

    # Save to CSV
    output_file = f'data/intermediate/WV_child_care_providers_{date}.csv'
    df.to_csv(output_file, index=False)
    print(f"Data has been extracted and saved to {output_file}")

if __name__ == "__main__":
    extract_center_data() 