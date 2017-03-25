const path = require('path');

module.exports = {
  entry: {
    app: [
      'react-hot-loader/patch',
      './entry.ts'
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
      }
    ]
  }
};