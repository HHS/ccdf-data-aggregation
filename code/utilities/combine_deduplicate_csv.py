import os
import pandas as pd
import glob
from datetime import datetime

def combine_and_deduplicate_csv(directory_path):
    """
    Combines all CSV files in the specified directory and removes duplicate rows.
    
    Parameters:
    directory_path (str): Path to the directory containing CSV files
    
    Returns:
    pandas.DataFrame: A combined dataframe with duplicates removed
    """
    # Use glob to get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {directory_path}")
        return None
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Create a list to store all dataframes
    all_dataframes = []
    
    # Read each CSV file and append to the list
    for file in csv_files:
        try:
            # Read the CSV file  
            df = pd.read_csv(file)
            print(f"Read {file}, shape: {df.shape}")

            # Append to the list
            all_dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if not all_dataframes:
        print("No data was successfully read from the CSV files")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_dataframes, ignore_index=False)
    print(f"Combined dataframe shape: {combined_df.shape}")
    
    # Remove duplicates
    deduplicated_df = combined_df.drop_duplicates()
    print(f"Deduplicated dataframe shape: {deduplicated_df.shape}")
    print(f"Removed {combined_df.shape[0] - deduplicated_df.shape[0]} duplicate rows")
    
    return deduplicated_df

def main():
    # Directory path containing CSV files
    directory_path = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/MA_child_care_providers"
    
    # Combine and deduplicate CSV files
    result_df = combine_and_deduplicate_csv(directory_path)

    # Get date
    date = datetime.now().strftime("%Y%m%d")
    
    if result_df is not None:
        # Save the result to a new CSV file
        output_path = os.path.join(os.path.dirname("/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/"), f"MA_child_care_providers_combined_deduplicated_{date}.csv")
        result_df.to_csv(output_path, index=False)
        print(f"Saved combined and deduplicated data to {output_path}")

if __name__ == "__main__":
    main()