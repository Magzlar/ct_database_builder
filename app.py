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
    fields = "Condition|InterventionType|Phase|EnrollmentCount|PrimaryOutcomeMeasure|PrimaryOutcomeTimeFrame|NumPrimaryOutcomes|OrgFullName|StartDate|PrimaryCompletionDate|NCTId|LeadSponsorName"
    query_term = "AREA[StartDate]RANGE[2013-01-01,MAX]"
    parameters = {'query.cond': disease_area, "query.term":query_term, "fields": fields,'format': 'json'}

    # make an instance of ClinicalTrial class and fetch the studies
    ct_api = ClinicalTrial(parameters)
    studies = ct_api.fetch_studies()

    if not studies:
        logger.error("no studies were fetched from the API")
        return
    
    # process the data cleaning, formating and feature engineering for SQL storage
    processor = DataProcessing(studies["studies"])
    studies_df = pd.DataFrame.from_dict(processor.processed_studies, orient='index')
    print(studies_df.head())

if __name__ == "__main__":
    main()
