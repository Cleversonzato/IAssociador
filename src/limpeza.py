""" Anotações sobre dados:
pegar o ouro = 0
deixar = 1
"""
import os
import pandas as pd
from pymongo import MongoClient
# from nltk import tokenize    

def tratar_dados_opcoes(ultimos_mili, db):
    opcoes = db.resultado.find({'tipo_teste': 'opcoes', 'tempo_inicio_milisegundos': {'$gt': ultimos_mili['opcoes']} })
    df_inicial =  pd.DataFrame(list(opcoes))
    df = pd.concat([df_inicial[['id_teste', 'escolha']], pd.json_normalize(df_inicial['resultados'])], axis=1)

    cols_tempo = [nome for nome in df.columns if '.tempo' in nome]
    cols_selecao = [nome for nome in df.columns if '.selecao' in nome]
    df[cols_selecao] = df[cols_selecao].apply(lambda x: x.replace(True, 1).replace(False, 0), axis=1)
    df[cols_tempo] = df.apply(lambda x:  x[cols_tempo] / x['tempo_total_milisegundos'], axis=1 )
    # 20 minutos me parece um bom tempo "máximo"
    df['tempo_total_milisegundos'] = df['tempo_total_milisegundos'] / 1200000
    df['escolha'] = df['escolha'].replace('pegar', int(1)).replace('deixar', int(0))
    df.columns = [name.replace('palavras.', '').replace('.', '_') for name in df.columns]
    db.opcoes_limpinhas.insert_many(df.to_dict("records"))
    ultimos_mili['opcoes'] = int(df_inicial['tempo_inicio_milisegundos'].max())
    db.ia.update({'tipo':'tempo_ultimos'}, ultimos_mili)



def tratar_dados_escalas(ultimos_mili, db):
    escalas = db.resultado.find({'tipo_teste': 'escalas', 'tempo_inicio_milisegundos': {'$gt': ultimos_mili['escalas']} })
    df_inicial =  pd.DataFrame(list(escalas))
    df = pd.concat([df_inicial[['id_teste', 'escolha']], pd.json_normalize(df_inicial['resultados'])], axis=1)

    cols_tempo = [nome for nome in df.columns if '.tempo' in nome]
    cols_valor = [nome for nome in df.columns if '.valor' in nome]
    df[cols_valor] = df[cols_valor].apply(lambda x: x[cols_valor] / 100, axis=1 ) 
    df[cols_tempo] = df.apply(lambda x:  x[cols_tempo] / x['tempo_total_milisegundos'], axis=1 )
    # 20 minutos me parece um bom tempo "máximo"
    df['tempo_total_milisegundos'] = df['tempo_total_milisegundos'] / 1200000
    df['escolha'] = df['escolha'].replace('pegar', int(1)).replace('deixar', int(0))
    df.columns = [name.replace('palavras.', '').replace('.', '_') for name in df.columns]
    db.escalas_limpinhas.insert_many(df.to_dict("records"))
    ultimos_mili['escalas'] = int(df_inicial['tempo_inicio_milisegundos'].max())
    db.ia.update({'tipo':'tempo_ultimos'}, ultimos_mili)


def tratar_dados_digitadas(ultimos_mili, db):
    digitadas = db.resultado.find({'tipo_teste': 'digitadas', 'tempo_inicio_milisegundos': {'$gt': ultimos_mili['digitadas']} })
    df_inicial =  pd.DataFrame(list(digitadas))    
    df = pd.concat([df_inicial[['id_teste', 'escolha']], pd.json_normalize(df_inicial['resultados'])], axis=1)

    cols_tempo = [nome for nome in df.columns if '.tempo' in nome]
    #esperar mais palavras antes de analizar algo sobre

    df[cols_tempo] = df.apply(lambda x:  x[cols_tempo] / x['tempo_total_milisegundos'], axis=1 )
    # 20 minutos me parece um bom tempo "máximo"
    df['tempo_total_milisegundos'] = df['tempo_total_milisegundos'] / 1200000
    df['escolha'] = df['escolha'].replace('pegar', int(1)).replace('deixar', int(0))
    df.columns = [name.replace('palavras.', '').replace('.', '_') for name in df.columns]
    db.digitadas_limpinhas.insert_many(df.to_dict("records"))
    ultimos_mili['digitadas'] = int(df_inicial['tempo_inicio_milisegundos'].max())
    db.ia.update({'tipo':'tempo_ultimos'}, ultimos_mili)


def limpar(db):
    ultimos_mili = db.ia.find_one({'tipo':'tempo_ultimos'})

    try:
        tratar_dados_opcoes(ultimos_mili, db)
    except Exception:
        pass
    try:
        tratar_dados_escalas(ultimos_mili, db)
    except Exception:
        pass
    try:
        tratar_dados_digitadas(ultimos_mili, db)
    except Exception:
        pass
