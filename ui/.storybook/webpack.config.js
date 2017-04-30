// you can use this file to add your custom webpack plugins, loaders and anything you like.
// This is just the basic way to add addional webpack configurations.
// For more information refer the docs: https://getstorybook.io/docs/configurations/custom-webpack-config
const webpack = require('webpack');

let genDefaultConfig = require('@kadira/storybook/dist/server/config/defaults/webpack.config.js');

// IMPORTANT
// When you add this file, we won't add the default configurations which is similar
// to "React Create App". This only has babel loader to load JavaScript.
const {CheckerPlugin} = require('awesome-typescript-loader');

module.exports = function(config, env) {
    let defaultConfig = genDefaultConfig(config, env);

    defaultConfig.plugins = defaultConfig.plugins.concat(new CheckerPlugin());
    defaultConfig.module.loaders.push({
        test: /\.tsx?$/,
        loaders: ['react-hot-loader/webpack', 'awesome-typescript-loader']
    });
    
    defaultConfig.resolve.extensions = defaultConfig.resolve.extensions.concat(
        ['.ts', '.tsx', '.js', '.jsx']
    );
    
    return defaultConfig;
};


