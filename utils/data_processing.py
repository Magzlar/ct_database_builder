from   dateutil import parser
import sqlite3
import logging

class DataProcessing:

    def __init__(self,data) -> None:
        self.studies = {}

    def process_studies(self, studies:list):
        """Pulls data from CT gov and stores data in dictionary"""
        for study in studies:
            study_info = study["protocolSection"]
            nct_id = study_info["identificationModule"]["nctId"]
            self.studies[nct_id] = {
                'company': study_info["identificationModule"]["organization"]["fullName"],
                'sponsor_type': study_info['identificationModule']["organization"]["class"],
                'enrollment_count': study_info["designModule"]["enrollmentInfo"]["count"],
                'status': study_info["statusModule"]["overallStatus"],
                'start_date': study_info["statusModule"]["startDateStruct"]["date"],
                'end_date': study_info["statusModule"]["primaryCompletionDateStruct"]["date"]
                }
            
    def format_datetime(self,date:str)->parser.parse:
        '''Return datetime object from string'''
        try:
            return parser.parse(date)
        except parser.ParserError as e:
            logging.error("Unable to Parse date")