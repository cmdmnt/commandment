const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const extractSass = new ExtractTextPlugin({
    filename: "[name].[contenthash].css",
    disable: process.env.NODE_ENV === "development"
});


module.exports = {
    entry: {
        app: [
            'react-hot-loader/patch',
            './src/entry.tsx'
        ]
    },

    output: {
        path: path.resolve(__dirname, "..", "commandment", "static"),
        filename: 'bundle.js',
        publicPath: '/static/'
    },

    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.jsx']
    },

    devtool: 'source-map',
    target: 'web',

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                loaders: ['react-hot-loader/webpack', 'awesome-typescript-loader']
            },
            {
                test: /\.scss$/,
                use: extractSass.extract({
                    use: [{
                        loader: 'style-loader'
                    }, {
                        loader: 'css-loader'
                    }, {
                        loader: 'sass-loader'
                    }],
                    fallback: 'style-loader'
                })
            }
        ]
    },

    plugins: [
        extractSass
    ],

    devServer: {
        publicPath: "https://localhost:4000/static/",
        hot: true,
        port: 4000,
        https: true
    }
};