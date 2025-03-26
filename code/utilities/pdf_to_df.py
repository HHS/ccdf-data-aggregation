import tabula
import pandas as pd
import os
import glob

def extract_table_from_pdf(pdf_path, output_path=None):
    """
    Extract table from a PDF file and convert it to a pandas DataFrame.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path to save the DataFrame as CSV. If None, returns DataFrame only.
    
    Returns:
        pandas.DataFrame: The extracted table as a DataFrame
    """
    # Read all tables from the PDF
    # The pages parameter can be adjusted based on your PDF
    # 'all' means all pages, or you can specify a list of page numbers
    dfs = tabula.read_pdf(
        pdf_path,
        pages='all',
        multiple_tables=False  # Set to True if your PDF has multiple tables
    )
    
    # If multiple tables were found, concatenate them
    if len(dfs) > 1:
        df = pd.concat(dfs, ignore_index=True)
    else:
        df = dfs[0]
    
    # Clean the DataFrame
    # Remove any completely empty rows
    df = df.dropna(how='all')
    # Reset the index
    df = df.reset_index(drop=True)
    
    # Save to CSV if output path is provided
    if output_path:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"DataFrame saved to {output_path}")
    
    return df

if __name__ == "__main__":
    # Define input and output directories
    input_dir = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/NC_child_care_providers"
    output_dir = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/NC_child_care_providers"
    
    # Get all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    # Process each PDF file
    for pdf_path in pdf_files:
        # Get the filename without extension
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Create output path
        output_path = os.path.join(output_dir, f"{base_name}.csv")
        
        print(f"\nProcessing: {pdf_path}")
        try:
            df = extract_table_from_pdf(pdf_path, output_path)
            print(f"Successfully processed {pdf_path}")
            print("\nFirst few rows of the extracted table:")
            print(df.head())
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}") 