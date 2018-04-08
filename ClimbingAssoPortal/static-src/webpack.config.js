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

// const NODE_ENV = process.env.NODE_ENV || 'production';
// const NODE_ENV = 'production';
const NODE_ENV = 'development';

const is_development = NODE_ENV === 'development';

// set default Babel preset
if (!process.env.BABEL_ENV)
    process.env.BABEL_ENV = 'latest-browser';
console.log('Babel will use', process.env.BABEL_ENV);

/**************************************************************************************************/

var path = require('path');

// https://github.com/FormidableLabs/webpack-dashboard
// run using : npx webpack-dashboard webpack ...
const DashboardPlugin = require('webpack-dashboard/plugin');

// https://webpack.js.org/plugins/extract-text-webpack-plugin
//   https://www.npmjs.com/package/extract-text-webpack-plugin
//   for webpack 4: npm i -D extract-text-webpack-plugin@next
var ExtractTextPlugin = require('extract-text-webpack-plugin');

/**************************************************************************************************/

// https://webpack.js.org/plugins/commons-chunk-plugin
// https://webpack.js.org/plugins/compression-webpack-plugin
// https://github.com/waysact/webpack-subresource-integrity
// https://github.com/mikechau/sri-stats-webpack-plugin

/**************************************************************************************************/

const babel_config = {
    babelrc: false,

    env: {
	browser: {
	    presets: ['es2015', 'react', 'stage-2'],
	    plugins: []
	},

	'latest-browser': {
	    presets: [
		['env', {
		    targets: {
			browsers: ['last 2 versions']
		    },
		    // debug: true
		}],
 		'react',
		'stage-2',
  	    ],
	    plugins: []
	},

	node: {
	    presets: [
		['env', {
		    targets: {
			node: '8.10'
		    }
		}],
 		'react',
 		'stage-2',
	    ]
	}
    }
}

/***************************************************************************************************
 *
 * Boostrap Compilation
 *
 */

// "css-compile": "node-sass --output-style expanded --source-map true --source-map-contents true --precision 6 scss/bootstrap.scss dist/css/bootstrap.css
// "css-prefix": "postcss --config build/postcss.config.js --replace \"dist/css/*.css\" \"!dist/css/*.min.css\"",
// "css-minify": "cleancss --level 1 --source-map --source-map-inline-sources --output dist/css/bootstrap.min.css dist/css/bootstrap.css

/**************************************************************************************************/

const css_loader_options = (() => {
    if (is_development)
	return {}
    else
	return {
	// importLoaders: 1,

	// http://cssnano.co
	minimize: {
	    discardComments: {
		removeAll: true
	    }
	}
    }
})();

/**************************************************************************************************/

// https://github.com/michael-ciniawsky/postcss-load-config
const postcss_options = {
    // parser: 'sugarss', // https://github.com/postcss/sugarss
    plugins: [
	// require('postcss-cssnext')(),

	// https://github.com/postcss/autoprefixer
    	require('autoprefixer')({
	    cascade: false
	}),
    ]
};

/**************************************************************************************************/

