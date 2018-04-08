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

import {
    // alice_milliat_wall_line_position,
    alice_milliat_wall_line_profiles
} from './alice-milliat-wall.js';

/**************************************************************************************************/

export
class RouteModel {
    constructor(endpoint) {
	es6BindAll(this, ['_on_xhr_success', '_on_xhr_error', '_to_line']);

	this._endpoint = endpoint;
	this._wall_profile = alice_milliat_wall_line_profiles;
	var profiles = new Set();
	var inclinations = new Set();
	this._wall_profile.map(line => {
	    profiles.add(line.profile);
	    inclinations.add(line.inclination);
	});
	this._profiles = Array.from(profiles);
	this._inclinations = Array.from(inclinations);

	this._error = null;
	this._routes = null;
	this._filtered_routes = null;
	this._grade_filter = null;
	this._profile_filter = null;
	this._inclination_filter = null;

	this._view = null;

	this._load();
    }

    get routes() {
	if (this._filtered_routes !== null)
	    return this._filtered_routes;
	else
	    return this._routes;
    }

    get profiles() {
	return this._profiles;
    }

    get inclinations() {
	return this._inclinations;
    }

    get error() {
	return this._error;
    }

    set_view(view) {
	this._view = view;
    }

    _to_line(route) {
	var i = route.line_number -1;
	if (i < this._wall_profile.length)
	    return this._wall_profile[i];
	else
	    // return dummy line
	    return { line_number: route.line_number, sector:'', profile: '', inclination: '' };
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
	    route.line = this._to_line(route);
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
	this._view.model_update();
    }

    _on_xhr_error(error) {
	// console.log('RouteModel xhr error');
	this._routes = [];
	this._error = error;
	this._view.model_update();
    }

    // Slot
    filter_on_grade(grade_range) {
	this._grade_filter = grade_range;
	// this.filter_on_profile(['Dièdre', 'Plan'])
	this._filter();
    }

    filter_on_profile(profiles) {
	console.log('filter_on_profiles', profiles);
	this._profile_filter = profiles !== null ? new Set(profiles) : null;
	this._filter();
    }

    filter_on_inclination(inclinations) {
	console.log('filter_on_inclination', inclinations);
	this._inclination_filter = inclinations !== null ? new Set(inclinations) : null;
	this._filter();
    }

    _filter() {
	// console.log('RouteModel filter_on_grade', min , max);
	if (this._routes !== null) {
	    var routes = Array.from(this._routes);

	    if (this._grade_filter !== null) {
		const [min_float, max_float] = this._grade_filter.map(grade => grade.float);
		routes = routes.filter(
		    route => min_float <= route.grade_float && route.grade_float <= max_float
		);
	    }

	    if (this._profile_filter !== null)
	    	routes = routes.filter(route => this._profile_filter.has(route.line.profile));

	    if (this._inclination_filter !== null)
		routes = routes.filter(route => this._inclination_filter.has(route.line.inclination));

	    this._filtered_routes = routes;
	    this._view.model_update();
	}
    }
}
