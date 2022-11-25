const { QueryTypes } = require('sequelize');
const db = require('../db');

module.exports = {
    async loadEquipamentosAjax(req, res) {
        let dados = await global.connection.query(`select *, extract (EPOCH from (now() - dt_exec)) as diference from alarme where comando is null`, { type: QueryTypes.SELECT});
        res.json({dados});
    },
    async loadEquipamentosLogs (req, res) {
        let dados = await global.connection.query(`select * from alarme`, { type: QueryTypes.SELECT});
        res.json({dados});
    },
    async loadEquipamentosStatus (req, res) {
        let dados = await global.connection.query(`select * from alarme where status is not null`, { type: QueryTypes.SELECT});
        res.json({dados});
    },
    async loadEquipamentosComandos (req, res) {
        let dados = await global.connection.query(`select * from alarme where comando is not null`, { type: QueryTypes.SELECT});
        res.json({dados});
    },
}