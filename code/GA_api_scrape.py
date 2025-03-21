#%%
import requests
import json
import csv
from datetime import datetime
import time

#%%
# API endpoint from the network request
url = "https://families.decal.ga.gov/api/provider/searchByAddress"

#%%
# Define the parameters seen in the network request (empty for no filters)
base_params = {
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
# Complete list of Georgia zip codes
ga_zip_codes = [
    '30002', '30004', '30005', '30008', '30009', '30011', '30012', '30013', '30014', '30016',
    '30017', '30018', '30019', '30021', '30022', '30024', '30025', '30028', '30030', '30032',
    '30033', '30034', '30035', '30038', '30039', '30040', '30041', '30043', '30044', '30045',
    '30046', '30047', '30052', '30054', '30055', '30056', '30058', '30060', '30062', '30064',
    '30066', '30067', '30068', '30070', '30071', '30072', '30075', '30076', '30078', '30079',
    '30080', '30082', '30083', '30084', '30087', '30088', '30090', '30092', '30093', '30094',
    '30096', '30097', '30101', '30102', '30103', '30104', '30105', '30106', '30107', '30108',
    '30110', '30111', '30113', '30114', '30115', '30116', '30117', '30118', '30120', '30121',
    '30122', '30124', '30125', '30126', '30127', '30132', '30134', '30135', '30137', '30139',
    '30141', '30143', '30144', '30145', '30147', '30148', '30149', '30152', '30153', '30157',
    '30161', '30165', '30168', '30170', '30171', '30173', '30175', '30176', '30177', '30178',
    '30179', '30180', '30182', '30183', '30184', '30185', '30187', '30188', '30189', '30204',
    '30205', '30206', '30213', '30214', '30215', '30216', '30217', '30218', '30220', '30222',
    '30223', '30224', '30228', '30229', '30230', '30233', '30234', '30236', '30238', '30240',
    '30241', '30248', '30250', '30251', '30252', '30253', '30256', '30257', '30258', '30259',
    '30260', '30263', '30265', '30268', '30269', '30272', '30273', '30274', '30275', '30276',
    '30277', '30281', '30284', '30285', '30286', '30288', '30289', '30290', '30291', '30292',
    '30293', '30294', '30295', '30296', '30297', '30303', '30305', '30306', '30307', '30308',
    '30309', '30310', '30311', '30312', '30313', '30314', '30315', '30316', '30317', '30318',
    '30319', '30322', '30324', '30326', '30327', '30328', '30329', '30331', '30332', '30334',
    '30336', '30337', '30338', '30339', '30340', '30341', '30342', '30344', '30345', '30346',
    '30349', '30350', '30354', '30360', '30363', '30401', '30410', '30411', '30412', '30413',
    '30414', '30415', '30417', '30420', '30421', '30423', '30425', '30426', '30427', '30428',
    '30429', '30434', '30436', '30439', '30441', '30442', '30445', '30446', '30448', '30449',
    '30450', '30451', '30452', '30453', '30454', '30455', '30456', '30457', '30458', '30460',
    '30461', '30464', '30467', '30470', '30471', '30473', '30474', '30477', '30501', '30504',
    '30506', '30507', '30510', '30511', '30512', '30513', '30516', '30517', '30518', '30519',
    '30520', '30521', '30522', '30523', '30525', '30527', '30528', '30529', '30530', '30531',
    '30533', '30534', '30535', '30536', '30537', '30538', '30539', '30540', '30541', '30542',
    '30543', '30545', '30546', '30547', '30548', '30549', '30552', '30553', '30554', '30555',
    '30557', '30558', '30559', '30560', '30562', '30563', '30564', '30565', '30566', '30567',
    '30568', '30571', '30572', '30573', '30575', '30576', '30577', '30581', '30582', '30597',
    '30598', '30601', '30602', '30605', '30606', '30607', '30609', '30619', '30620', '30621',
    '30622', '30623', '30624', '30625', '30627', '30628', '30629', '30630', '30631', '30633',
    '30634', '30635', '30639', '30641', '30642', '30643', '30646', '30648', '30650', '30655',
    '30656', '30660', '30662', '30663', '30664', '30665', '30666', '30667', '30668', '30669',
    '30673', '30677', '30678', '30680', '30683', '30701', '30705', '30707', '30708', '30710',
    '30711', '30720', '30721', '30724', '30725', '30726', '30728', '30730', '30731', '30733',
    '30734', '30735', '30736', '30738', '30739', '30740', '30741', '30742', '30746', '30747',
    '30750', '30751', '30752', '30753', '30755', '30756', '30757', '30802', '30803', '30805',
    '30807', '30808', '30809', '30810', '30812', '30813', '30814', '30815', '30816', '30817',
    '30818', '30820', '30821', '30822', '30823', '30824', '30828', '30830', '30833', '30901',
    '30904', '30905', '30906', '30907', '30909', '30912', '31001', '31002', '31003', '31004',
    '31005', '31006', '31007', '31008', '31009', '31011', '31012', '31014', '31015', '31016',
    '31017', '31018', '31019', '31020', '31021', '31022', '31023', '31024', '31025', '31027',
    '31028', '31029', '31030', '31031', '31032', '31033', '31034', '31035', '31036', '31037',
    '31038', '31039', '31041', '31042', '31044', '31045', '31046', '31047', '31049', '31050',
    '31051', '31052', '31054', '31055', '31057', '31058', '31060', '31061', '31062', '31063',
    '31064', '31065', '31066', '31067', '31068', '31069', '31070', '31071', '31072', '31075',
    '31076', '31077', '31078', '31079', '31081', '31082', '31083', '31085', '31087', '31088',
    '31089', '31090', '31091', '31092', '31093', '31094', '31096', '31097', '31098', '31201',
    '31204', '31206', '31207', '31210', '31211', '31213', '31216', '31217', '31220', '31301',
    '31302', '31303', '31305', '31307', '31308', '31309', '31312', '31313', '31314', '31315',
    '31316', '31318', '31320', '31321', '31322', '31323', '31324', '31326', '31327', '31328',
    '31329', '31331', '31333', '31401', '31404', '31405', '31406', '31407', '31408', '31409',
    '31410', '31411', '31415', '31419', '31421', '31501', '31503', '31510', '31512', '31513',
    '31516', '31518', '31519', '31520', '31522', '31523', '31524', '31525', '31527', '31532',
    '31533', '31535', '31537', '31539', '31542', '31543', '31544', '31545', '31546', '31547',
    '31548', '31549', '31550', '31551', '31552', '31553', '31554', '31555', '31556', '31557',
    '31558', '31560', '31561', '31562', '31563', '31564', '31565', '31566', '31567', '31568',
    '31569', '31599', '31601', '31602', '31605', '31606', '31620', '31622', '31623', '31624',
    '31625', '31626', '31627', '31629', '31630', '31631', '31632', '31634', '31635', '31636',
    '31637', '31638', '31639', '31641', '31642', '31643', '31645', '31647', '31648', '31649',
    '31650', '31698', '31699', '31701', '31704', '31705', '31707', '31709', '31711', '31712',
    '31714', '31716', '31719', '31720', '31721', '31722', '31727', '31730', '31733', '31735',
    '31738', '31743', '31744', '31747', '31749', '31750', '31753', '31756', '31757', '31763',
    '31764', '31765', '31768', '31771', '31772', '31773', '31774', '31775', '31778', '31779',
    '31780', '31781', '31783', '31784', '31787', '31788', '31789', '31790', '31791', '31792',
    '31793', '31794', '31795', '31796', '31798', '31801', '31803', '31804', '31805', '31806',
    '31807', '31808', '31810', '31811', '31812', '31814', '31815', '31816', '31820', '31821',
    '31822', '31823', '31824', '31825', '31826', '31827', '31829', '31830', '31831', '31832',
    '31833', '31836', '31901', '31903', '31904', '31905', '31906', '31907', '31909', '39813',
    '39815', '39817', '39819', '39823', '39824', '39825', '39826', '39827', '39828', '39832',
    '39834', '39836', '39837', '39840', '39841', '39842', '39845', '39846', '39851', '39854',
    '39859', '39861', '39862', '39866', '39867', '39870', '39877', '39885', '39886', '39897'
]

#%%
# Function to fetch all records using zip code filtering
def fetch_records_by_zip_codes(base_url, base_params, zip_codes):
    """
    Fetches records from the API using zip code filtering.
    
    Args:
        base_url (str): The API endpoint URL
        base_params (dict): The base parameters for the API request
        zip_codes (list): List of zip codes to query
        
    Returns:
        list: All unique records from all zip codes combined
    """
    all_data = []
    seen_ids = set()
    total_zip_codes = len(zip_codes)
    
    print(f"Starting to fetch data for {total_zip_codes} zip codes...")
    
    # Create progress tracker
    progress_intervals = [int(total_zip_codes * p) for p in [0.25, 0.5, 0.75, 1.0]]
    
    for idx, zip_code in enumerate(zip_codes, 1):
        print(f"Fetching data for zip code {zip_code} ({idx}/{total_zip_codes})...")
        
        # Update parameters with current zip code
        current_params = base_params.copy()
        current_params['zipCode'] = zip_code
        
        # Send request
        try:
            response = requests.get(base_url, params=current_params)
            
            if response.status_code == 200:
                try:
                    # First parse gets the string containing the JSON array
                    json_string = response.json()
                    
                    # Second parse gets the actual array
                    data = json.loads(json_string)
                    
                    # Check if we received any data
                    if isinstance(data, list):
                        new_records = 0
                        for record in data:
                            # Use an appropriate identifier field
                            if 'id' in record:
                                record_id = record['id']
                            elif 'providerId' in record:
                                record_id = record['providerId']
                            elif 'providerNumber' in record:
                                record_id = record['providerNumber']
                            else:
                                # Create a unique identifier from the whole record
                                record_id = str(record)
                            
                            if record_id not in seen_ids:
                                seen_ids.add(record_id)
                                all_data.append(record)
                                new_records += 1
                        
                        print(f"Received {len(data)} records, added {new_records} new unique records")
                        
                        # Save progress after each 50 zip codes or when we've processed 25%, 50%, 75%, and 100%
                        if idx % 50 == 0 or idx in progress_intervals:
                            # Get date for file name
                            date = datetime.now().strftime("%Y%m%d")
                            
                            # Save intermediate progress
                            progress_file = f'GA_child_care_providers_progress_{idx}_of_{total_zip_codes}_{date}.json'
                            with open(progress_file, 'w') as f:
                                json.dump(all_data, f)
                            print(f"Saved progress: {len(all_data)} records to {progress_file}")
                    else:
                        print(f"No data or invalid data format received for zip code {zip_code}")
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for zip code {zip_code}: {e}")
            else:
                print(f"Request failed with status code {response.status_code} for zip code {zip_code}")
                
        except Exception as e:
            print(f"Exception occurred while fetching data for zip code {zip_code}: {e}")
            
        # Add a small delay to avoid overwhelming the API
        time.sleep(1)
        
        # Print progress
        if idx in progress_intervals:
            print(f"Progress: {idx}/{total_zip_codes} zip codes processed ({int(idx/total_zip_codes*100)}%)")
    
    print(f"Completed fetching data for all zip codes. Total unique records: {len(all_data)}")
    return all_data

#%%
# Function to save data to files
def save_data(data, file_prefix):
    """
    Save data to JSON and CSV files
    
    Args:
        data (list): The data to save
        file_prefix (str): Prefix for the filenames
    """
    # Get date for file name
    date = datetime.now().strftime("%Y%m%d")
    
    # Save the data to a JSON file
    json_filename = f'{file_prefix}_{date}.json'
    with open(json_filename, 'w') as f:
        json.dump(data, f)
    print(f"Saved JSON file with {len(data)} records to {json_filename}")

    # Save the data to a CSV file
    if isinstance(data, list) and len(data) > 0:
        csv_filename = f'{file_prefix}_{date}.csv'
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data[0].keys())  # Write the header
            for row in data:
                writer.writerow(row.values())
        print(f"Saved CSV file with {len(data)} records to {csv_filename}")
    else:
        print("No data to save to CSV")

#%%
# Main execution
if __name__ == "__main__":
    # Record start time
    start_time = time.time()
    
    # Fetch all records using zip code filtering
    all_records = fetch_records_by_zip_codes(url, base_params, ga_zip_codes)
    
    # Save the complete dataset
    save_data(all_records, "GA_child_care_providers_complete")
    
    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\nExecution completed in {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Total unique records collected: {len(all_records)}")