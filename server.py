from flask import Flask, render_template, jsonify
from data_helpers import get_county_mean_temperature, \
						 get_county_mean_rainfall
from fetch import fetch_all

app = Flask(__name__)

@app.route('/')
def index():
	return render_template(
		'index.html',
		chart_data = get_county_mean_temperature(),
	)

@app.route('/rainfall')
def rainfall():
	return render_template(
		'index.html',
		chart_data = get_county_mean_rainfall()
	)

if __name__ == '__main__':
	fetch_all()
	app.run(debug=True, port=5001)