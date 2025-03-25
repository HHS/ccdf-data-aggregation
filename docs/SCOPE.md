# ACF Tech Data Surge Team Project Scope Document

## Project Title
CCDF Service Provider Address Data Aggregation and Normalization

## Project Overview
Goal: Gather, aggregate, and normalize data about entities that receive Child Care and Development Fund (CCDF) funding through state block grants, with a focus on collecting business names and addresses.

The Administration for Children and Families (ACF) provides substantial funding to states through CCDF block grants. Due to the nature of block grants, states have flexibility in how they distribute these funds to childcare providers, resulting in limited visibility for ACF regarding the end recipients of funding. This project aims to address this gap by collecting data on CCDF-funded childcare providers across all 50 states, DC, and U.S. territories, using an approach that puts no burden of time on grant recipients.

This information will serve dual purposes:
1. Enhance accountability by improving visibility into where CCDF funds are ultimately distributed
2. Support disaster response planning by identifying childcare resources in potential disaster areas, helping to prevent the creation of "childcare deserts" during emergency situations

## Objectives
**Phase 1**  

1. Assess data availability across state CCDF systems  
    a. Review each state's CCDF plan website and related resources  
    b. Identify states with accessible data and those requiring alternative approaches  
    c. Document data formats, accessibility methods, and completeness for each state  

**Phase 2: depending on results from Phase 1...**    
 
1. Develop and implement data collection strategies   
    a. Create web scraping solutions for states with online data  
    b. Establish alternative collection methods for states with limited online presence   
    c. Standardize collection approaches where possible

2. Aggregate and normalize collected data  
    a. Create a unified data structure for provider information  
    b. Normalize address formats and other key data points using Smarty API  
    c. Implement data quality checks and validation

3. Develop visualization and distribution tools   
    a. Produce exportable datasets in standard formats  
    b. Document data dictionary and limitations

4. Establish a framework for periodic data updates   
    a. Document collection processes for repeatability  
    b. Recommend update frequency and maintenance approaches

## Scope and Approach
This project will focus on collecting business names and addresses of CCDF-funded childcare providers across all states and territories. The approach will vary by state based on data availability:

- **Web Data Collection:** For states with interactive maps or downloadable datasets, automated collection methods will be developed using Python-based web scraping tools.

- **Data Processing Pipeline:** Once collected, data will be processed through a standardized pipeline that will:
  - Clean and validate addresses and business names
  - Normalize data formats across different state sources
  - Geocode locations for mapping purposes
  - Identify and flag potential duplicates or errors

- **Visualization:** The processed data will be visualized through:
  - Summary statistics by state/region
  - Exportable datasets for further analysis

## Partnership Model
**Sprint syncs:** Held weekly throughout the project duration.

**Working sessions:** Held weekly with the Data Surge Team and other stakeholders as needed.

**Asynchronous clarifications:** An MS Teams channel will be established with the members of the Data Surge Team and other relevant stakeholders. Teams will be used for informal communication. Email will be used for more formal communication and deliverables.

## Deliverables
- **Data Availability Assessment:** Documentation of data availability and access methods for all states/territories
- **Collection Code Repository:** Python-based tools for data collection and processing
- **Aggregated Dataset:** Comprehensive CSV file containing normalized provider data
- **Documentation:** Technical documentation detailing the collection methods, data structure, and update processes
- **Update Framework:** Recommendations for maintaining data currency, including suggested frequency and methods

## Timeline
These timelines represent initial plans. Tasks may adjust based on findings from earlier weeks.

### Financial Data
- **Phase 1 - Sprint 0: March 17-28, 2025**
  - Complete initial assessment of data availability across all state CCDF plans
  - Categorize states by data accessibility
  - Begin developing collection strategies for states with readily accessible data
  - Initial project sync with stakeholders

- **Phase 2 - Sprint 1: March 31-April 11, 2025**
  - Complete data collection from states with accessible online data
  - Begin data normalization and cleaning
  - Develop initial data structure for aggregated dataset
  - Begin outreach to states with limited online data

- **Sprint 2: April 14-25, 2025**
  - Continue data collection from remaining states
  - Implement data validation and quality checks
  - Begin development of visualization tools
  - Document collection methods and challenges

- **Sprint 3: April 28-May 1, 2025**
  - Finalize data collection and aggregation
  - Complete visualization tools
  - Document data limitations and gaps
  - Develop recommendations for ongoing data maintenance
  - Final project review with stakeholders

## Assumptions
- State CCDF plans and related websites will remain accessible during the project period
- Most states have some form of provider data available, though the format and accessibility may vary
- Python and related data processing tools will be sufficient for the technical requirements
- The project scope is limited to data collection and organization

## Roles
- Government Lead: Jane Yang
- Project Owner:
  - Phase 1 - Jane Yang
  - Phase 2 - TBD OHSEPR (Jane Yang to do outreach)
- Project Lead: Daina Bouquin
- Project Team:
  - When appropriate we will contact the Office of Human Services Emergency Preparedness and Response (OHSEPR) and the Office of Child Care (OCC) 

