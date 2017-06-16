const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const extractSass = new ExtractTextPlugin({
    filename: "css/[name].css"
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
        filename: 'app.js',
        publicPath: '/static/'
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
                use: ['awesome-typescript-loader']
            },
            {
                test: /\.scss$/,
                use: extractSass.extract({
                    use: [{
                        loader: 'css-loader'
                    }, {
                        loader: 'resolve-url-loader'
                    }, {
                        loader: 'sass-loader?sourceMap'
                    }],
                    fallback: 'style-loader'
                })
            },
            {
                test: /\.css$/,
                use: extractSass.extract({
                    use: [{
                        loader: 'css-loader'
                    }, {
                        loader: 'resolve-url-loader'
                    }]
                })
            },
            {
                test: /\.(png|jpg|svg|gif)$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        limit: 10000,
                        name: '[name]-[hash].[ext]',
                        outputPath: 'images/'
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
        extractSass
    ]
};