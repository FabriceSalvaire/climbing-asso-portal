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
import ReactBootstrapSlider from 'react-bootstrap-slider';
import es6BindAll from 'es6bindall';

// import ReactBootstrapSlider from '../../externals/react-bootstrap-slider.jsx';

// import '../../tools/set.js';
import { FrenchGrade } from '../../tools/grade.js';
import { SliderWithValues } from './route-table-tpl.jsx';

/**************************************************************************************************/

export
class GradeFilter extends React.Component {
    constructor(props) {
	super(props);
	es6BindAll(this, ['on_value_change']);

	this._route_model = props.route_model;

	this._grade_names = Array.from(FrenchGrade.grade_iter(4, 8));
	this._grades = this._grade_names.map(name => new FrenchGrade(name));
	this._max = this._grades.length -1;

	this.state = {
	    current_value: [0, this._max]
	};

	// this.on_value_change = this.on_value_change.bind(this);
    }

    on_value_change(event) {
	var min_max = event.target.value;
	this.setState({ current_value: min_max });

	// Signal: slider -> table
	var grade_min_max = min_max.map(value => this._grades[value]);
	this._route_model.filter_on_grade(grade_min_max);
    }

    render() {
	const { current_value } = this.state;
	var [ min_grade, max_grade ] = current_value.map(i => this._grade_names[i]);
	var slider = (
	    <ReactBootstrapSlider
		value={current_value}
		change={this.on_value_change}
		slideStop={this.on_value_change}
		min={0}
		max={this._max}
		step={1}
		/>
	);
	return <SliderWithValues slider={slider} min={min_grade} max={max_grade} />;
    }
}

/**************************************************************************************************/

export
class PropertyFilter extends React.Component {
    constructor(props) {
	super(props);
	es6BindAll(this, ['_on_click', '_on_click_all', '_on_click_inverse', '_on_click_clear']);

	this._model = props.model;
	this._properties = this._model[props.properties];
	this._slot = props.slot;

	this.state = {
	    toggled: new Set(this._properties)
	};
    }

    _call_slot(toggled) {
	this._model[this._slot](toggled);
    }

    _on_click(property) {
	var toggled = new Set(this.state.toggled);
	if (toggled.has(property))
	    toggled.delete(property);
	else
	    toggled.add(property);
	this.setState({ toggled });

	toggled = Array.from(toggled);
	this._call_slot(toggled);
    }

    _on_click_all() {
	this.setState({ toggled: new Set(this._properties) });
	this._call_slot(null);
    }

    _on_click_inverse() {
	var toggled = this.state.toggled;
	toggled = new Set(this._properties.filter(x => !toggled.has(x)));
	this.setState({ toggled });

	toggled = Array.from(toggled);
	this._call_slot(toggled);
    }

    _on_click_clear() {
	this.setState({ toggled: new Set() });
	this._call_slot([]);
    }

    render() {
	const { toggled } = this.state;
	const buttons = this._properties.map(property => {
	    var class_name = 'btn btn-sm btn-' + (toggled.has(property) ? 'success' : 'danger');
	    return (
		<button key={property} type="button" className={class_name} onClick={() => this._on_click(property)}>{property}</button>
	    );
	});
	return (
	    <div className="btn-group" role="group" aria-label="">
		<button key='all' type="button" className="btn btn-secondary btn-sm" onClick={this._on_click_all}><i className="fas fa-check"></i></button>
		<button key='inverse' type="button" className="btn btn-secondary btn-sm" onClick={this._on_click_inverse}><i className="fas fa-retweet"></i></button>
		<button key='clear' type="button" className="btn btn-secondary btn-sm" onClick={this._on_click_clear}><i className="fas fa-trash-alt"></i></button>
		{buttons}
	    </div>
	);
    }
}
