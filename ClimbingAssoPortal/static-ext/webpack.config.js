var path = require('path');

// https://webpack.js.org/plugins/extract-text-webpack-plugin
//   https://www.npmjs.com/package/extract-text-webpack-plugin
//   for webpack 4: npm i -D extract-text-webpack-plugin@next
var ExtractTextPlugin = require('extract-text-webpack-plugin');

// https://github.com/schmod/babel-plugin-angularjs-annotate
// https://github.com/babel/babel-loader

// https://webpack.js.org/plugins/commons-chunk-plugin
// https://webpack.js.org/plugins/compression-webpack-plugin

module.exports = {
    mode: 'development',
    // mode: 'production',

    externals: {
	jquery: 'jQuery',
	react: 'React',
	'react-dom': 'ReactDOM' // ,
	// 'react-bootstrap-slider': 'ReactBootstrapSlider'
    },

    // entry: ['babel-polyfill', './app/js']
    entry: {
	main: './src/main.js',
	route_page: './src/pages/wall/route-page.js',
	test: './src/test.js',
	route_page_react: './src/pages/wall/route-page.jsx'
    },

    output: {
	path: path.resolve(__dirname, 'dist'),
	filename: '[name].js'
    },

    module: {
	rules: [
	    {
		test: /\.(js|jsx)$/,
		exclude: /node_modules/,
		loader: "babel-loader"
	    },
            {
		// Match .css and .scss
                test:/\.(s*)css$/,
                use: ExtractTextPlugin.extract({
                        fallback:'style-loader',
                    use:[
			// 'style-loader',
			// { loader: 'css-loader', options: { importLoaders: 1 } },
			'css-loader',
			'sass-loader',
			'postcss-loader' // https://github.com/postcss/postcss-loader
		    ],
                })
            }
        ]
    },

    plugins: [
        new ExtractTextPlugin({filename:'[name].css'}),
    ],

    // devtool: 'source-map',

    watchOptions: {
	aggregateTimeout: 300,
	poll: 1000
    },

    stats: {
    }
};
