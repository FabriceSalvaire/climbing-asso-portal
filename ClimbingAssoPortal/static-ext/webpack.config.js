var path = require('path');

module.exports = {
    mode: 'development',
    // mode: 'production',

    entry: {
	route_page: './src/route-page.js',
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
