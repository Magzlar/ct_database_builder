from dateutil import parser
import logging
import requests
import os

class DataProcessing:
    API_key = os.getenv("API_key")

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

            nct_id = identification_module.get("nctId")
            if nct_id:
                self.processed_studies[nct_id] = {
                    'company': identification_module.get("organization", {}).get("fullName"),
                    'sponsor': sponsor_module.get("leadSponsor", {}).get("name"),
                    'enrollment_count': design_module.get("enrollmentInfo", {}).get("count"),
                    'status': status_module.get("overallStatus"),
                    'start_date': self.format_datetime(status_module.get("startDateStruct", {}).get("date")),
                    'end_date': self.format_datetime(status_module.get("primaryCompletionDateStruct", {}).get("date")),
                    "market_cap":self.get_market_cap(identification_module.get("organization",{}).get("fullName"))
                }

    def format_datetime(self, date: str):
        '''Return datetime object from string, or None if parsing fails.'''
        if date is None:
            return None
        try:
            return parser.parse(date)
        except parser.ParserError as e:
            logging.error(f"Error parsing date: {date} - {e}")
            return None
        
    def get_market_cap(self,company_name:str):
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



