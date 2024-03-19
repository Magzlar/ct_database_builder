import logging
from utils.api import ClinicalTrial
from utils.data_processing import DataProcessing
import sqlite3

# configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # set params for API request
    disease_area = 'COVID-19'
    parameters = {'query.params': disease_area, 'min_rnk': 1, 'max_rnk': 50, 'format': 'json'}
    industry_only = False
    already_completed = False

    # make an instance of ClinicalTrial class and fetch the studie
    ct_api = ClinicalTrial(disease_area, parameters, industry_only, already_completed)
    studies = ct_api.fetch_studies()

    if not studies:
        logger.error("no studies were fetched from the API")
        return

    # process the data cleaning, formating and feature engineering for SQL sotrage
    processor = DataProcessing()
    processor.process_studies(studies)

    # connect to anSQLite database or create in  the first instance
    conn = sqlite3.connect('clinical_trials.db')
    cursor = conn.cursor()

    # make the studies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS studies (
        nct_id TEXT PRIMARY KEY,
        company TEXT,
        sponsor_type TEXT,
        enrollment_count INTEGER,
        status TEXT
    )
    ''')

    # iterate through datq and insert each study into the database
    for nct_id, study_info in processor.studies.items():
        try:
            cursor.execute('''
            INSERT INTO studies (nct_id, company, sponsor_type, enrollment_count, status) 
            VALUES (?, ?, ?, ?, ?)
            ''', (nct_id, study_info['company'], study_info['sponsor_type'], study_info['enrollment_count'], study_info['status']))
        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to insert {nct_id}: {e}")

    # commit the changes and close the database connection
    conn.commit()
    conn.close()
    logger.info("All studies have been succesfully stored in the database.")

if __name__ == "__main__":
    main()
