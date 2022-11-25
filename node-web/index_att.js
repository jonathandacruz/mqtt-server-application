const express = require("express");
const app = express();

const bodyParse = require("body-parser");
const ComputadorController = require("./controllers/ComputadorController.js");
const IndexController = require("./controllers/IndexController.js");

app.use(bodyParse.json());
app.use(bodyParse.urlencoded({ extended: false }));

app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css'));

app.set("view-engine", "ejs");
app.use(express.static(__dirname + '/public'));

app.get("/", IndexController.loadIndex);

app.get("/consulta_dados", ComputadorController.loadEquipamentosAjax);

app.get("/consulta_logs", ComputadorController.loadEquipamentosLogs);

app.get("/consulta_logs_status", ComputadorController.loadEquipamentosStatus);

app.get("/consulta_logs_comandos", ComputadorController.loadEquipamentosComandos);

app.listen(3000, async () => {
  console.log("Servidor iniciando na porta 3000.");
});