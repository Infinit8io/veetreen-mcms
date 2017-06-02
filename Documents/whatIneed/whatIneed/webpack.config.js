"use strict";

const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = {
    context: __dirname,
    entry: {
        'main': './assets/main',
    },
    output: {
        path: path.resolve('./static/webpack_bundles'),
        filename: '[name]-[hash].js'
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            Tether: 'tether'
        }),
        new BundleTracker({filename: './webpack-stats.json'}),
        new ExtractTextPlugin('[name]-[contenthash].css'),
    ],
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                ['latest']
                            ]
                        }
                    }
                ]
            }, {
                test: /\.s?css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    loader: ['css-loader', 'sass-loader']
                })
            }
        ]
    }
}
