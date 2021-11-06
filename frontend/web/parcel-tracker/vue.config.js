const path = require('path');
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
//   .BundleAnalyzerPlugin;

module.exports = {
  lintOnSave: false,
  publicPath:
    process.env.NODE_ENV === 'production'
      ? process.env.VUE_APP_CDN_URL
      : '/static/',
  outputDir: '../../static',
  devServer: {
    sockPort: 8080,
    writeToDisk: true,
    proxy: {
      '^/': {
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  configureWebpack: {
    plugins: [
      // new BundleAnalyzerPlugin()
    ],
    resolve: {
      alias: {
        web: path.resolve(__dirname, './src'),
        ...(process.env.NODE_ENV === 'test'
          ? { indexof: 'component-indexof/index' }
          : {}),
      },
    },
  },
  css: {
    loaderOptions: {
      postcss: {
        config: {
          path: './postcss.config.js',
        },
      },
      scss: {
        implementation: require('node-sass'),
      },
    },
  },
};
