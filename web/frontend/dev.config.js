const path = require('path');

module.exports = {
  env: {
    NODE_ENV: 'development',
    DEBUG: true,
  },
  
  webpack: (config, { dev, isServer }) => {
    // Add development-specific webpack configurations
    if (dev) {
      config.devtool = 'eval-source-map';
    }

    // Add custom rules for development
    config.module.rules.push({
      test: /\.(ogg|mp3|wav|mpe?g)$/i,
      exclude: config.exclude,
      use: [
        {
          loader: 'url-loader',
          options: {
            limit: 8192,
            name: '[path][name].[ext]',
          },
        },
      ],
    });

    return config;
  },

  // Development server configuration
  devServer: {
    hot: true,
    port: 3000,
    host: 'localhost',
    open: true,
    historyApiFallback: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        pathRewrite: { '^/api': '/api/v1' },
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },

  // Enable detailed error reporting
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },

  // Enable TypeScript type checking
  typescript: {
    ignoreBuildErrors: false,
  },

  // Development performance optimizations
  optimization: {
    removeAvailableModules: false,
    removeEmptyChunks: false,
    splitChunks: false,
  },

  // Development-specific features
  features: {
    buildIndicator: true,
    compilationProgress: true,
  },
};

