import React, { Component, ReactNode } from 'react';
import { Link } from 'react-router-dom';

export default class Another extends Component {
	render(): ReactNode {
		return (
			<div>
				<h1> This is another page. </h1>
				
				<Link to='/'>
					Back to main page.
				</Link>
			</div>
		)
	}
}