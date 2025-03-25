import tabula
import pandas as pd
import os

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
        df.to_csv(output_path, index=False)
        print(f"DataFrame saved to {output_path}")
    
    return df

if __name__ == "__main__":
    # Example usage
    pdf_path = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/raw/NC_test.pdf"  
    output_path = "/Users/dainabouquin/Library/CloudStorage/OneDrive-ArchSystems/CCDF/data/intermediate/NC_test.csv"  
    
    df = extract_table_from_pdf(pdf_path, output_path)
    print("\nFirst few rows of the extracted table:")
    print(df.head()) 