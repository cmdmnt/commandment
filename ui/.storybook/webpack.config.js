const path = require('path');

const {CheckerPlugin} = require('awesome-typescript-loader');

module.exports = (baseConfig, env, config) => {
  config.module.rules.push({
    test: /\.(ts|tsx)$/,
    include: path.resolve(__dirname, '../src'),
    loader: require.resolve('awesome-typescript-loader')
  });
  // config.plugins.push(new CheckerPlugin());
  config.resolve.extensions.push('.ts', '.tsx');

  return config;
};

