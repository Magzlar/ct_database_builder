import logging
from utils.api import ClinicalTrial
from utils.data_processing import DataProcessing
import pandas as pd

# configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # set params for API request
    disease_area = 'Psoriatic arthritis'
    fields = "Condition|Phase|EnrollmentCount|PrimaryOutcomeMeasure|PrimaryOutcomeTimeFrame|OrgFullName|StartDate|PrimaryCompletionDate|NCTId|LocationFacility|LocationCity|LocationCountry|OverallStatus|minimumAge|maximumAge"
    filter = "AREA[StartDate]RANGE[2013-01-01,MAX] AND AREA[Phase]PHASE2 OR PHASE3 AND AREA[OverallStatus]COMPLETED"
    parameters = {'query.cond': disease_area, 
                  "query.term":filter, 
                  "fields": fields,
                  'format': 'json',
                  "filter.overallStatus":"COMPLETED",
                  "pageSize":100}

    # make an instance of ClinicalTrial class and fetch the studies
    ct_api = ClinicalTrial(parameters)
    studies = ct_api.fetch_studies()

    if not studies:
        logger.error("no studies were fetched from the API")
        return
    
    # process the data cleaning, formating and feature engineering for SQL storage
    processor = DataProcessing(studies["studies"])
    studies_df = pd.DataFrame.from_dict(processor.processed_studies, orient='index')
    studies_df.to_csv(r"C:\Users\ryanm\Documents\Code\ct_database_builder\ct_tester.csv")
    print(studies_df.head())

if __name__ == "__main__":
    main()
