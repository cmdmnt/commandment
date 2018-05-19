const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const {CheckerPlugin} = require('awesome-typescript-loader');
const {createLodashTransformer} = require('typescript-plugin-lodash');
const lodashTransformer = createLodashTransformer();

const extractSass = new ExtractTextPlugin({
  filename: "css/[name].css"
});

module.exports = {
  entry: {
    app: [
      './src/entry.tsx'
    ]
  },

  output: {
    path: path.resolve(__dirname, "..", "commandment", "static"),
    filename: 'app.js',
    publicPath: '/static/'
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
  target: 'web',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: [{
          loader: 'awesome-typescript-loader',
          options: {
            errorsAsWarnings: true
          }
        }]
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
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    }),
    extractSass,
    new CheckerPlugin(),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new webpack.optimize.UglifyJsPlugin()
  ]
};