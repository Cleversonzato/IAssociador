import random

def corrigir_opcoes(dados):
    if random.randrange(2) == 1:
        return'vv'
    else:
        return'ff'


def corrigir_escalas(dados):
    if random.randrange(2) == 1:
        return'vf'
    else:
        return 'fv'


def corrigir_digitadas(dados):
    if random.randrange(2) == 1:
        return'vf'
    else:
        return 'fv'


def corrigir(dados):
    if dados['tipo_teste'] == 'opcoes':
        dados['resultado'] = corrigir_opcoes(dados)

    elif dados['tipo_teste'] == 'escalas':
        dados['resultado'] = corrigir_escalas(dados)

    elif dados['tipo_teste'] == 'digitadas':
        dados['resultado'] = corrigir_digitadas(dados)

    return dados
