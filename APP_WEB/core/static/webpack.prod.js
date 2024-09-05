const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const {WebpackManifestPlugin} = require("webpack-manifest-plugin");
const {CleanWebpackPlugin} = require("clean-webpack-plugin");

module.exports = merge(common, {
    plugins: [
        new CleanWebpackPlugin(), // removes outdated assets from the output dir
        new WebpackManifestPlugin(),  // generates the required manifest.json file
    ],
    watch: false,
    mode: "production"
});