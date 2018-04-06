/***************************************************************************************************
 *
 *
 */

// var styles = {
//   // GeometryCollection
//   'foo': [new ol.style.Style({
//     image: new ol.style.Circle({
//       radius: 10,
//       fill: new ol.style.Fill({
// 	color: 'rgba(0, 0, 255, .5)'
//       }),
//       stroke: new ol.style.Stroke({
//         color: 'blue',
// 	width: 2
//       })
//     })
//   })],
// };

// var style_function = function(feature, resolution) {
//   // console.log("style_function: resolution =", resolution);
//   var object_type = feature.get('object');
//   if (object_type == '...') {
//     if (feature.get('...') == place_name)
// 	return styles['...'];
//   } else
//       return null;
// };

var feature_options = {
    'dataProjection': proj_4326,
    'featureProjection': proj_3857
};
// feature loader http://openlayersbook.github.io/ch05-using-vector-layers/example-03.html
// readProjection(geojson_object),

var member_geojson_source = new ol.source.Vector({
    features: (new ol.format.GeoJSON()).readFeatures(member_geojson, feature_options)
});
var member_geojson_layer = new ol.layer.Vector({
    source: member_geojson_source,
    style: style_function
});
map.addLayer(member_geojson_layer);

var cluster_source = new ol.source.Cluster({
    distance: 20,
    source: massif_geojson_source
});

var style_cache = {};

function has_current_place(features, member_name) {
    for (var i = 0; i < features.length; i++) {
	feature = features[i];
	if (feature.get('name') == place_name)
	    return true;
    }
    return false;
}

function make_cluster_style(size, colour) {
    return [new ol.style.Style({
	image: new ol.style.Circle({
	    radius: 10,
	    stroke: new ol.style.Stroke({
		color: '#fff'
	    }),
	    fill: new ol.style.Fill({
		color: colour
	    })
	}),
	text: new ol.style.Text({
	    text: size.toString(),
	    fill: new ol.style.Fill({
		color: '#fff'
	    })
	})
    })];
}

var cluster_style_function = function(feature, resolution) {
    // console.log("clusters style_function: resolution =", resolution);
    var features = feature.get('features');
    if (resolution > resolutions[14]) {
	var size = features.length;
	if (has_current_place(features, place_name)) {
	    return make_cluster_style(size, 'red');
	} else {
	    var style = style_cache[size];
	    if (!style) {
		style = make_cluster_style(size, '#3399CC');
		style_cache[size] = style;
	    }
	    return style;
	}
    } else {
	features = feature.get('features');
	feature = features[0];
	return style_function(feature, resolution);
    }
};

var clusters = new ol.layer.Vector({
    source: cluster_source,
    style: cluster_style_function
});
map.addLayer(clusters);

/***************************************************************************************************
 *
 *
 */

// Define styles

var normal_style = new ol.style.Style({
  image: new ol.style.Circle({
    radius: 4,
    fill: new ol.style.Fill({
      color: 'rgba(20,150,200,0.3)'
    }),
    stroke: new ol.style.Stroke({
      color: 'rgba(20,130,150,0.8)',
      width: 1
    })
  })
});

var selected_style = new ol.style.Style({
  image: new ol.style.Circle({
    radius: 40,
    fill: new ol.style.Fill({
      color: 'rgba(150,150,200,0.6)'
    }),
    stroke: new ol.style.Stroke({
      color: 'rgba(20,30,100,0.8)',
      width: 3
    })
  })
});

var selected_text_style_function = function(name, coordinate) {
  // var box_width = feature_name.length * ...;
  // var margin = box_width * ...;
  // map.getView().getResolution();
  return new ol.style.Style({
    // geometry: new ol.geom.Polygon([[[coordinate[0] -margin, coordinate[1] -margin],
    // 				   [coordinate[0] +margin, coordinate[1] -margin],
    // 				   [coordinate[0] +margin, coordinate[1] +margin],
    // 				   [coordinate[0] -margin, coordinate[1] +margin]
    // 				  ]]),
    // fill: new ol.style.Fill({
    //   color: '#FFF'
    // }),
    text: new ol.style.Text({
      font: '20px helvetica, sans-serif',
      text: name,
      fill: new ol.style.Fill({
        color: '#000'
      }),
      stroke: new ol.style.Stroke({
        color: '#fff', // #fff #DEFFCD #D1FEBB
        width: 20
      })
    })
  });
};

var selected_features = [];

// Unselect previous selected features
function unselect_previous_features() {
  var i;
  for(i=0; i < selected_features.length; i++) {
    selected_features[i].setStyle(null);
  }
  selected_features = [];
}

