import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime   

def scrape_provider_urls(url):
    try:
        # Send a GET request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links that contain "View Provider Details"
        provider_links = []
        for link in soup.find_all('a', href=True):
            if link.text.strip() == "View Provider Details":
                provider_url = link['href']
                provider_links.append(provider_url)
        
        return provider_links
    
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def main():
    # Get URL for Oklahoma child care providers
    url = "https://ccl.dhs.ok.gov/providers"
    
    # Scrape the provider URLs
    provider_urls = scrape_provider_urls(url)
    
    # Print results
    if provider_urls:
        print("\nFound provider URLs:")
        for url in provider_urls:
            print(url)
        print(f"\nTotal providers found: {len(provider_urls)}")

        #append found string to base URL https://ccl.dhs.ok.gov/
        provider_urls = [f"https://ccl.dhs.ok.gov{url}" for url in provider_urls]

        # Get date for file name
        date = datetime.now().strftime("%Y%m%d")

        # save to csv
        df = pd.DataFrame({'URL': provider_urls})
        df.to_csv(f'OK_child_care_provider_urls_{date}.csv', index=False)
    else:
        print("No provider URLs found or an error occurred.")

if __name__ == "__main__":
    main() 