import nodeResolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import babel from '@rollup/plugin-babel'
import replace from '@rollup/plugin-replace'
//import css from "rollup-plugin-css-only"
import postcss from 'rollup-plugin-postcss'
import typescript from '@rollup/plugin-typescript'
import json from '@rollup/plugin-json'
import dsv from '@rollup/plugin-dsv'

import { ChildProcess, spawn } from 'child_process'

import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

import tsconfigJSON from './tsconfig.json' assert { type: 'json' }
const isDev = process.env.ROLLUP_WATCH;

/** @type {import('rollup'.RollupOptions)} */
export default {
	input: 'src/client/app.tsx',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js',
		inlineDynamicImports: true
	},
	plugins: [
		//css({
		//	output: "bundle.css"
		//}),
		nodeResolve({
			browser: true,
			dedupe: ['react', 'react-dom'],
			extensions: ['.ts', '.tsx']
		}),
		typescript(tsconfigJSON),
		babel({
			babelHelpers: 'bundled',
			presets: ['@babel/preset-react', '@babel/preset-typescript'],
			extensions: ['.ts', '.tsx']
		}),
		postcss({
			plugins: [
				tailwindcss('./tailwind.config.js'),
				autoprefixer(),
			],
			extensions: ['.css'],
		}),
		commonjs(),
		json({
			compact: true
		}),
		dsv(),
		replace({
			preventAssignment: false,
			'process.env.NODE_ENV': '"development"'
		}),
		isDev && await startDevSever()
	],
	watch: {
		clearScreen: true
	}
}

async function startDevSever() {
	/** @type {ChildProcess} */
	let server;

	function kill() {
		if (server)
			server.kill(0)
	}

	return {
		writeBundle() {
			if(server)
				return

			server = spawn('npm', ['run', 'serve'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			})

			process.on('SIGTERM', kill)
			process.on('exit', kill)
		}
	}
}
