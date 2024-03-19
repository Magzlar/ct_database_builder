### Testing file ###

import requests

url = r"https://clinicaltrials.gov/api/v2/studies"
disease_area = 'Psoriatic arthritis'
fields = "Condition|InterventionType|NumPhases|EnrollmentCount|PrimaryOutcomeMeasure|PrimaryOutcomeTimeFrame|NumPrimaryOutcomes|OrgFullName|StartDate"
query_term = "AREA[StartDate]RANGE[MIN,2012-01-15]"
parameters = {'query.cond': disease_area,"fields": fields,"query.term":query_term}


response = requests.get(url,params=parameters)
json = response.json()

print(json["nextPageToken"])