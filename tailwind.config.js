const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
	content: ["./src/client/**/*.{tsx,ts,js,html}"],
	theme: {
		extend: {
			fontFamily: {
				sans: ['Inter var', ...defaultTheme.fontFamily.sans],
			},
		},
	},
	// ...
}