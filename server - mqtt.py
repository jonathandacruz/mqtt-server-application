import os

import json
import datetime

import psutil
import psycopg2
from _thread import *

from paho.mqtt import client as mqtt_client

#Informaçoes utilizadas para a definição do cliente mqtt
broker = '192.168.88.248'
porta = 1883
topico = "ControleSensor"
topico2 = "ComandosSensor"
client_id = ''
username = ''
password = ''

#Função para a criação do cliente mqtt para dar subscribe no broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conexão com o servidor mqtt feita com sucesso!")
        else:
            print("ERRO AO CONECTAR: %d\n", rc)

    clientmqtt = mqtt_client.Client(client_id)
    clientmqtt.username_pw_set(username, password)
    clientmqtt.on_connect = on_connect
    clientmqtt.connect(broker, porta)
    return clientmqtt

#Função que define o que acontece quando recebe uma mensagem
#no broker responsável por transformar a mensagemem um DICT
# para ser usado na função insert_db_func
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        received = (msg.payload.decode())
        print(msg.topic)
        if(msg.topic == 'ControleSensor'):
            data = {
            "msg": received,
            "destino": 'log'
            }
            insert_db_func(data)
        if(msg.topic == 'ComandosSensor'):
            data = {
            "msg": received,
            "destino": 'comando'
            }
            insert_db_func(data)
    client.subscribe(topico)
    client.subscribe(topico2)
    client.on_message = on_message

#Conexão do cliente mqtt no broker
def mqtt_run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


#Conexão com o banco de dados onde ficam a tabela esp_info
print("Conectando-se a base de dados")
try:
    db_conn = psycopg2.connect("dbname=trabalho host=192.168.88.248 port=5432 user=postgres password=postgres")
    print("Conexão com banco feita com sucesso.")
except:
    print("Não foi possível se conectar com o banco de dados.")
    exit()

#Função para inserir dados recebidos dos clientes no banco de dados
def insert_db_func(data):
    sql = db_conn.cursor()
    data_type = data.get("destino")
    if(data_type == "log"):
        print("Dados recebidos de um sensor.")
        statement = '''INSERT INTO alarme (status, dt_exec) VALUES (valor, 'horario')'''
        statement = statement.replace("valor", data.get("msg"));
        statement = statement.replace("horario", str(datetime.datetime.now()));
    if(data_type == "comando"):
        print("Dados recebidos de um comando.")
        statement = '''INSERT INTO alarme (comando, dt_exec) VALUES (log, 'horario')'''
        statement = statement.replace("log", data.get("msg"));
        statement = statement.replace("horario", str(datetime.datetime.now()));
    try:
        print("Inserindo.")
        sql.execute(statement)
        db_conn.commit()
    except error:
        print(error)
        print("Não foi possível inserir os dados no banco.")

while True:
    mqtt_run()





