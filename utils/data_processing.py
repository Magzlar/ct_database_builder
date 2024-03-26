from dateutil import parser
import sqlite3
import logging

class DataProcessing:
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
                    'end_date': self.format_datetime(status_module.get("primaryCompletionDateStruct", {}).get("date"))
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
