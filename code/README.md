# Code Directory

This directory contains scripts designed to collect and process data on licensed childcare providers across various U.S. states and territories where direct file downloads were not possible.

## Structure

- **State-Specific Scripts:** Each Python script corresponds to a specific state or territory and is responsible for data collection and processing for that region. The naming convention follows the pattern: `[StateAbbreviation]_[function].py`. For example:
  - `GA_api_scrape_childcare.py`: Handles API scraping for childcare data in Georgia.
  - `KS_html_parse.py`: Parses HTML data for Kansas.
  - `RI_build_child_care_urls.py`: Builds URLs for childcare data in Rhode Island.

- **Utilities Folder:** Contains helper functions and modules that support data collection.

## Dependencies

See [requirements.txt](https://github.com/HHS/ccdf-data-aggregation/blob/main/requirements.txt) and ensure that these packages are installed before running the scripts.

## Usage

1. **Configuration:** Before executing any script, configure file paths to match your local envirnoment.

2. **Execution:** Run the desired script using Python:
   ```bash
   python [script_name].py
