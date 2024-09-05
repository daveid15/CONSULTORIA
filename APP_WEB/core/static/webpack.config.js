const path = require("path");
const autoprefixer = require("autoprefixer");
const {WebpackManifestPlugin} = require("webpack-manifest-plugin");
const {CleanWebpackPlugin} = require("clean-webpack-plugin");

module.exports = [{
    entry: {
        // This is necessary for webpack to compile
        // But we never use style-bundle.js
        style: ["./lib/styles.scss"],
        app: ["./lib/app.js"],
        onboarding: ["./lib/onboarding.js"],
        login: ["./lib/login.js"],
        sidebar: ["./lib/sidebar.js"],
        calendar: ["./lib/calendar.js"],
        purchase: ["./lib/purchase.js"],
        "pyme-data": ["./lib/pyme-data.js"],
        "account-pyme": ["./lib/account-pyme.js"],
        password: ["./lib/password.js"],
        services: ["./lib/services.js"],
        "inner-services": ["./lib/inner-services.js"],
    },
    output: {
        path: path.resolve(__dirname, "./dist"),
        publicPath: "/dist/",
        filename: "[name]-[hash].js"
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "[name]-[hash].css"
                        }
                    },
                    {
                        loader: "extract-loader"
                    },
                    {
                        loader: "css-loader"
                    },
                    {
                        // Run postcss actions
                        loader: "postcss-loader",
                        options: {
                            // `postcssOptions` is needed for postcss 8.x;
                            // if you use postcss 7.x skip the key
                            postcssOptions: {
                                // postcss plugins, can be exported to postcss.config.js
                                plugins: [
                                        autoprefixer()
                                    ]
                            }
                        }
                    },
                    {
                        // compiles Sass to CSS
                        loader: "sass-loader"
                    }
                ]
            },
            {
                test: /\.(png|jpg|gif|svg)$/i,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                        },
                    },
                ],
            },
            {
                test: /\.js$/,
                loader: "babel-loader",
                options: {
                    presets: [
                        "@babel/preset-env"
                    ]
                }
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(), // removes outdated assets from the output dir
        new WebpackManifestPlugin(),  // generates the required manifest.json file
    ],
    watch: false,
    mode: "development"
}];