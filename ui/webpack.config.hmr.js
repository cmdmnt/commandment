const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const {CheckerPlugin} = require('awesome-typescript-loader');

module.exports = {
    entry: {
        app: [
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
        extensions: ['.ts', '.tsx', '.js', '.jsx'],
      alias: { // avoid lodash duplication: https://www.contentful.com/blog/2017/10/27/put-your-webpack-bundle-on-a-diet-part-3/
        'lodash-es': 'lodash',
        'lodash.get': 'lodash/get',
        'lodash.isfunction': 'lodash/isFunction',
        'lodash.isobject': 'lodash/isObject',
        'lodash.merge': 'lodash/merge',
        'lodash.reduce': 'lodash/reduce',
        'lodash.set': 'lodash/set',
        'lodash.unset': 'lodash/unset'
      }
    },

    devtool: 'cheap-module-eval-source-map',
    target: 'web',

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: ['awesome-typescript-loader'] // 'react-hot-loader/webpack',
            },
            {
                test: /\.js$/,
              include: [
                path.resolve(__dirname, "node_modules/semantic-ui-react"),
                path.resolve(__dirname, "node_modules/byte-size")
              ],
                loader: "babel-loader"
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
                        outputPath: 'fonts/'
                    }
                }]
            }
        ]
    },
    plugins: [
        new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/), // Reduces size by not including all locales
        new webpack.HotModuleReplacementPlugin(),
        new CheckerPlugin()
    ],

    devServer: {
        // This must be a full hostname for HMR to work
        publicPath: "https://localhost:4000/static/",
        hot: true,
        port: 4000,
        disableHostCheck: true,
        https: {
          key: fs.readFileSync('../ssl/server.key'),
          cert: fs.readFileSync('../ssl/server.crt'),
          ca: fs.readFileSync('../ssl/ca.crt')
        },
        headers: {
            'Access-Control-Allow-Origin': '*'
        }
    }
};