import requests
import logging

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClinicalTrialError(Exception):
    """class for ClinicalTrial exceptions"""

class ClinicalTrial:
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

    def __init__(self, disease_area, parameters=None):
        self.disease_area = disease_area
        self.parameters = parameters or {}
        self.studies = {}

    def fetch_studies(self):
        """fetch studies from the API and store them in the instance of the class"""
        try:
            response = requests.get(ClinicalTrial.BASE_URL, params=self.parameters)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise ClinicalTrialError(f"API request failed: {e}")
        except KeyError:
            logger.error("Unexpected response structure")
            raise ClinicalTrialError("Unexpected response structure")

    def update_parameters(self, new_params):
        """enables update of request parameters for any subsequent API calls"""
        self.parameters.update(new_params)
