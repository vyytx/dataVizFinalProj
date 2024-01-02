import json
from math import radians, degrees, sin, cos, atan
import pandas as pd
from datetime import datetime, timedelta

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'
WEATHER_FORECAST_DATA_PATH = './data/weather-forecast.json'

def find_middle_time(time_str_1, time_str_2):
	time_1 = datetime.strptime(time_str_1, "%Y-%m-%d %H:%M:%S")
	time_2 = datetime.strptime(time_str_2, "%Y-%m-%d %H:%M:%S")
	result = time_1 + (time_2 - time_1)/2 
	return result.strftime("%Y-%m-%d %H:%M:%S")

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

def get_county_mean_windspeed():
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)

			df = pd.json_normalize(json_data, 'data')

			df = df[
				~df['WeatherElement.WindDirection'].isin(['X', -99, 990])
				& ~df['WeatherElement.WindSpeed'].isin(['X', -99])
			]

			df['WeatherElement.WindSpeedNS'] = df['WeatherElement.WindSpeed'] * df['WeatherElement.WindDirection'].apply(radians).apply(sin)
			df['WeatherElement.WindSpeedEW'] = df['WeatherElement.WindSpeed'] * df['WeatherElement.WindDirection'].apply(radians).apply(cos)

			counties = df.groupby('GeoInfo.CountyName')

			cWSNS = counties['WeatherElement.WindSpeedNS'].mean()
			cWSEW = counties['WeatherElement.WindSpeedEW'].mean()

			counties = cWSNS.to_frame().join(cWSEW).rename(
				columns={
					'WeatherElement.WindSpeedNS': 'WindSpeedNS',
					'WeatherElement.WindSpeedEW': 'WindSpeedEW'
				})
			counties['z'] = ((counties['WindSpeedNS'] **2 + counties['WindSpeedEW'] ** 2) ** 0.5)
			counties['direction'] = (counties['WindSpeedNS'] / counties['WindSpeedEW']).apply(atan).apply(degrees)\
				.fillna(0) # since sometimes there were no wind

			result_list = (
				counties[['z', 'direction']]
					.reset_index()
					.rename(columns={'GeoInfo.CountyName': 'location'})
					.to_dict(orient='records')
			)

			result_json = json.dumps(result_list, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json

def get_county_temperature_extremum(location):
	try:
		with open(WEATHER_FORECAST_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			data_list = json_data['data']
			for data in data_list:
				if data['locationName'] == location:
					minT_list = []
					maxT_list = []
					x_list = []
					tick_list = []
					for element in data['weatherElement']:
						if element['elementName'] == 'MinT':
							for i, time in enumerate(element['time']):
								minT_list.append(time['parameter']['parameterName'])
								x_list.append(find_middle_time(time['startTime'], time['endTime']))
								tick_list.append(time['startTime'])
								if i == 2:
									tick_list.append(time['endTime'])
						if element['elementName'] == 'MaxT':
							for time in element['time']:
								maxT_list.append(time['parameter']['parameterName'])
					result = {
						'MinT': minT_list,
						'MaxT': maxT_list,
						'x': x_list,
						'ticks': tick_list
					}


			result_json = json.dumps(result, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json