module.exports = function(api) {
  api.cache(true);

  return {
    plugins: [
      "@babel/plugin-proposal-export-default-from",
      "@babel/plugin-syntax-jsx",
      "@babel/plugin-transform-react-jsx",
      "@babel/plugin-transform-react-display-name",
      "@babel/plugin-proposal-class-properties",
      "@babel/plugin-proposal-export-namespace-from",
    ],
    presets: [

    ],
  };
};