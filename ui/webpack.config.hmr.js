const path = require('path');

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
        use: [{
            loader: 'style-loader'
          }, {
            loader: 'css-loader'
          }, {
            loader: 'resolve-url-loader'
          }, {
            loader: 'sass-loader?sourceMap'
          }]
      },
      {
        test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
        use: ['file-loader?publicPath=fonts/&outputPath=fonts/']
      }
    ]
  },

  devServer: {
    publicPath: "https://localhost:4000/static/",
    hot: true,
    port: 4000,
    https: true
  }
};