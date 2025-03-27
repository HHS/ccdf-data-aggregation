import pandas as pd

# read in RI child care providers complete csv
ri_child_care_providers_complete = pd.read_csv('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/RI_child_care_providers_complete_20250327.csv')

# create a new column for the URL
ri_child_care_providers_complete['URL'] = 'https://earlylearningprograms.dhs.ri.gov/Provider/ViewProviderInfo?ProviderId=' + ri_child_care_providers_complete['ProviderId'].astype(str)

# save to csv
ri_child_care_providers_complete.to_csv('/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/RI_child_care_providers_complete_with_urls_20250327.csv', index=False)


