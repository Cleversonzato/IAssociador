import os
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from src.correcao import corrigir

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')
CORS(app, origins=[os.environ['CORS_ALLOW_URL']] )
app.config["MONGO_URI"]=os.environ['MONGODB_URI']
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
@cross_origin(origins='*')
def hello_world():
    return render_template('index.html')

@app.route('/perfil', methods=['POST'])
def perfil():
    resposta = mongo.db.perfil.insert_one(request.json)
    return {'teste': str(resposta.inserted_id)}

@app.route('/evento', methods=['POST'])
def evento():
    mongo.db.evento.insert_one(request.json)
    return {'situacao':'sucesso'}

@app.route('/resultado', methods=['POST'])
def resultado():
    mongo.db.evento.insert_one(request.json)
    resultado = corrigir(request.json)
    return { 'culpado': resultado }
