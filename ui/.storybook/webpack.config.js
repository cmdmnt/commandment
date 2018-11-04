const path = require('path');

const {CheckerPlugin} = require('awesome-typescript-loader');

module.exports = (baseConfig, env, defaultConfig) => {
  defaultConfig.module.rules.push({
    test: /\.tsx?$/,
    include: path.resolve(__dirname, '../src'),
    loader: require.resolve('awesome-typescript-loader')
  });
  defaultConfig.plugins.push(new CheckerPlugin());
  defaultConfig.resolve.extensions.push('.ts', '.tsx');

  // defaultConfig.module.rules.push({
  //   test: /\.jsx?$/,
  //   include: [
  //     path.resolve(__dirname, "node_modules/semantic-ui-react"),
  //     path.resolve(__dirname, "node_modules/byte-size")
  //   ],
  //   loader: "babel-loader"
  // });

  return defaultConfig;
};

