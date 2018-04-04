/**************************************************************************************************/

// import 'babel-polyfill';

import React from 'react';
import ReactDOM from 'react-dom';

import { RouteTable, RouteTableFilters } from './route-table-components.jsx';

/**************************************************************************************************/

var route_table = ReactDOM.render(
    <RouteTable/>,
    document.getElementById('route-table')
);

ReactDOM.render(
    <RouteTableFilters route_table={route_table} />,
    document.getElementById('filters')
);
