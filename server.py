from flask import Flask, render_template, jsonify, redirect
from data_helpers import get_county_mean_temperature, \
						 get_county_mean_rainfall, \
						 get_county_mean_windspeed
from fetch import fetch_all

from icon_helper import svg_dict

app = Flask(__name__)

@app.route('/')
def index():
	return render_template(
		'mapView.html',
		icon = svg_dict,
		mean_temp = get_county_mean_temperature(),
		mean_rain = get_county_mean_rainfall(),
		mean_wind = get_county_mean_windspeed()
	)


@app.route('/test')
def test():
	return render_template(
		'test.html',
		chart_data = get_county_mean_temperature(),
	)

if __name__ == '__main__':
	fetch_all()
	app.run(debug=True, port=5001)