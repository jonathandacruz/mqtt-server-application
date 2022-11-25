const { QueryTypes } = require('sequelize');
const db = require('../db');

module.exports = {
    async loadIndex(req, res) {
        res.render(__dirname + "/../views/ejs/index.ejs");
    }
}