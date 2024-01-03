import json
import pandas as pd
from datetime import datetime
import statistics as st

WEATHER_DATA_PATH = './data/weather.json'
RAINFALL_DATA_PATH = './data/rainfall.json'
WEATHER_FORECAST_DATA_PATH = './data/weather-forecast.json'
WEATHER_HISTORY_DATA_PATH = './data/weather-history.json'
MONTHLY_AVERAGE_DATA_PATH = './data/monthly-average.json'
MANNED_STATION_INFORMATION = './data/manned-station-information.json'
UNMANNED_STATION_INFORMATION = './data/unmanned-station-information.json'
OBS_RECORD_30DAYS = './data/obs-record-30days.json'

def find_middle_time(time_str_1, time_str_2):
	time_1 = datetime.strptime(time_str_1, "%Y-%m-%dT%H:%M:%S%z")
	time_2 = datetime.strptime(time_str_2, "%Y-%m-%dT%H:%M:%S%z")
	result = time_1 + (time_2 - time_1)/2 
	return result.strftime("%Y-%m-%d %H:%M:%S")

def time_format(time_str):
	result = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")
	return result.strftime("%m/%d %H:%M")


def get_county_mean_rainfall(time_range):
	try:
		with open(RAINFALL_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			result_list = (
				df[~df[f'RainfallElement.{time_range}.Precipitation'].isin([-99, -98, 'X', 'T'])]
					.groupby('GeoInfo.CountyName')[f'RainfallElement.{time_range}.Precipitation']
					.mean()
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						f'RainfallElement.{time_range}.Precipitation': 'z'
					})
					.to_dict(orient='records')
			)
			result_json = json.dumps(result_list, ensure_ascii=False)
				
	except FileNotFoundError:
		print('Rainfall data not found')
		return
	return result_json

