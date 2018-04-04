// import 'babel-polyfill';

import React from 'react';
import ReactDOM from 'react-dom';
import es6BindAll from "es6bindall";
import ReactBootstrapSlider from 'react-bootstrap-slider';
// import ReactBootstrapSlider from '../../externals/react-bootstrap-slider.jsx';
import { FrenchGrade } from "../../tools/grade.js";

// https://developer.mozilla.org/fr/docs/Web/API/WindowOrWorkerGlobalScope/fetch
var fetch_init = {
    method: 'GET',
    credentials: 'include'
};

const RouteRow = ({ route }) => (
    <tr >
	<th scope="row"><a href="">{route.line_number}</a></th>
	<td>{route.grade}</td>
	<td>{route.colour}</td>
	<td>{route.name}</td>
	<td>{route.comment}</td>
	<td>{route.opener}</td>
	<td>{route.opening_date}</td>
    </tr>
);

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

    componentDidMount() {
	fetch('/api/routes/?limit=1000', fetch_init)
	    .then(result => result.json())
	    .then(
		(result) => {
		    var routes = result.results;
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
		    this.setState({
			is_loaded: true,
			routes
		    });
		},
		// Note: it's important to handle errors here
		// instead of a catch() block so that we don't swallow
		// exceptions from actual bugs in components.
		(error) => {
		    this.setState({
			is_loaded: true,
			error
		    });
		}
	    )
    }

    filter_on_grade(min, max) {
	// console.log('table filter', min.str, max.str);
	this.setState({ grade_filter: [min.float, max.float] });
    }

    render() {
	const { error, is_loaded, routes, grade_filter } = this.state;
	// console.log('table render', error, is_loaded, routes, grade_filter);
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

const SliderValue = ({ id, value }) => (
    <p className={'slider-value-' + id}>{value}</p>
);

class Filters extends React.Component {
    constructor(props) {
	// console.log('Filters', props, props.route_table);

	super(props);
	es6BindAll(this, ['on_value_change']);

	var grade_names = Array.from(FrenchGrade.grade_iter(4, 8));
	this.grades = grade_names.map(name => new FrenchGrade(name));
	// console.log(this.grades);
	var max = this.grades.length -1;

	this.state = {
	    current_value: [0, max],
	    min: 0,
	    max,
	    step: 1,
	    grade_names,
	    route_table
	};

	// this.on_value_change = this.on_value_change.bind(this);
    }

    on_value_change(event) {
	var min_max = event.target.value;
	this.setState({ current_value: min_max });
	// console.log('on_value_change', min_max);
	var grade_min_max = min_max.map(value => this.grades[value]);
	this.state.route_table.filter_on_grade(...grade_min_max);
    }

    render() {
	const { current_value, min, max, step, grade_names } = this.state;
	// console.log('filter render', current_value);
	return (
	    <React.Fragment>
		<ReactBootstrapSlider
		    id='grade-slider'
		    value={current_value}
		    change={this.on_value_change}
		    slideStop={this.on_value_change}
		    step={step}
		    max={max}
		    min={min}
		    />
		<span className='slider-min-max'>
		    <SliderValue id={'min'} value={grade_names[current_value[0]]} />
		    <SliderValue id={'max'} value={grade_names[current_value[1]]} />
		</span>
	    </React.Fragment>
	);
    }
}

var route_table = ReactDOM.render(
    <RouteTable/>,
    document.getElementById('route-table')
);

ReactDOM.render(
    <Filters route_table={route_table} />,
    document.getElementById('filters')
);
