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

import React from 'react';
import ReactDOM from 'react-dom';

import { RouteModel } from './route-model.js';
import { GradeFilter, PropertyFilter } from './route-filters.jsx';
import { RouteTable } from './route-table.jsx';

/**************************************************************************************************/

// import { injectIntl, defineMessages } from 'react-intl';

// const messages = defineMessages({
//   widget1Header: {
//     id: 'Widgets.widget1.header',
//     defaultMessage: 'Creative header',
//   },
//   widget1Body: {
//     id: 'Widgets.widget1.body',
//     defaultMessage: 'Mark todays date: {date}',
//   },
// });

/**************************************************************************************************/

var route_model = new RouteModel('/api/routes/?limit=1000');

var route_table = ReactDOM.render(
    <RouteTable model={route_model} />,
    document.getElementById('route-table')
);

ReactDOM.render(
    <GradeFilter route_model={route_model} />,
    document.getElementById('grade-filter')
);

ReactDOM.render(
    <PropertyFilter model={route_model} properties='profiles' slot='filter_on_profile' />,
    document.getElementById('profile-filter')
);

ReactDOM.render(
    <PropertyFilter model={route_model} properties='inclinations' slot='filter_on_inclination' />,
    document.getElementById('inclination-filter')
);
