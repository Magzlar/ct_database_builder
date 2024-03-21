### Testing file ###

import requests

url = r"https://clinicaltrials.gov/api/v2/studies"
disease_area = 'Psoriatic arthritis'
fields = "Condition|InterventionType|NumPhases|EnrollmentCount|PrimaryOutcomeMeasure|PrimaryOutcomeTimeFrame|NumPrimaryOutcomes|OrgFullName|StartDate"
query_term = "AREA[StartDate]RANGE[2013-01,MAX]"
#parameters = {'query.cond': disease_area,"fields": fields,"query.term":query_term,"pageSize":100}
parameters = {'query.cond': disease_area,"fields": fields,"pageSize":100}


response = requests.get(url,params=parameters)
json = response.json()

for i in json["studies"]:
    try:
        print(i["protocolSection"]['statusModule']['startDateStruct']["date"])
    except KeyError:
        print("Dictionary key not found")