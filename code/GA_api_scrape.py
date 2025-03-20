#%%
import requests
import json
import csv
from datetime import datetime

#%%
# API endpoint from the network request
url = "https://families.decal.ga.gov/api/provider/searchByAddress"

#%%
# Define the parameters you saw in the network request (empty for no filters)
params = {
    'providerNumber': '',
    'name': '',
    'zipCode': '',
    'qrOnly': '',
    'programType': '',
    'latitudeLongitude': '|',
    'radiusAroundAddress': '',
    'servicesProvided': '',
    'transportation': '',
    'otherChildCareType': '',
    'specialHours': '',
    'acceptingChildrenType': '',
    'campCare': '',
    'meals': '',
    'financialInfo': '',
    'minimumFullDayRate': '',
    'registrationFee': '',
    'activityFee': '',
    'daysOfOperation': '',
    'openTime': '',
    'closeTime': '',
    'preKSlots': '',
    'minAge': '',
    'maxAge': '',
    'languages': '',
    'environment': '',
    'activities': ''
}

#%%
# Send GET request to API
response = requests.get(url, params=params)

#%%
# get date for file name
date = datetime.now().strftime("%Y%m%d")

#%%
# Check if the response is successful
if response.status_code == 200:
    print("Response content type:", response.headers.get('content-type'))
    
    try:
        # First parse gets us the string containing the JSON array
        json_string = response.json()
        print("\nFirst parse type:", type(json_string))
        
        # Second parse gets us the actual array
        data = json.loads(json_string)
        print("Second parse type:", type(data))
        
        # Save the data to a JSON file
        with open(f'GA_child_care_providers_{date}.json', 'w') as f:
            json.dump(data, f)
            
        # Only try to write CSV if data is a list
        if isinstance(data, list) and len(data) > 0:
            with open(f'GA_child_care_providers_{date}.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(data[0].keys())  # Write the header
                for row in data:
                    writer.writerow(row.values())
        else:
            print("Data is not in the expected list format for CSV conversion")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
else:
    print(f"Request failed with status code {response.status_code}")

