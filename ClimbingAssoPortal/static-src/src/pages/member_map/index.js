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

/**************************************************************************************************
 *
 * Configuration Variables
 *
 *   var center = {longitude: ..., latitude: ...}
 *   var extent_margin = [1000, 1000]; // m
 *   var extent = null;
 *
 *   var geoportail_api_key = "...";
 *
 *   var show_edit_toolbar = false;

 * Inputs:
 *   - #map
 *   - #projection
 *   - #precision
 *   - #map-source
 *   - #map-toolbar label
 *   - #feature
 *
 * Targets:
 *   - mouse-position
 *
 */

/***************************************************************************************************
 *
 * Define Projections
 *
 */

// new OpenLayers.Projection('EPSG:4326');
var proj_4326 = ol.proj.get('EPSG:4326');
var proj_3857 = ol.proj.get('EPSG:3857');

/***************************************************************************************************
 *
 * Define the view extent
 *
 */

if (extent) {
    var center_in_mercator = [
	    .5*(extent[0] + extent[2]),
	    .5*(extent[1] + extent[3])
    ];
} else {
    var center_in_mercator = ol.proj.transform(
	[center.longitude, center.latitude],
	'EPSG:4326', 'EPSG:3857'
    );

    extent = [
	center_in_mercator[0] - extent_margin[0], center_in_mercator[1] - extent_margin[1],
	center_in_mercator[0] + extent_margin[0], center_in_mercator[1] + extent_margin[1]
    ]
}

var view_setup = {
    zoom: 15,
    center: center_in_mercator
}

/***************************************************************************************************
 *
 * Define some controls
 *
 */

var zoom_to_extent = new ol.control.ZoomToExtent({
    extent: extent
});

var scale_line_control = new ol.control.ScaleLine();

var full_screen_control = new ol.control.FullScreen();

// control is shown in the top right corner of the map
// css selector .ol-mouse-position.
// var mouse_position_control = new ol.control.MousePosition();

var mouse_position_target = document.getElementById('mouse-position');
var mouse_position_control = null;
if (mouse_position_target) {
    var mouse_position_control = new ol.control.MousePosition({
	coordinateFormat: ol.coordinate.createStringXY(4),
	projection: 'EPSG:4326',
	// comment the following two lines to have the mouse position be placed within the map.
	className: 'custom-mouse-position',
	target: mouse_position_target,
	undefinedHTML: '&nbsp;'
    });
}

var projection_select = $('#projection');
var precision_input = $('#precision');

function set_precision(value) {
    var format = ol.coordinate.createStringXY(value);
    if (mouse_position_control)
	mouse_position_control.setCoordinateFormat(format);
}

// Fixme: last_precision
var last_precision = precision_input.valueAsNumber;
projection_select.on('change', function() {
    var value = this.value;
    if (value == 'EPSG:3857') {
	last_precision = precision_input.valueAsNumber;
	precision_input.val(0);
	set_precision(0);
    }
    else if (value == 'EPSG:4326') {
	last_precision = 4;
	precision_input.val(last_precision);
	set_precision(last_precision);
    }
    if (mouse_position_control)
	mouse_position_control.setProjection(ol.proj.get(value));
});
if (mouse_position_control)
    projection_select.val(mouse_position_control.getProjection().getCode());

precision_input.on('change', function() {
    var value = this.valueAsNumber;
    last_precision = value;
    set_precision(value);
});


var controls = [
    zoom_to_extent,
    scale_line_control,
    full_screen_control
]
if (mouse_position_control)
    controls.push(mouse_position_control)

/***************************************************************************************************
 *
 * Setup Map
 *
 */

var map = new ol.Map({
    target: document.getElementById('map'),
    controls: ol.control.defaults({
	attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
	    collapsible: false
	})
    }).extend(controls),
    view: new ol.View(view_setup)
});

if (extent)
    map.getView().fit(extent, map.getSize());

/***************************************************************************************************
 *
 * Setup OSM Map
 *
 */

var osm_layer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: false
});

osm_layer.setVisible(true);
map.addLayer(osm_layer);

