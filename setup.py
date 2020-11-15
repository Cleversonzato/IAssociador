import os
import pandas as pd
from pymongo import MongoClient
from src.limpeza import limpar
from src.treinamento import treinar
# import nltk  

def get_db():
    mongo = MongoClient(os.environ['MONGODB_URI'])
    return mongo.associador


def iniciar():
    # nltk.download('punkt')
    get_db().ia.insert_one( {"tipo":"estatisticas","opcoes":{"erros":0,"acertos":0},"escalas":{"erros":0,"acertos":0},"digitadas":{"erros":0,"acertos":0}} )
    get_db().ia.insert_one({"tipo":"tempo_ultimos","opcoes":0,"escalas":0,"digitadas":0})

def limpar_dados():
    limpar(db=get_db())

def treinar_ia():
    treinar(db=get_db())
