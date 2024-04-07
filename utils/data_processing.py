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
    counter = 0

    def __init__(self, studies):
        self.studies = studies
        self.processed_studies = {}
        self.process_studies()

    def process_studies(self):
        """Pulls data from CT gov and stores data in a dictionary"""

        for study in self.studies:
            DataProcessing.counter += 1 
            print(DataProcessing.counter)
            study_info = study.get("protocolSection", {})
            identification_module = study_info.get("identificationModule", {})
            design_module = study_info.get("designModule", {})
            status_module = study_info.get("statusModule", {})
            outcome_module = study_info.get('outcomesModule', {})
            locations_module = study_info.get("contactsLocationsModule",{}).get('locations', [])
            primary_outcomes = outcome_module.get("primaryOutcomes",[{"":""}])

            nct_id = identification_module.get("nctId")
            if nct_id:
                self.processed_studies[nct_id] = {
                    'company': identification_module.get("organization", {}).get("fullName"),
                    'enrollment_count': design_module.get("enrollmentInfo", {}).get("count"),
                    'status': status_module.get("overallStatus"),
                    'primary_outcome_measures': [x.get("measure","") for x in primary_outcomes],
                    'primary_outcome_timeframes': self.convert_to_relativedelta([x.get("timeFrame", "") for x in primary_outcomes]),
                    'facilites_count': len(locations_module),
                    "city_count": len(list(set([x["city"] for x in locations_module]))),
                    'countries_count':len(list(set([x["country"] for x in locations_module]))),
                    'start_date': self.format_datetime(status_module.get("startDateStruct", {}).get("date")),
                    'end_date': self.format_datetime(status_module.get("primaryCompletionDateStruct", {}).get("date")),
                    #"market_cap":self.get_market_cap(identification_module.get("organization",{}).get("fullName")) # need create mapping for company names a tickers moght be better to do this in a seperate file once got the data
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
        
    def convert_to_relativedelta(self,time_frame_str:list=None)->relativedelta:
        """Returns relativedelta object from string by finding the time unit and returning it's qunatity in days"""

        unit_list = [] # holds the unit of time e.g. days, week, month
        amount_list = [] # holds the amount of that time
        pattern = r"[,\(\)]"

        for x in time_frame_str:

            time_frame_str_lower = x.lower()
            remove_dash = re.sub("-", " ", time_frame_str_lower)
            remove_punc = re.sub(pattern, "", remove_dash)

            time_frame_list = remove_punc.split(" ")

            for i in time_frame_list:
                if i in ["day","week","month","year"]:
                    unit_list.append(DataProcessing.relativedelta_mapping[i])
                elif re.match("\d+",i):
                    amount_list.append(float(i))
                else:
                    continue

            time_list = [a * b for a, b in zip(unit_list, amount_list)] # list of relative time deltas in days to return 
            return [relativedelta(day=x) for x in time_list]
    
    
    def get_approval_status(self,asset:str)->str:
        pass 


