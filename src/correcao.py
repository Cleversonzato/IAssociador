import random
import tensorflow as tf
import pandas as pd
from src import limpeza


def corrigir_opcoes(dados):
    df = limpeza.limpar_opcoes(dados)
    escolha = df['escolha'][0]
    df = df.drop(['escolha'], axis=1)

    model = tf.keras.models.load_model('nn_models/opcoes')
    resultado_ia = float(model.predict(df)[0][0])
      
    if resultado_ia < 0.5:      
        return (str(escolha)+'0', resultado_ia, escolha == 0)
    else:
        return (str(escolha)+'1', resultado_ia, escolha == 1)


def corrigir_escalas(dados):
    df = limpeza.limpar_escalas(dados)
    escolha = df['escolha'][0]
    df = df.drop(['escolha'], axis=1)

    model = tf.keras.models.load_model('nn_models/escalas')
    resultado_ia = float(model.predict(df)[0][0])
      
    if resultado_ia < 0.5:      
        return (str(escolha)+'0', resultado_ia, escolha == 0)
    else:
        return (str(escolha)+'1', resultado_ia, escolha == 1)


def corrigir_digitadas(dados):
    df = limpeza.limpar_digitadas(dados)
    escolha = df['escolha'][0]
    df = df.drop(['escolha'], axis=1)

    model = tf.keras.models.load_model('nn_models/digitadas')
    resultado_ia = float(model.predict(df)[0][0])
      
    if resultado_ia < 0.5:      
        return (str(escolha)+'0', resultado_ia, escolha == 0)
    else:
        return (str(escolha)+'1', resultado_ia, escolha == 1)
        

def corrigir(dados, mongo):
    df_inicial =  pd.json_normalize(dados)
    df_inicial = df_inicial.drop(['id_teste', 'tipo_teste', 'tempo_inicio_milisegundos'], axis=1)
    df_inicial.columns = [name.replace('resultados.', '') for name in df_inicial.columns]
    estatisticas = mongo.db.ia.find_one({'tipo':'estatisticas'})
    tipo = dados['tipo_teste'] 

    if tipo == 'opcoes':
        (sigla, valor_ia, acerto) = corrigir_opcoes(df_inicial)

    elif tipo == 'escalas':
        (sigla, valor_ia, acerto) = corrigir_escalas(df_inicial)

    elif tipo == 'digitadas':
        (sigla, valor_ia, acerto) = corrigir_digitadas(df_inicial)

    if acerto:
        estatisticas[tipo]['acertos'] += 1
    else:
        estatisticas[tipo]['erros'] += 1

    dados['sigla_ia'] = sigla
    dados['valor_ia'] = valor_ia

    estatisticas = mongo.db.ia.replace_one({'tipo':'estatisticas'}, estatisticas)

    return dados
