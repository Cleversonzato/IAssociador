import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from src.correcao import corrigir

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
CORS(app, origins=[os.environ['CORS_ALLOW_URL']] )
app.config["MONGO_URI"]=os.environ['MONGODB_URI']
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/<path:path>', methods=['GET'])
def default(path):
    partes = path.split('/')

    if partes[-1].endswith('.mp3') or partes[-1].endswith('.ico'):
        print(partes[-1])
        print(url_for('static', filename=partes[-1]))
        return redirect(url_for('static', filename=partes[-1]))

    elif len(partes) > 2:
        url = partes[-2]+'/'+partes[-1]        
        return redirect(url_for('static', filename=url))

    else:
        return render_template('index.html')

@app.route('/perfil', methods=['POST'])
def perfil():
    resposta = mongo.db.perfil.insert_one(request.json)
    return {'teste': str(resposta.inserted_id)}

@app.route('/escolha', methods=['POST'])
def escolha():
   mongo.db.escolha.insert_one(request.json)
   return {'situacao':'sucesso'}

@app.route('/evento', methods=['POST'])
def evento():
    mongo.db.evento.insert_one(request.json)
    return {'situacao':'sucesso'}

@app.route('/resultado', methods=['POST'])
def resultado():
    resultado = corrigir(request.json)
    mongo.db.resultado.insert_one(resultado)
    return { 'sigla': resultado['resultado'] }
