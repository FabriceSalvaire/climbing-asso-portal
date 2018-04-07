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

import { RouteRow } from './route-table-tpl.jsx';

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
		<React.Fragment>
		    {routes.map(route => (<RouteRow key={route.id} route={route} />))}
		</React.Fragment>
	    );
    }
}