/***************************************************************************************************
 *
 * Setup IGN Map
 *
 */

var resolutions = [];
var matrix_ids = [];
var resolution_max = ol.extent.getWidth(proj_3857.getExtent()) / 256;

for (var i = 0; i < 18; i++) {
    matrix_ids[i] = i.toString();
    resolutions[i] = resolution_max / Math.pow(2, i);
}
console.log("Resolutions:", resolutions)

var tile_grid = new ol.tilegrid.WMTS({
    origin: [-20037508, 20037508],
    resolutions: resolutions,
    matrixIds: matrix_ids
});

var ign_attribution = new ol.Attribution({
    html: '<a href="http://www.geoportail.fr/" target="_blank">' +
	'<img src="http://api.ign.fr/geoportail/api/js/latest/' +
	'theme/geoportal/img/logo_gp.gif"></a>'
});

function ign_layer_factory(layer_settings) {
    var source = new ol.source.WMTS({
	url: 'http://wxs.ign.fr/' + geoportail_api_key + '/wmts',
	layer: layer_settings.layer_name,
	matrixSet: 'PM',
	format: layer_settings.image_format,
	projection: 'EPSG:3857',
	tileGrid: tile_grid,
	style: 'normal',
	attributions: [ign_attribution]
    });

    var layer = new ol.layer.Tile({
	source: source,
	visible: false
    });

    return layer;
}

var ign_layer_settings = [
    {layer_name: 'GEOGRAPHICALGRIDSYSTEMS.MAPS', image_format: 'image/jpeg'},
    {layer_name: 'ORTHOIMAGERY.ORTHOPHOTOS', image_format: 'image/jpeg'},
    {layer_name: 'GEOGRAPHICALGRIDSYSTEMS.PLANIGN', image_format: 'image/jpeg'},
    // {layer_name: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD', image_format: 'image/jpeg'},
    // {layer_name: 'TRANSPORTNETWORKS.ROADS', image_format: 'image/png'},
    // {layer_name: 'CADASTRALPARCELS.PARCELS', image_format: 'image/png'}
];

var ign_layers = [];
if (geoportail_api_key) {
    ign_layer_settings.forEach(function(layer_settings) {
	var layer = ign_layer_factory(layer_settings);
	if (layer_settings.layer_name == 'GEOGRAPHICALGRIDSYSTEMS.PLANIGN')
	    layer.setVisible(true);
	map.addLayer(layer);
	ign_layers.push(layer);
    });
}

var map_source_input = $('#map-source');
map_source_input.on('change', function() {
    var layer_name = this.value;
    // var layers = map.getLayers();
    ign_layers.forEach(function(layer) {
	layer.setVisible(layer.getSource().getLayer() == layer_name);
    });
});

/***************************************************************************************************
 *
 * Cluster
 *
 */

var feature_options = {
    'dataProjection': proj_4326,
    'featureProjection': proj_3857
};

var member_source = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function(extent, resolution, projection) {
	jQuery.getJSON("/member/member_city.json", function(data) {
	    var features = member_source.getFormat().readFeatures(data, feature_options);
	    for (var i = 0; i < features.length; i++) {
		var feature = features[i];
		// Clone N times the feature ...
		for (var j = 0; j < feature.get('member_count'); j++)
		    member_source.addFeature(feature.clone());
	    }
	})
    }
});

var cluster_source = new ol.source.Cluster({
    distance: 20,
    source: member_source
});

var style_cache = {};

function feature_style(feature) {
    var size = feature.get('features').length;
    var style = style_cache[size];
    if (!style) {
        style = new ol.style.Style({
	    image: new ol.style.Circle({
                radius: 10,
                stroke: new ol.style.Stroke({
		    color: '#fff'
                }),
                fill: new ol.style.Fill({
		    color: '#3399CC'
                })
	    }),
	    text: new ol.style.Text({
                text: size.toString(),
                fill: new ol.style.Fill({
		    color: '#fff'
                })
	    })
        });
        style_cache[size] = style;
    }
    return style;
}

var clusters = new ol.layer.Vector({
    source: cluster_source,
    style: feature_style
});
map.addLayer(clusters);
