const Sequelize = require("sequelize");
const config = require('./config/relationalDb');
const { QueryTypes } = require('sequelize');

global.connection = new Sequelize(config);
const connection = global.connection;

module.exports = {}; 