def get_rainfall_time_range():
	time_range = ['Now', 'Past10Min', 'Past1hr', 'Past3hr', 'Past6Hr', 'Past12hr', 'Past24hr', 'Past2days', 'Past3days']
	return time_range

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
			result_list = (
				df[df['WeatherElement.WindSpeed'] != -99]
					.groupby('GeoInfo.CountyName')['WeatherElement.WindSpeed']
					.mean()
					.round(1)
					.reset_index()
					.rename(columns={
						'GeoInfo.CountyName': 'location', 
						'WeatherElement.WindSpeed': 'z'
					})
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
					range_list = []
					for element in data['weatherElement']:
						if element['elementName'] == 'MinT':
							for time in element['time']:
								minT_list.append(time['parameter']['parameterName'])
								x_list.append(find_middle_time(time['startTime'], time['endTime']))
								range_list.append(f'{time_format(time["startTime"])} ~ {time_format(time["endTime"])}')		
						if element['elementName'] == 'MaxT':
							for time in element['time']:
								maxT_list.append(time['parameter']['parameterName'])
						
					result = {
						'MinT': minT_list,
						'MaxT': maxT_list,
						'x': x_list,
						'range': range_list
					}
			result_json = json.dumps(result, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result_json

# def get_county_temperature_history(location):
# 	try:
# 		with open(WEATHER_HISTORY_DATA_PATH, 'r', encoding='utf-8') as json_file:
# 			json_data = json.load(json_file)
# 			data_list = json_data['data']
# 			daily_list_list = []
# 			for data in data_list:
# 				county = get_station_county(data['station']['StationID'])
# 				if county == location:
# 					daily_list_list.append(data['stationObsStatistics']['AirTemperature']['daily'])

# 			organized = dict()
# 			if len(daily_list_list):
# 				for daily_list in daily_list_list:
# 					for day in daily_list[-7:]:
# 						organized.setdefault(day['Date'], {
# 							'Date': day['Date'],
# 							'Maximum': 0,
# 							'Minimum': 0
# 						})
# 						organized[day['Date']]['Maximum'] += float(day['Maximum'])
# 						organized[day['Date']]['Minimum'] += float(day['Minimum'])
# 				for day in daily_list_list[0][-7:]:
# 					organized[day['Date']]['Maximum'] /= len(daily_list_list)
# 					organized[day['Date']]['Minimum'] /= len(daily_list_list)
			
# 			result_dict = {
# 				"x": [date+" 00:00:00" for date in organized],
# 				"MaxT": [day['Maximum'] for day in organized.values()],
# 				"MinT": [day['Minimum'] for day in organized.values()],
# 			}

# 			result_json = json.dumps(result_dict, ensure_ascii=False)
# 	except FileNotFoundError:
# 		print('Weather data not found')
# 		return
# 	return result_json

def get_station_county(stationID):
	try:
		with open(MANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			data_list = json_data['data']
			for data in data_list:
				if data['StationID'] == stationID:
					county = data['CountyName']
					break
	except FileNotFoundError:
		print('Weather data not found')
		return
	return county

def get_county_information(location):
	try:
		with open(WEATHER_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			data_list = json_data['data']
			temperature_list = []
			humidity_list = []
			pressure_list = []
			windspeed_list = []
			for data in data_list:
				if data['GeoInfo']['CountyName'] == location:
					if(data['WeatherElement']['AirTemperature']!= -99):
						temperature_list.append(data['WeatherElement']['AirTemperature'])
					if(data['WeatherElement']['RelativeHumidity']!= -99):
						humidity_list.append(data['WeatherElement']['RelativeHumidity'])
					if(data['WeatherElement']['AirPressure']!= -99):
						pressure_list.append(data['WeatherElement']['AirPressure'])
					if(data['WeatherElement']['WindSpeed']!= -99):
						windspeed_list.append(data['WeatherElement']['WindSpeed'])
			result = {
				'temperature': round(st.mean(temperature_list), 2) if temperature_list else 'X',
				'pressure': round(st.mean(pressure_list), 2) if pressure_list else 'X',
				'windspeed': round(st.mean(windspeed_list), 2) if windspeed_list else 'X',
				'humidity': round(st.mean(humidity_list), 2) if humidity_list else 'X',
			}
			print(result)
	except FileNotFoundError:
		print('Weather data not found')
		return
	return result

def get_counties():
	counties = ['臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '基隆市', '新竹市', '嘉義市']
	return counties

def get_station_information():
	try:
		with open(UNMANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			unmanned_station = df[['StationID', 'CountyName']]
	except FileNotFoundError:
		print('Unmanned station information data not found')
		return
	
	try:
		with open(MANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			manned_station = df[['StationID', 'CountyName']]	
	except FileNotFoundError:
		print('Manned station information data not found')
		return
	
	result = pd.concat([unmanned_station, manned_station]).set_index('StationID')['CountyName'].to_dict()
	return result

def get_unnmanned_station_information():
	try:
		with open(UNMANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			unmanned_station = df[['StationID', 'CountyName']]
			result = unmanned_station.set_index('StationID')['CountyName'].to_dict()
	except FileNotFoundError:
		print('Unmanned station information data not found')
		return
	return result

def get_manned_station_information():
	try:
		with open(MANNED_STATION_INFORMATION, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			df = pd.json_normalize(json_data, 'data')
			manned_station = df[['StationID', 'CountyName']]
			result = manned_station.set_index('StationID')['CountyName'].to_dict()
	except FileNotFoundError:
		print('Unmanned station information data not found')
		return
	return result

def get_county_history_temperature(location):
	station_dict = get_manned_station_information()
	try:
		with open(WEATHER_HISTORY_DATA_PATH, 'r', encoding='utf-8') as json_file:
			json_data = json.load(json_file)
			station_list = json_data['data']
			result_list = []
			for station in station_list:
				station_id = station['station']['StationID']
				df = pd.json_normalize(station, ['stationObsTimes', 'stationObsTime'])
				df['DateTime'] = df['DateTime'].str.replace("24:00:00", "00:00:00")
				df['DateTime'] = pd.to_datetime(df['DateTime'])
				df['weatherElements.AirTemperature'] = pd.to_numeric(df['weatherElements.AirTemperature'], errors='coerce')
				result = (
					df.groupby([df['DateTime'].dt.date])['weatherElements.AirTemperature']
						.mean()
						.reset_index()
						.rename(columns={
							'DateTime': 'date', 
							'weatherElements.AirTemperature': 'temperature'
						})
				)
				result['date'] = result['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
				result['countyName'] = station_dict[station_id]
				result_list.append(result)
			
			result = pd.concat(result_list, ignore_index=True)
			result_avg = (
				result.groupby(['countyName', 'date'])['temperature']
				.mean()
				.round(1)
				.reset_index()
			)
			result_data_combined = (
				result_avg.groupby('countyName')[['date', 'temperature']]
					.apply(lambda x: x.to_dict(orient='records'))
					.reset_index(name='data')
			)
			result_dict = result_data_combined.set_index('countyName')['data'].to_dict()
			county_history_data = result_dict.get(location, [])
			result_json = ''
			if county_history_data:
				result_json = json.dumps(county_history_data, ensure_ascii=False)
	except FileNotFoundError:
		print('Weather history data not found')
		return
	return result_json