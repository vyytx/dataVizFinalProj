temp_svg = '''
<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"
						stroke-linecap="round" stroke-linejoin="round">
	<path stroke="none" d="M0 0h24v24H0z" />
	<path d="M10 13.5a4 4 0 1 0 4 0v-8.5a2 2 0 0 0 -4 0v8.5" />
	<line x1="10" y1="9" x2="14" y2="9" />
</svg>
'''

rain_svg = '''
<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"
	stroke-linecap="round" stroke-linejoin="round">
	<path stroke="none" d="M0 0h24v24H0z" />
	<path d="M7 18a4.6 4.4 0 0 1 0 -9h0a5 4.5 0 0 1 11 2h1a3.5 3.5 0 0 1 0 7" />
	<path d="M11 13v2m0 3v2m4 -5v2m0 3v2" />
</svg>
'''

wind_svg = '''
<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"
	stroke-linecap="round" stroke-linejoin="round">
	<path stroke="none" d="M0 0h24v24H0z" />
	<path d="M5 8h8.5a2.5 2.5 0 1 0 -2.34 -3.24" />
	<path d="M3 12h15.5a2.5 2.5 0 1 1 -2.34 3.24" />
	<path d="M4 16h5.5a2.5 2.5 0 1 1 -2.34 3.24" />
</svg>
'''

svg_dict = {
	'temp': temp_svg,
	'rain': rain_svg,
	'wind': wind_svg
}