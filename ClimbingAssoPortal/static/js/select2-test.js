// $( "#dropdown" ).select2({
//     theme: "bootstrap4"
// });

// $.fn.select2.defaults.set( "theme", "bootstrap4" );

$(document).ready(function() {
    $('.js-example-basic-single').select2();

    $('.route-name').select2({
        ajax: {
	    // https://api.github.com/search/repositories?term=sel&_type=query&q=sel
            url: '/api/route/',
            // dataType: 'json',
	    processResults: function (data) {
		var routes = data.results;
		var results = [];
		for (var i=0;i<routes.length;i++) {
		    var route = routes[i];
		    if (route.name) {
			results.push({
			    id: i,
			    text: route.name
			})
		    }
		}
		console.log(results);
		return {
                    results: results
		};
            }
	}
    });
});
