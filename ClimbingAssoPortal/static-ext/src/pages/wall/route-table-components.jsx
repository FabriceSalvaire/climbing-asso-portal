/**************************************************************************************************/

// import 'babel-polyfill';

import React from 'react';
import ReactDOM from 'react-dom';
import es6BindAll from 'es6bindall';
import ReactBootstrapSlider from 'react-bootstrap-slider';
// import ReactBootstrapSlider from '../../externals/react-bootstrap-slider.jsx';

import { FrenchGrade } from '../../tools/grade.js';
import { RouteRow, SliderWithValues } from './route-table-presentation.jsx';

/**************************************************************************************************/

export
class RouteTable extends React.Component {
    constructor(props) {
	super(props);

	this.state = {
	    error: null,
	    is_loaded: false,
	    routes: [],
	    grade_filter: [0, new FrenchGrade('9c+').float]
	};
    }

    prepare_routes(routes) {
	// console.log('Fetch', routes);
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

    componentDidMount() {
	const endpoint = '/api/routes/?limit=1000';

	// https://developer.mozilla.org/fr/docs/Web/API/WindowOrWorkerGlobalScope/fetch
	var fetch_init = {
	    method: 'GET',
	    credentials: 'include'
	};

	fetch(endpoint, fetch_init)
	    .then(result => result.json())
	    .then(
		result => {
		    this.setState({
			is_loaded: true,
			routes: this.prepare_routes(result.results)
		    });
		},
		// Note: it's important to handle errors here instead
		// of a catch() block so that we don't swallow
		// exceptions from actual bugs in components.
		error => {
		    this.setState({
			is_loaded: true,
			error
		    });
		}
	    )
    }

    // Slot
    filter_on_grade(min, max) {
	this.setState({ grade_filter: [min.float, max.float] });
    }

    render() {
	const { error, is_loaded, routes, grade_filter } = this.state;
	// Fixme:
	if (error) {
	    return <div>Error: {error.message}</div>;
	} else if (!is_loaded) {
	    return <div>Loading...</div>;
	} else {
	    var filtered_routes = routes.filter(route => grade_filter[0] <= route.grade_float && route.grade_float <= grade_filter[1]);
	    return (
		<React.Fragment>
		    {filtered_routes.map(route => (<RouteRow key={route.id} route={route} />))}
		</React.Fragment>
	    );
	}
    }
}

/**************************************************************************************************/

export
class RouteTableFilters extends React.Component {
    constructor(props) {
	super(props);
	es6BindAll(this, ['on_value_change']);

	this.route_table = props.route_table;

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
	this.route_table.filter_on_grade(...grade_min_max);
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
