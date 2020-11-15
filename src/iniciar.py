import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps
from src.correcao import corrigir


def create_app():
    app = Flask(__name__)
    CORS(app, origins=[os.environ['CORS_ALLOW_URL']] )
    app.config["MONGO_URI"]=os.environ['MONGODB_URI']
    mongo = PyMongo(app)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/<path:path>', methods=['GET'])
    #desabilita também os "refreshs"
    def gets(path):
        if path == 'dados':
            resposta = mongo.db.ia.find_one({'tipo':'estatisticas'})
            return dumps(resposta), 200

        return redirect("/static/"+path)

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
        resultado_correcao = corrigir(request.json, mongo)
        mongo.db.resultado.insert_one(resultado_correcao)

        # addicionar nos dados
        return { 'sigla': resultado_correcao['sigla_ia'], 'porcentagem': resultado_correcao['valor_ia']}


    return app