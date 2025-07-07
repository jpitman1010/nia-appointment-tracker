import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  entry: './src/app.js',
  output: {
    path: path.resolve(__dirname, '../static/js'),
    filename: 'bundle.js',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  devtool: 'source-map',
  devServer: {
    static: {
      directory: path.resolve(__dirname, '../static'),
    },
    compress: true,
    port: 9000,
  },
  resolve: {
    extensions: ['.js'],
  },
  mode: 'development',
};
