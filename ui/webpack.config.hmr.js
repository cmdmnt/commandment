const path = require('path');
const webpack = require('webpack');
const {CheckerPlugin} = require('awesome-typescript-loader');

module.exports = {
    entry: {
        app: [
            'react-hot-loader/patch',
            'webpack-dev-server/client?https://localhost:4000',
            'webpack/hot/only-dev-server',
            './src/entry.tsx'
        ]
    },

    output: {
        path: path.resolve(__dirname, "..", "commandment", "static"),
        filename: 'app.js',
        publicPath: 'https://localhost:4000/static/'
    },

    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.jsx']
    },

    devtool: 'cheap-module-eval-source-map',
    target: 'web',

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: ['react-hot-loader/webpack', 'awesome-typescript-loader']
            },
            {
                test: /\.scss$/,
                use: [{
                    loader: 'style-loader'
                }, {
                    loader: 'css-loader'
                }, {
                    loader: 'resolve-url-loader'
                }, {
                    loader: 'sass-loader',
                    options: {
                        sourceMap: true
                    }
                }]
            },
            {
                test: /\.(png|jpg|svg|gif)$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        limit: 10000,
                        name: '[name]-[hash].[ext]'
                    }
                }]
            },
            {
                test: /\.(ttf|eot|svg|woff|woff2)$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        publicPath: 'https://localhost:4000/static/fonts/',
                        outputPath: 'fonts/'
                    }
                }]
            }
        ]
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new CheckerPlugin()
    ],

    devServer: {
        // This must be a full hostname for HMR to work
        publicPath: "https://localhost:4000/static/",
        hot: true,
        port: 4000,
        https: true,
        headers: {
            'Access-Control-Allow-Origin': '*'
        }
    }
};