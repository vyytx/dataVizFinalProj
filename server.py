from flask import Flask, render_template, jsonify, redirect
from data_helpers import get_county_mean_temperature, \
						 get_county_mean_rainfall, \
						 get_county_temperature_extremum
from fetch import fetch_all

app = Flask(__name__)

@app.route('/')
def index():
	return redirect('/temperature')

@app.route('/temperature')
def temperature():
	return render_template(
		'temperature.html',
		chart_data = get_county_mean_temperature(),
	)

@app.route('/rainfall')
def rainfall():
	return render_template(
		'rainfall.html',
		chart_data = get_county_mean_rainfall()
	)

@app.route('/county/<string:countyName>')
def county(countyName):
	return render_template(
		'county.html',
		location = countyName,
		temperature_forecast_data = get_county_temperature_extremum(countyName)
	)


if __name__ == '__main__':
	fetch_all()
	app.run(debug=True, port=5001)