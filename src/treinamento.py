import pandas as pd

def tratar_dados_opcoes(mongo):
    dados = mongo.db.resultado.find({'tipo_teste': 'opcoes'})
    df_inicial =  pd.DataFrame(list(dados))

    df = pd.concat([df_inicial[['id_teste', 'escolha']], pd.json_normalize(df_inicial['resultados'])], axis=1)

    print(df.head())

def treinar_opcoes():
    pass


def iniciar_treinamento(mongo):
    tratar_dados_opcoes(mongo)
    treinar_opcoes()

                   id_teste escolha  tempo_total_milisegundos  palavras.p1.selecaoecao  ...  palavras.p50.selecao  palavras.p50.tempo  palavras.p51.selecao  palavras.p51.tempo
0  5fa9e4815aa9458cc97057a1   pegar                      1544                    False  ...                 False                   0                 False                   0
1  5fad293f19d3bf26a4da2ea2   pegar                      1101                    False  ...                 False                   0                 False                   0
2  5fad204e5a640ebb7bf008b5   pegar                      2864                    False  ...                 False                   0                 False                   0
3  5fad61585234d4d1b12457ca  deixar                     32838                    False  ...                 False                   0                 False                   0
4  5fad61585234d4d1b12457ca   pegar                      2630                    False  ...                 False                   0                 False                   0