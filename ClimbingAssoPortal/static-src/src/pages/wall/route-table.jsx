/***************************************************************************************************
 *
 * Climbing Grade
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

// import 'babel-polyfill';

import React from 'react';
import ReactDOM from 'react-dom';
import es6BindAll from 'es6bindall';
import ReactBootstrapSlider from 'react-bootstrap-slider';
// import ReactBootstrapSlider from '../../externals/react-bootstrap-slider.jsx';

import { FrenchGrade } from '../../tools/grade.js';
import { RouteRow, SliderWithValues } from './route-table-tpl.jsx';

/**************************************************************************************************/

export
class RouteModel {
    constructor(endpoint) {
	es6BindAll(this, ['_on_xhr_success', '_on_xhr_error']);

	this._endpoint = endpoint;
	this._loaded = false;
	this._error = null;
	this._routes = [];
	this._filtered_routes = [];

	this._view = null;

	this._load();
    }

    get loaded() {
	return this._loaded;
    }

    get routes() {
	return this._routes;
    }

    get error() {
	return this._error;
    }

    set_view(view) {
	this._view = view;
    }

    _prepare_routes(routes) {
	var i = 0;
	for (let route of routes) {
	    route.id = (i++).toString();
	    if (route.grade && route.grade.toLowerCase() != 'enf')
		route.grade_float = new FrenchGrade(route.grade).float;
	    else {
		// console.log('Null grade', route);
		route.grade_float = new FrenchGrade('4a').float;
	    }
	}

	return routes;
    }

    _load() {
	console.log('RouteModel GET', this._endpoint);

	// https://developer.mozilla.org/fr/docs/Web/API/WindowOrWorkerGlobalScope/fetch
	const fetch_init = {
	    method: 'GET',
	    credentials: 'include'
	};

	fetch(this._endpoint, fetch_init)
	    .then(result => result.json())
	    .then(this._on_xhr_success, this._on_xhr_error);
    }

    _on_xhr_success(result) {
	console.log('RouteModel xhr success');
	this._routes = this._prepare_routes(result.results);
	this._loaded = true;
	console.log('RouteModel fetched', this._routes.length, this._view);
	this._view.reset_routes(this._routes);
    }

    _on_xhr_error(error) {
	// Note: it's important to handle errors here instead of a
	// catch() block so that we don't swallow exceptions from
	// actual bugs in components.

	console.log('RouteModel xhr error');
	this._loaded = true;
	this._error = error;
	this._view.reset_routes([]);
    }

    // Slot
    filter_on_grade(min, max) {
	console.log('RouteModel filter_on_grade', min , max);
	if (this.routes !== null) {
	    const min_float = min.float;
	    const max_float = max.float;
	    this._filtered_routes = this._routes.filter(
		route =>
		    min_float <= route.grade_float &&
		    route.grade_float <= max_float
	    );
	    this._view.reset_routes(this._filtered_routes);
	}
    }
}

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
    reset_routes(routes) {
	console.log('RouteTable reset_routes', routes);
	this.forceUpdate();
    }

    render() {
	const loaded = this._model.loaded;
	const error = this._model.error;
	const routes = this._model.routes;
	console.log('RouteTable render', loaded, error, routes);

	if (error)
	    return <div>Error: {error.message}</div>;
	else if (! loaded)
	    return <div>Loading...</div>;
	else
	    return (
		<React.Fragment>
		    {routes.map(route => (<RouteRow key={route.id} route={route} />))}
		</React.Fragment>
	    );
    }
}

/**************************************************************************************************/

export
class RouteTableFilters extends React.Component {
    constructor(props) {
	super(props);
	es6BindAll(this, ['on_value_change']);

	this.route_model = props.route_model;

	this.grade_names = Array.from(FrenchGrade.grade_iter(4, 8));
	this.grades = this.grade_names.map(name => new FrenchGrade(name));
	this.max = this.grades.length -1;

	this.state = {
	    current_value: [0, this.max]
	};

	// this.on_value_change = this.on_value_change.bind(this);
    }

    on_value_change(event) {
	var min_max = event.target.value;
	this.setState({ current_value: min_max });

	// Signal: slider -> table
	var grade_min_max = min_max.map(value => this.grades[value]);
	this.route_model.filter_on_grade(...grade_min_max);
    }

    render() {
	const { current_value } = this.state;
	var [ min_grade, max_grade ] = current_value.map(i => this.grade_names[i]);
	var slider = (
	    <ReactBootstrapSlider
		value={current_value}
		change={this.on_value_change}
		slideStop={this.on_value_change}
		min={0}
		max={this.max}
		step={1}
		/>
	);
	return <SliderWithValues slider={slider} min={min_grade} max={max_grade} />;
    }
}
