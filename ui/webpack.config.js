if (process.env.NODE_ENV === "production") {
  console.log('using config from ./webpack.config.prod');
  module.exports = require('./webpack.config.prod');
} else {
  console.log('using config from ./webpack.config.hmr');
  module.exports = require('./webpack.config.hmr');
}
