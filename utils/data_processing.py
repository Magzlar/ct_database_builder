from dateutil import parser
from dateutil.relativedelta import relativedelta
import logging
import requests
import re
import os

class DataProcessing:

    API_key = os.getenv("alphavantage_api_key")
    # Mapping for plural as relativedelta only work with plurals
    relativedelta_mapping = {
                "day":1,
                "days":1,
                "week":7,
                "weeks":7,
                "month":30,
                "months":30,
                "year":365,
                "years":365
                }

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
                    'primary_outcome_measure': outcome_module.get("primaryOutcomes"[0], {}).get("measure"),
                    'primary_outcome_timeframe': self.convert_to_relativedelta(outcome_module["primaryOutcomes"][0]["timeFrame"]),
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
        """Returns relativedelta object from string by finding the time unit and returning it's qunatity in days """

        unit_list = []
        time_list = []

        time_frame_str_lower = time_frame_str.lower()

        time_frame_list = time_frame_str_lower.split(" ")

        for i in time_frame_list:
            if i in ["day","week","month","year"]:
                unit_list.append(DataProcessing.relativedelta_mapping[i])
            elif re.match("\d+",i):
                time_list.append(int(i))
            else:
                continue

        rd = relativedelta.relativedelta(days=(unit_list[0]*time_list[0]))

        return rd
    
    def get_approval_status(self,asset:str)->str:
        pass 


