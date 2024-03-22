### Testing file ###

import requests

url = r"https://clinicaltrials.gov/api/v2/studies"
disease_area = 'Psoriatic arthritis'
fields = "Condition|InterventionType|NumPhases|EnrollmentCount|PrimaryOutcomeMeasure|PrimaryOutcomeTimeFrame|NumPrimaryOutcomes|OrgFullName|StartDate"
query_term = "AREA[StartDate]RANGE[2013-01,MAX]"
#parameters = {'query.cond': disease_area,"fields": fields,"query.term":query_term,"pageSize":100}
parameters = {'query.cond': disease_area,"fields": fields,"pageSize":100}


response = requests.get(url,params=parameters)
json = response.json()

for i in json["studies"]:
    try:
        print(i["protocolSection"]['statusModule']['startDateStruct']["date"])
    except KeyError:
        print("Dictionary key not found")




    # process the data cleaning, formating and feature engineering for SQL sotrage
    processor = DataProcessing()
    processor.process_studies(studies)

    # connect to anSQLite database or create in  the first instance
    # conn = sqlite3.connect('clinical_trials.db')
    # cursor = conn.cursor()

    # # make the studies table
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS studies (
    #     nct_id TEXT PRIMARY KEY,
    #     company TEXT,
    #     sponsor_type TEXT,
    #     enrollment_count INTEGER,
    #     status TEXT
    # )
    # ''')

    # # iterate through datq and insert each study into the database
    # for nct_id, study_info in processor.studies.items():
    #     try:
    #         cursor.execute('''
    #         INSERT INTO studies (nct_id, company, sponsor_type, enrollment_count, status) 
    #         VALUES (?, ?, ?, ?, ?)
    #         ''', (nct_id, study_info['company'], study_info['sponsor_type'], study_info['enrollment_count'], study_info['status']))
    #     except sqlite3.IntegrityError as e:
    #         logger.error(f"Failed to insert {nct_id}: {e}")

    # # commit the changes and close the database connection
    # conn.commit()
    # conn.close()
    # logger.info("All studies have been succesfully stored in the database.")