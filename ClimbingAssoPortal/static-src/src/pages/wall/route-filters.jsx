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

import { FrenchGrade } from '../../tools/grade.js';
import { SliderWithValues } from './route-table-tpl.jsx';

/**************************************************************************************************/

export
class GradeFilter extends React.Component {
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
	this.route_model.filter_on_grade(grade_min_max);
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

/**************************************************************************************************/

export
class ProfileFilter extends React.Component {
    constructor(props) {
	super(props);
	// es6BindAll(this, ['']);

	this.route_model = props.route_model;

	this.state = {
	};
    }

    render() {
	return <div></div>;
    }
}

