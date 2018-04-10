/***************************************************************************************************
 *
 * Climbing Asso Portal
 * Copyright (C) 2018 Fabrice Salvaire
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

/**************************************************************************************************/

import React from 'react';
import ReactDOM from 'react-dom';
import es6BindAll from 'es6bindall';
import ReactBootstrapSlider from 'react-bootstrap-slider';
// import ReactBootstrapSlider from '../../externals/react-bootstrap-slider.jsx';
import ReactTable from 'react-table';

import { FrenchGrade } from '../../tools/grade.js';

import { RouteRow } from './route-table-tpl.jsx';

import { hold_colours } from './hold-colour.js';

/**************************************************************************************************/

export
class RouteTable extends React.Component {
    constructor(props) {
	super(props);

	this._model = props.model;
	this._model.set_view(this);

	this.state = {};
    }

    // Slot
    model_update() {
	// console.log('RouteTable udpate');
	this.forceUpdate();
    }

    render() {
	const routes = this._model.routes;
	const error = this._model.error;
	// console.log('RouteTable render', error, routes);

	if (error)
	    return <div>Error: {error.message}</div>;
	else if (routes === null)
	    return <div>Loading...</div>;
	else
	    return (
		<ReactTable
		    data={routes}
		    columns={[
			{
			    Header: 'Line Number',
			    accessor: 'line_number',
			},
			{
			    Header: 'Sector',
			    id: 'sector',
			    accessor: route => route.line.sector,
			},
			{
			    Header: 'Profile',
			    id: 'profile',
			    accessor: route => route.line.profile,
			},
			{
			    Header: 'Inclination',
			    id: 'inclination',
			    accessor: route => route.line.inclination,
			},
                        {
                            Header: 'Grade',
                            accessor: 'grade',
 			    sortMethod: (a, b) => {
			        if (!a || a == 'ENF')
  			    	    a = '4a';
			    	if (!b || b == 'ENF')
			    	    b = '4a';
			    	a = new FrenchGrade(a).float;
			    	b = new FrenchGrade(b).float;
 				if (a > b)
 				    return 1;
 				if (a < b)
				    return -1;
 				return 0;
                            },
                        },
                        {
                            Header: 'Name',
                            accessor: 'name',
                        },
                        {
 			    Header: 'Colour',
			    accessor: 'colour',
			    Cell: row => {
			        var class_name = 'hold-colour hold-colour-' + hold_colours[row.value];
				return <div className={class_name}></div>;
 			    },
			},
			{
			    Header: 'Comment',
			    accessor: 'comment',
			},
			{
			    Header: 'Opener',
			    accessor: 'opener',
			},
			{
			    Header: 'Opening Date',
			    accessor: 'opening_date',
			}
		    ]}
		    defaultPageSize={10}
		    className="-striped -highlight"
		    />
		// <React.Fragment>
		//     {routes.map(route => (<RouteRow key={route.id} route={route} />))}
		// </React.Fragment>
	    );
    }
}
