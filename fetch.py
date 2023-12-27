import os
import json
import requests as req
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'
DATE_FORMAT = '%Y-%m-%d %H'

def fetch_weather():
	# Check if the data is already fetched today
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Weather data is up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['Station']
		}
		with open(WEATHER_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting weather data')

def fetch_rainfall():
	# Check if the data is already fetched today
	try:
		with open(RAINFALL_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Rainfall data is up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['Station']
		}
		with open(RAINFALL_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting rainfall data')

fetch_weather()
fetch_rainfall()