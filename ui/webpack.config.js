const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const extractSass = new ExtractTextPlugin({
    filename: "css/[name].css"
    //disable: process.env.NODE_ENV === "development"
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
                use: ['react-hot-loader/webpack', 'awesome-typescript-loader']
            },
            {
                test: /\.scss$/,
                use: extractSass.extract({
                    use: [{
                        loader: 'css-loader'
                    },  {
                        loader: 'resolve-url-loader'
                    },  {
                        loader: 'sass-loader?sourceMap'
                    }],
                    fallback: 'style-loader'
                })
            },
            {
                test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
                use: ['file-loader?publicPath=fonts/&outputPath=fonts/']
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