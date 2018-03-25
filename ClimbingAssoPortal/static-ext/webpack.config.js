var path = require('path');

module.exports = {
    mode: 'development',
    // mode: 'production',

    entry: {
	test: './src/test.js',
	route_page: './src/pages/wall/route-page.js',
    },

    output: {
	path: path.resolve(__dirname, 'dist'),
	filename: '[name].js'
    },

    module: {
	rules: [
	    { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
	]
    },

    // devtool: 'source-map',

    watchOptions: {
	aggregateTimeout: 300,
	poll: 1000
    },

    stats: {
    }
};
