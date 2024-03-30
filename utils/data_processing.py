from dateutil import parser
from dateutil.relativedelta import relativedelta
import logging
import requests
import re
import os

class DataProcessing:

    API_key = os.getenv("alphavantage_api_key")

    def __init__(self, studies):
        self.studies = studies
        self.processed_studies = {}
        self.process_studies()

    def process_studies(self):
        """Pulls data from CT gov and stores data in a dictionary"""
        for study in self.studies:
            study_info = study.get("protocolSection", {})
            identification_module = study_info.get("identificationModule", {})
            sponsor_module = study_info.get('sponsorCollabratorModule', {})
            design_module = study_info.get("designModule", {})
            status_module = study_info.get("statusModule", {})
            outcome_module = study_info.get('outcomesModule', {})

            nct_id = identification_module.get("nctId")
            if nct_id:
                self.processed_studies[nct_id] = {
                    'company': identification_module.get("organization", {}).get("fullName"),
                    'sponsor': sponsor_module.get("leadSponsor", {}).get("name"),
                    'enrollment_count': design_module.get("enrollmentInfo", {}).get("count"),
                    'status': status_module.get("overallStatus"),
                    'primary_outcome_measure': outcome_module.get("primaryOutcomes", {}).get("measure"),
                    'primary_outcome_timeframe': self.convert_to_relativedelta(outcome_module["primaryOutcomes"]["timeFrame"]),
                    'study_facilities':[x["facility"] for x in study_info["contactsLocationsModule"]["locations"]],
                    'locations_count': len(study_info["contactsLocationsModule"]["locations"]),
                    'start_date': self.format_datetime(status_module.get("startDateStruct", {}).get("date")),
                    'end_date': self.format_datetime(status_module.get("primaryCompletionDateStruct", {}).get("date")),
                    "market_cap":self.get_market_cap(identification_module.get("organization",{}).get("fullName")) # need to add number of study locations
                }

    def format_datetime(self, date: str)->parser:
        if date is None:
            return None
        try:
            return parser.parse(date)
        except parser.ParserError as e:
            logging.error(f"Error parsing date: {date} - {e}")
            return None
        
    def get_market_cap(self,company_name:str):
        '''Return market cap in dollars from company name'''
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company_name}&apikey={DataProcessing.API_key}'
        try:
            response = requests.get(url)
            data = response.json()
            return data
        except requests.ConnectionError as e:
            logging.error(f"Could not establish a connection with {url}")
            return None
        finally:
            logging.error("Unknown error")
            return None
        
    def convert_to_relativedelta(time_frame_str:str=None)->relativedelta:
        """Returns relativedelta object from string"""

        time_unit_to_relativedelta_param = {
            'year': 'years',
            'month': 'months',
            'week': 'weeks',
            'day': 'days'
        }
        
        match = re.match(r'(\d+)\s*(year|month|week|day)s?', time_frame_str)
        
        if not match:
            raise ValueError(f"Invalid time frame format: {time_frame_str}")
        
        number_of_units, unit = int(match.group(1)), match.group(2)

        relativedelta_param = time_unit_to_relativedelta_param[unit]
        
        return relativedelta(**{relativedelta_param: number_of_units})
    
    def get_approval_status(self,asset:str)->str:
        pass 


