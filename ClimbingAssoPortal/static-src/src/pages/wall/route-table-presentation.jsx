/**************************************************************************************************/

import React from 'react';

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
