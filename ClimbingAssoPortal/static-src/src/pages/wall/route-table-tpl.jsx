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

import { hold_colours } from './hold-colour.js';

/**************************************************************************************************/

const SliderValue = ({ id, value }) => (
    <p className={'slider-value-' + id}>{value}</p>
);

const SliderMinMaxValue = ({ min, max }) => (
    <span className='slider-min-max'>
	<SliderValue id={'min'} value={min} />
	<SliderValue id={'max'} value={max} />
    </span>
);

export
const SliderWithValues = ({ slider, min, max }) => (
    <React.Fragment>
	{slider}
	<SliderMinMaxValue min={min} max={max} />
    </React.Fragment>
);

export
function RouteRow({ route }) {
    var class_name = 'hold-colour hold-colour-' + hold_colours[route.colour];
    return (
	<tr >
	    <th scope="row"><a href="">{route.line_number}</a></th>
	    <td>{route.grade}</td>
	    <td><div className={class_name}></div></td>
	    <td>{route.name}</td>
	    <td>{route.comment}</td>
	    <td>{route.opener}</td>
	    <td>{route.opening_date}</td>
	</tr>
    );
}
