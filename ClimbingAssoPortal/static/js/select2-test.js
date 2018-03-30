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
            url: '/api/members/',
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
	    		id: i,
	    		text: member.address
	    	    })
	    	}
	    	console.log(results);
	    	return {
                    results: results
	    	};
            }
	}
    });
});
