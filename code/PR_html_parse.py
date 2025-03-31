import pandas as pd
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Read the HTML file
with open('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/PR_html_source_all_child_care_providers_20250331.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize lists to store provider information
providers = []

# Find all provider cards
provider_cards = soup.find_all('div', class_='card')

for card in provider_cards:
    provider_info = {}
    
    # Extract provider name from h4 tag
    name_tag = card.find('h4')
    if name_tag:
        provider_info['provider_name'] = name_tag.text.strip()
    
    # Extract phone number
    phone_icon = card.find('i', class_='fas fa-phone')
    if phone_icon:
        phone_span = phone_icon.find_next('span')
        if phone_span:
            provider_info['phone'] = phone_span.text.strip()
    
    # Extract address
    address_icon = card.find('i', class_='fas fa-map-marker-alt')
    if address_icon:
        address_span = address_icon.find_next('span')
        if address_span:
            provider_info['address'] = address_span.text.strip()
    
    # Extract coordinates
    map_link = card.find('a', class_='ver-mapa-link')
    if map_link:
        provider_info['latitude'] = map_link.get('data-latitud')
        provider_info['longitude'] = map_link.get('data-longitud')
    
    
    # Extract monitoring report links
    report_links = card.find_all('a', class_='btn')
    monitoring_reports = []
    for link in report_links:
        if 'Informe de Monitoria' in link.text:
            monitoring_reports.append({
                'year': link.text.split()[-1],
                'url': link.get('href')
            })
    provider_info['monitoring_reports'] = monitoring_reports
    
    providers.append(provider_info)

# Create DataFrame
df = pd.DataFrame(providers)

# get date for filename
date = datetime.now().strftime("%Y%m%d")

# Save to CSV
output_file = f'data/intermediate/PR_child_care_providers_{date}.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)

print(f"Extracted information for {len(providers)} providers")
print(f"Data saved to {output_file}")

