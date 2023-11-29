import React, { Component, ReactNode } from 'react';
import { Link } from 'react-router-dom';

export default class Main extends Component {
	render(): ReactNode {
		return (
			<div>
				<h1> This is the main page. </h1>
				
				<Link to='/another'>
					Go to another page.
				</Link>
			</div>
		)
	}
}