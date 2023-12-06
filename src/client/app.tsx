import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import './css/tailwind.css'
  
import Main from './pages/Main';
import Another from './pages/Another';

const router = createBrowserRouter([
	{
		path: "/",
		element: <Main />
	},
	{
		path: "/another",
		element: <Another />
	}
]);

const rootElement = document.querySelector('#root') as Element;
ReactDOM.createRoot(rootElement).render(
	<React.StrictMode>
		<link rel="stylesheet" href="https://rsms.me/inter/inter.css"></link>

		<RouterProvider router={router} />
	</React.StrictMode>
);