// Handle pointer
map.on('pointermove', function(event) {
  unselect_previous_features();
  map.forEachFeatureAtPixel(event.pixel, function(feature) {
    features = feature.get('features');
    if (features) {
      feature1 = features[0];
      feature_name = feature1.get('name');
      if (features.length > 1)
	feature_name += ' ...' // fixme: unicode
      coordinate = feature1.getGeometry().getCoordinates();
    } else {
      var object_type = feature.get('object');
      if (object_type == '...') {
	feature_name = feature.get('...');
      } else
	feature_name = feature.get('name');
      coordinate = feature.getGeometry().getCoordinates();
    }

    feature.setStyle([
      // selected_style,
      selected_text_style_function(feature_name, coordinate)
    ]);
    selected_features.push(feature);
  });
});

/***************************************************************************************************
 *
 *
 */

if (show_edit_toolbar) {

  var style_function_custom = function(feature, resolution) {
    return [new ol.style.Style({
      image: new ol.style.Circle({
        radius: 10,
        fill: new ol.style.Fill({
  	color: 'rgba(255, 0, 255, .5)'
        }),
        stroke: new ol.style.Stroke({
          color: 'blue',
  	width: 2
        })
      })
    })]
  }

  var custom_source = new ol.source.Vector({
    features: new ol.format.GeoJSON()
  });

  var custom_layer = new ol.layer.Vector({
    source: custom_source,
    style: style_function_custom
  });
  map.addLayer(custom_layer);

  var interaction;
  $('#map-toolbar label').on('click', function(event) {
    map.removeInteraction(interaction);

    var id = event.target.id;
    switch(id) {
    case "select":
      interaction = new ol.interaction.Select();
      map.addInteraction(interaction);
      break;

    case "point":
      interaction = new ol.interaction.Draw({
        type: 'Point',
        source: custom_source
      });
      map.addInteraction(interaction);
      interaction.on('drawend', onDrawEnd);
      break;

    case "modify":
      interaction = new ol.interaction.Modify({
        features: new ol.Collection(custom_source.getFeatures())
      });
      map.addInteraction(interaction);
      break;

    default:
      break;
    }
  });

  var current_feature = null;
  var feature_modal = $('#feature-modal');
  var feature_wgs84_position = feature_modal.find('#feature-wsg84-position');
  var feature_mercator_position = feature_modal.find('#feature-mercator-position');
  var feature_name_group = feature_modal.find('#feature-name-group');
  var feature_name_input = feature_modal.find('#feature-name');
  var feature_category_input = feature_modal.find('#feature-category');
  var feature_note_input = feature_modal.find('#feature-note');
  var cancel_feature_button = feature_modal.find('#cancel-feature-button');
  var save_feature_button = feature_modal.find('#save-feature-button');
  var download_feature_button = $("#download-feature-button");
  var number_of_features_label = $("#number-of-features");

  function show_feature_modal(feature) {
    current_feature = feature;
    mercator_coordinate = feature.getGeometry().getCoordinates();
    coordinate = ol.proj.transform(mercator_coordinate, 'EPSG:3857', 'EPSG:4326');
    feature_wgs84_position.text(coordinate[0].toFixed(5) + ', ' + coordinate[1].toFixed(5))
    feature_mercator_position.text(mercator_coordinate[0].toFixed(0) + ', ' + mercator_coordinate[1].toFixed(0))
    feature_modal.modal();
  }

  function hide_feature_modal() {
    feature_modal.modal('hide');
    feature_name_group.removeClass('has-error')
    feature_name_input.removeClass('form-control-error')
    features = custom_source.getFeatures();
    number_of_features_label.text(features.length.toString());
    feature_name_input.val('');
    feature_note_input.val('');
    current_feature = null;
  }

  function onDrawEnd(event) {
    show_feature_modal(event.feature);
  }

  save_feature_button.on('click', function(event) {
    var name = feature_name_input.val();
    if (name) {
      current_feature.set('name', name);
      current_feature.set('category', feature_category_input.val());
      current_feature.set('note', feature_note_input.val());
      hide_feature_modal();
    }
    else {
      feature_name_group.addClass('has-error')
      feature_name_input.addClass('form-control-error')
    }
  });

  cancel_feature_button.on('click', function(event) {
    custom_source.removeFeature(current_feature)
    hide_feature_modal();
  });

  download_feature_button.click(function(event) {
    var obj_geojson = (new ol.format.GeoJSON()).writeFeatures(custom_source.getFeatures(), feature_options);
    var obj_json = JSON.stringify(obj_geojson);
    var blob = new Blob([obj_geojson], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "bleau-geo.json");
  });
}
