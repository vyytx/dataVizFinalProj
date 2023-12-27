import json
import pandas as pd

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'

def get_county_mean_rainfall():
	try:
		with open(RAINFALL_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			print(df.groupby('GeoInfo.CountyName')['RainfallElement.Now.Precipitation'].mean())
	except FileNotFoundError:
		print('Rainfall data not found')
		return
	return 

def get_county_mean_temperature():
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			filtered_df = df[df['WeatherElement.AirTemperature'] != -99]
			print(filtered_df.groupby('GeoInfo.CountyName')['WeatherElement.AirTemperature'].mean())
	except FileNotFoundError:
		print('Weather data not found')
		return
	return 

get_county_mean_rainfall()
get_county_mean_temperature()