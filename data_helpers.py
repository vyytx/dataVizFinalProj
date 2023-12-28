import json
import pandas as pd

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'

def get_county_mean_rainfall():
	try:
		with open(RAINFALL_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			result_list = (
				df[~df['RainfallElement.Now.Precipitation'].isin([-99, -98, 'X', 'T'])]
					.groupby('GeoInfo.CountyName')['RainfallElement.Now.Precipitation']
					.mean()
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						'RainfallElement.Now.Precipitation': 'z'
					})
					.to_dict(orient='records')
			)
			result_json = json.dumps(result_list, ensure_ascii=False)
				
	except FileNotFoundError:
		print('Rainfall data not found')
		return
	return result_json

def get_county_mean_temperature():
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			result_list = (
				df[df['WeatherElement.AirTemperature'] != -99]
					.groupby('GeoInfo.CountyName')['WeatherElement.AirTemperature']
					.mean()
					.round(1)
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						'WeatherElement.AirTemperature': 'z'
					})
					.to_dict(orient='records')
			)

			result_json = json.dumps(result_list, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json