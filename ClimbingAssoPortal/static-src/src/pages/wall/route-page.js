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

import * as AliceMilliatWall from "./alice-milliat-wall.js";
import * as HoldColour from "./hold-colour.js";
// import * as RouteController from "./route-controller.js";

console.log('HoldColour', HoldColour.hold_colours);

// cf. http://django-angular.readthedocs.io/en/latest/integration.html
// https://docs.djangoproject.com/en/2.0/ref/csrf/

export var application = angular.module('route_index', ['ngCookies', 'ngResource']);

// Ajax requests shall send this HTTP-Header
application.config(/* @ngInject */ $httpProvider => {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

application.factory('Route', /* @ngInject */ $resource => {
    // Fixme: angularjs can remove trailing / -> useless redirection
    return $resource('/api/routes/?limit=1000', {}, {
	query: {
	    method: 'GET',
	    // params: {},
	    isArray: false
	}
    });
});

application.controller('route_controller', /* @ngInject */ ($scope, Route) => {
    $scope.routes = [];
    var query = Route.query();
    query.$promise.then(
    	result => {
    	    console.log('result:', result);
    	    angular.forEach(result.results, item => {
    		$scope.routes.push(item);
    	    });
    	},
    	results => {
    	    console.log('error:', result);
    	}
    );
});