let config = {
    mode: NODE_ENV,

    // entry: ['babel-polyfill', './app/js']
    entry: {
	common: './src/common/index.js',
	admin: './src/admin/index.js',
	member_map: './src/pages/member_map/index.js',
	rest_framework: './src/rest_framework/index.js',
	route_page_react: './src/pages/wall/route-page.jsx',
	select2_test: './src/pages/select2_test.js',
	test: './src/test.js',
    },

    output: {
	path: path.resolve(__dirname, '..', 'static'),
	filename: 'js/[name].js'
    },

    module: {
	rules: [
	    {
		test: /\.(js|jsx)$/,
		exclude: /(node_modules|packages)/,
		use: {
		    // https://github.com/babel/babel-loader
		    loader: 'babel-loader',
		    options: babel_config
		}
	    },
            {
		// Match .css and .scss
                test:/\.(s*)css$/,
		// https://github.com/webpack-contrib/extract-text-webpack-plugin
                use: ExtractTextPlugin.extract({
		    use: [
			// scss files > sass-loader > postcss-loader > css-loader > ExtractTextPlugin
			// { loader: "style-loader" },
			{
			    loader: 'css-loader',
			    options: css_loader_options
			},
			{
			    // https://github.com/postcss/postcss-loader
			    loader: 'postcss-loader',
			    options: postcss_options
			},
			{
			    // https://github.com/webpack-contrib/sass-loader
			    // https://github.com/sass/node-sass
			    loader: 'sass-loader',
			    options: {
				outputStyle: 'expanded',
				// sourceMap: true,
				// sourceMapContents: true,
				precision: 6,
			        // includePaths: ['...', ]
			    }
			},
		    ],
		    // https://github.com/webpack-contrib/style-loader
                    // use style-loader in development
                    // fallback: 'style-loader'
                })
            }
        ]
    },

    externals: {
	jquery: 'jQuery',
	react: 'React',
	'react-dom': 'ReactDOM' // ,
	// 'react-bootstrap-slider': 'ReactBootstrapSlider'
    },

    resolve: {
	alias: {
	    // Exclude JQuery form bootstrap-slider
	    // cf. https://github.com/seiyria/bootstrap-slider#how-do-i-exclude-the-optional-jquery-dependency-from-my-build
            'jquery': path.join(__dirname, './src/stubs/jquery-stub.js')
	}
    },

    plugins: [
	new DashboardPlugin(),
        new ExtractTextPlugin({
	    filename: 'css/[name].css'
	}),
    ],

    // devtool: 'source-map',

    watchOptions: {
	aggregateTimeout: 300,
	poll: 1000
    },

    // stats: 'verbose',
    stats: 'normal',

    // stats: {
    // 	// fallback value for stats options when an option is not defined (has precedence over local webpack defaults)
    // 	all: undefined,
    // 	// Add asset Information
    // 	assets: true,
    // 	// Sort assets by a field
    // 	// You can reverse the sort with `!field`.
    // 	assetsSort: 'field',
    // 	// Add build date and time information
    // 	builtAt: true,
    // 	// Add information about cached (not built) modules
    // 	cached: true,
    // 	// Show cached assets (setting this to `false` only shows emitted files)
    // 	cachedAssets: true,
    // 	// Add children information
    // 	children: true,
    // 	// Add chunk information (setting this to `false` allows for a less verbose output)
    // 	chunks: true,
    // 	// Add built modules information to chunk information
    // 	chunkModules: true,
    // 	// Add the origins of chunks and chunk merging info
    // 	chunkOrigins: true,
    // 	// Sort the chunks by a field
    // 	// You can reverse the sort with `!field`. Default is `id`.
    // 	chunksSort: 'field',
    // 	// Context directory for request shortening
    // 	context: '../src/',
    // 	// `webpack --colors` equivalent
    // 	colors: false,
    // 	// Display the distance from the entry point for each module
    // 	depth: false,
    // 	// Display the entry points with the corresponding bundles
    // 	entrypoints: false,
    // 	// Add --env information
    // 	env: false,
    // 	// Add errors
    // 	errors: true,
    // 	// Add details to errors (like resolving log)
    // 	errorDetails: true,
    // 	// Exclude assets from being displayed in stats
    // 	// This can be done with a String, a RegExp, a Function getting the assets name
    // 	// and returning a boolean or an Array of the above.
    // 	excludeAssets: 'filter' | /filter/ | (assetName) => ... return true|false |
    // 	    ['filter'] | [/filter/] | [(assetName) => ... return true|false],
    // 	// Exclude modules from being displayed in stats
    // 	// This can be done with a String, a RegExp, a Function getting the modules source
    // 	// and returning a boolean or an Array of the above.
    // 	excludeModules: 'filter' | /filter/ | (moduleSource) => ... return true|false |
    // 	    ['filter'] | [/filter/] | [(moduleSource) => ... return true|false],
    // 	// See excludeModules
    // 	exclude: 'filter' | /filter/ | (moduleSource) => ... return true|false |
    // 	    ['filter'] | [/filter/] | [(moduleSource) => ... return true|false],
    // 	// Add the hash of the compilation
    // 	hash: true,
    // 	// Set the maximum number of modules to be shown
    // 	maxModules: 15,
    // 	// Add built modules information
    // 	modules: true,
    // 	// Sort the modules by a field
    // 	// You can reverse the sort with `!field`. Default is `id`.
    // 	modulesSort: 'field',
    // 	// Show dependencies and origin of warnings/errors (since webpack 2.5.0)
    // 	moduleTrace: true,
    // 	// Show performance hint when file size exceeds `performance.maxAssetSize`
    // 	performance: true,
    // 	// Show the exports of the modules
    // 	providedExports: false,
    // 	// Add public path information
    // 	publicPath: true,
    // 	// Add information about the reasons why modules are included
    // 	reasons: true,
    // 	// Add the source code of modules
    // 	source: true,
    // 	// Add timing information
    // 	timings: true,
    // 	// Show which exports of a module are used
    // 	usedExports: false,
    // 	// Add webpack version information
    // 	version: true,
    // 	// Add warnings
    // 	warnings: true,
    // 	// Filter warnings to be shown (since webpack 2.4.0),
    // 	// can be a String, Regexp, a function getting the warning and returning a boolean
    // 	// or an Array of a combination of the above. First match wins.
    // 	warningsFilter: 'filter' | /filter/ | ['filter', /filter/] | (warning) => ... return true|false
    // }
};

/**************************************************************************************************/

module.exports = config;
