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

// import 'babel-polyfill';

import es6BindAll from 'es6bindall';

import { FrenchGrade } from '../../tools/grade.js';

/**************************************************************************************************/

export
class RouteModel {
    constructor(endpoint) {
	es6BindAll(this, ['_on_xhr_success', '_on_xhr_error']);

	this._endpoint = endpoint;

	this._error = null;
	this._routes = null;
	this._filtered_routes = null;
	this._view = null;

	this._load();
    }

    get routes() {
	if (this._filtered_routes !== null)
	    return this._filtered_routes;
	else
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
	// console.log('RouteModel GET', this._endpoint);

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
	// console.log('RouteModel xhr success');
	this._routes = this._prepare_routes(result.results);
	// console.log('RouteModel fetched', this._routes.length, this._view);
	this._view.update();
    }

    _on_xhr_error(error) {
	// console.log('RouteModel xhr error');
	this._routes = [];
	this._error = error;
	this._view.update();
    }

    // Slot
    filter_on_grade(min, max) {
	// console.log('RouteModel filter_on_grade', min , max);
	if (this._routes !== null) {
	    const min_float = min.float;
	    const max_float = max.float;
	    this._filtered_routes = this._routes.filter(
		route =>
		    min_float <= route.grade_float &&
		    route.grade_float <= max_float
	    );
	    this._view.update();
	}
    }
}
