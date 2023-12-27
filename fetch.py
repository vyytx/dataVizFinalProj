import pandas as pd
import requests as req
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_weather():
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)
	if res.status_code == 200:
		json_data = res.json()
		df = pd.json_normalize(json_data, ['records', 'Station'])
		print(df['StationName'].value_counts())
	else:
		print('Error when requesting data')
	return 