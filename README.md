# ACF Tech Data Surge Team Project Scope Document

*Working Draft - Last Updated: March 18, 2025*

## Project Title
CCDF Data Aggregation and Normalization

## Project Overview
**Goal:** Gather, aggregate, and normalize data about entities that receive Child Care and Development Fund (CCDF) funding through state block grants, with a focus on collecting business names and addresses.

The Administration for Children and Families (ACF) provides substantial funding to states through CCDF block grants. Due to the nature of block grants, states have flexibility in how they distribute these funds to childcare providers, resulting in limited visibility for ACF regarding the end recipients of funding. This project aims to address this gap by collecting data on CCDF-funded childcare providers across all states and territories.

This information will serve dual purposes:
1. Enhance accountability by improving visibility into where CCDF funds are ultimately distributed
2. Support disaster response planning by identifying childcare resources in potential disaster areas, helping to prevent the creation of "childcare deserts" during emergency situations

## Objectives
1. Assess data availability across state CCDF systems
    - Review each state's CCDF plan website and related resources
    - Identify states with accessible data and those requiring alternative approaches
    - Document data formats, accessibility methods, and completeness for each state

2. Develop and implement data collection strategies
    - Create web scraping solutions for states with online data
    - Establish alternative collection methods for states with limited online presence
    - Standardize collection approaches where possible

3. Aggregate and normalize collected data
    - Create a unified data structure for provider information
    - Normalize address formats and other key data points
    - Implement data quality checks and validation

4. Develop visualization and distribution tools
    - Create an interactive map visualization of provider locations
    - Produce exportable datasets in standard formats
    - Document data dictionary and limitations

5. Establish a framework for periodic data updates
    - Document collection processes for repeatability
    - Recommend update frequency and maintenance approaches

## Scope and Approach
This project will focus on collecting business names and addresses of CCDF-funded childcare providers across all states and territories. The approach will vary by state based on data availability:

- **Web Data Collection:** For states with interactive maps or downloadable datasets, automated collection methods will be developed using Python-based web scraping tools.

- **Manual Research:** For states with limited online data, manual research and direct outreach may be necessary, though this will be limited in scope for the initial project phase.

- **Data Processing Pipeline:** Once collected, data will be processed through a standardized pipeline that will:
  - Clean and validate addresses and business names
  - Normalize data formats across different state sources
  - Geocode locations for mapping purposes
  - Identify and flag potential duplicates or errors

- **Visualization:** The processed data will be visualized through:
  - An interactive map showing provider locations
  - Summary statistics by state/region
  - Exportable datasets for further analysis

## Partnership Model
Sprint syncs: Held weekly throughout the project duration.

Working sessions: Held weekly with the Data Surge Team and other stakeholders as needed.

Asynchronous clarifications: An MS Teams channel will be established with the members of the Data Surge Team and other relevant stakeholders. Teams will be used for informal communication. Email will be used for more formal communication and deliverables.

## Deliverables
- **Data Availability Assessment:** Documentation of data availability and access methods for all states/territories
- **Collection Code Repository:** Python-based tools for data collection and processing
- **Aggregated Dataset:** Comprehensive CSV file containing normalized provider data
- **Interactive Map:** Visualization tool showing the distribution of CCDF-funded providers
- **Documentation:** Technical documentation detailing the collection methods, data structure, and update processes
- **Update Framework:** Recommendations for maintaining data currency, including suggested frequency and methods

## Timeline
These timelines represent initial plans. Tasks may adjust based on findings from earlier weeks.

- **Week 1: March 17-21, 2025**
  - Complete initial assessment of data availability across all state CCDF plans
  - Categorize states by data accessibility
  - Begin developing collection strategies for states with readily accessible data
  - Initial project sync with stakeholders

- **Week 2: March 24-28, 2025**
  - Complete data collection from states with accessible online data
  - Begin data normalization and cleaning
  - Develop initial data structure for aggregated dataset
  - Begin outreach to states with limited online data

- **Week 3: March 31-April 4, 2025**
  - Continue data collection from remaining states
  - Implement data validation and quality checks
  - Begin development of visualization tools
  - Document collection methods and challenges

- **Week 4: April 7-11, 2025**
  - Finalize data collection and aggregation
  - Complete interactive map and visualization tools
  - Document data limitations and gaps
  - Develop recommendations for ongoing data maintenance
  - Final project review with stakeholders

## Assumptions
- State CCDF plans and related websites will remain accessible during the project period
- Most states have some form of provider data available, though the format and accessibility may vary
- Python and related data processing tools will be sufficient for the technical requirements
- The project scope is limited to data collection and organization; policy recommendations are outside scope
- Initial development of visualization tools will use open-source technologies due to potential delays in Tableau access

## Roles
- **Project Lead:** Daina Bouquin, Lead Data Scientist III
- **Project Team:** 
  - Data Surge Team members
  - Additional support from OEP&R and Office of Childcare as needed

## Future Considerations
If this initial data collection effort proves valuable, potential follow-on work could include:
- Development of a public-facing dashboard
- Integration with disaster planning tools
- Expansion to include additional provider information beyond location data
- Establishment of automated data refresh processes
- Creation of APIs for programmatic data access
