import os
import json
import requests as req
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'
WEATHER_FORECAST_DATA_PATH = './data/weather-forecast.json'
WEATHER_HISTORY_DATA_PATH = './data/weather-history.json'
STATION_DATA_PATH = './data/station.json'
DATE_FORMAT = '%Y-%m-%d %H'

def fetch_all():
	"""
    Fetch weather and rainfall data from [Open Weather Data](https://opendata.cwa.gov.tw/) into json files.
    """
	fetch_weather()
	fetch_rainfall()
	fetch_weather_forecast()
	fetch_weather_history()
	fetch_station()

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

def fetch_windspeed():
	# Check if the data is already fetched today
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Windspeed data is up to date')
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
		print('Error when requesting windspeed data')

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

def fetch_weather_history():
	try:
		with open(WEATHER_HISTORY_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Weather forecast data is up to date')
				return
	except FileNotFoundError:
		pass

	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/C-B0024-001?downloadType=WEB&format=JSON'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['cwaopendata']['resources']['resource']['data']['surfaceObs']['location']
		}
		with open(WEATHER_HISTORY_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting weather history data')

def fetch_weather_forecast():
	try:
		with open(WEATHER_FORECAST_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Weather forecast data is up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['location']
		}
		with open(WEATHER_FORECAST_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting weather forecast data')

def fetch_station():
	try:
		with open(STATION_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			if json_data['date'] == datetime.now().strftime(DATE_FORMAT):
				print('Station data is up to date')
				return
	except FileNotFoundError:
		pass
	
	# Fetch data from API
	url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/C-B0074-001'
	headers = {'Authorization': os.getenv('API_KEY')}
	res = req.get(url, headers=headers)

	if res.status_code == 200: # If the request is successful
		data = res.json()
		json_data = {
			'date': datetime.now().strftime(DATE_FORMAT),
			'data': data['records']['data']['stationStatus']['station']
		}
		with open(STATION_DATA_PATH, 'w', encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=2)
	else:
		print('Error when requesting station data')


