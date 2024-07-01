# ct_database_builder
builds a python dictionary of clinical trials data from https://clinicaltrials.gov/api/v2
V2 will then insert the data into a local SQL database to store the data and allow for multiple requests over time to build the database up
The next part will be a regression problem, where will use machine learning algorithim to determine wether we can use the features from each of the clinical trials to accuratley predict the length of a clinical trial in a particular disease area based on it's features




Would be good to know wether we can find a reliable source to assess the time between Phase III and approval, look to see if drugbank has a date the drug was approved