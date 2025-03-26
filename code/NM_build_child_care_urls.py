#%%
import pandas as pd
import json
from datetime import datetime
#%%
# Read JSON file
with open('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/NM_child_care_ids_from_html.json', 'r') as file:
    json_data = json.load(file)

# Convert JSON data directly to DataFrame
df = pd.DataFrame(json_data)
#%%

# remove .0 from external_school_id and school_id
df['external_school_id'] = df['external_school_id'].astype(str).str.replace('.0', '')
df['school_id'] = df['school_id'].astype(str).str.replace('.0', '')

# Replace nan with empty string
df['external_school_id'] = df['external_school_id'].replace('nan', '')
df['school_id'] = df['school_id'].replace('nan', '')

# remove any whitespace from external_school_id and school_id
df['external_school_id'] = df['external_school_id'].str.strip()
df['school_id'] = df['school_id'].str.strip()
#%%
# Create column called URL where it's an empty string
df['URL'] = ''

#%%
# Fill with URL based on schoolType
def create_url(row):
    base_url = "https://childcare.ececd.nm.gov/-"
    
    if row['schoolType'] == 'internalAndExternal':
        # For internalAndExternal type, use school_id
        return f"{base_url}{row['school_id']}"
    else:
        # For other types, use external_school_id + 'u'
        return f"{base_url}{row['external_school_id']}u"

# Apply the function to create the URL column
df['URL'] = df.apply(create_url, axis=1)

#%%
#date for file
date = datetime.now().strftime("%Y%m%d")
# save to CSV
df.to_csv(f'/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/NM_school_urls_{date}.csv', index=False) 