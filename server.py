from flask import Flask, render_template, jsonify
from data_helpers import get_county_mean_temperature

app = Flask(__name__)

@app.route('/')
def formPage():
	return render_template(
		'index.html',
		county_mean_temperature=get_county_mean_temperature()
	)

if __name__ == '__main__':
	app.run(debug=True, port=5001)