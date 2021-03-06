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

// $( "#dropdown" ).select2({
//     theme: "bootstrap4"
// });

// $.fn.select2.defaults.set( "theme", "bootstrap4" );

$(document).ready(function() {
    $('.js-example-basic-single').select2();

    $('#city-using-admin-autocomplete').select2({
        ajax: {
	    // ?term=sel&_type=query&q=sel
	    url: '/admin/ClimbingAssoPortal/frenchcity/autocomplete/',
	}
    });

    $('#member-using-admin-autocomplete').select2({
        ajax: {
	    // ?term=sel&_type=query&q=sel
	    url: '/admin/ClimbingAssoPortal/member/autocomplete/',
	}
    });

    $('#member-using-rest').select2({
        ajax: {
            url: '/api/member_auto_complete/',
            dataType: 'json',
	    data: function (params) {
		var query = {
		    search: params.term,
		}
		return query;
	    },
	    processResults: function (data) {
	    	var members = data.results;
		console.log(members);
	    	var results = [];
	    	for (var i = 0; i < members.length; i++) {
	    	    var member = members[i];
	    	    results.push({
	    		id: member.pk,
	    		text: member.last_first_name
	    	    })
	    	}
	    	return {
                    results: results
	    	};
            }
	}
    });

    $('#ban').select2({
        ajax: {
            url: 'http://api-adresse.data.gouv.fr/search/',
            dataType: 'json',
	    data: function (params) {
		var query = {
		    q: params.term,
		    limit: 10,
		    type: 'housenumber',
		    // type: 'street',
		    postcode: 95870
		    // type: 'municipality'
		}
		return query;
	    },
	    processResults: function (data) {
		console.log('data', data);
	    	var features = data.features;
		console.log('features', features);
	    	var results = [];
	    	for (var i = 0; i < features.length; i++) {
	    	    var feature = features[i];
		    console.log('feature', feature);
	    	    results.push({
	    		id: i,
	    		text: feature.properties.label
	    	    })
	    	}
	    	return {
                    results: results
	    	};
            }
	}
    });
});
