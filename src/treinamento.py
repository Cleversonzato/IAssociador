# import pandas as pd 
# import tensorflow as tf

def treinar_opcoes(db):
    db.opcoes_limpinhas.find({})

def treinar_escalas(db):
    pass

def treinar_digitadas(db):
    pass


def treinar(db):  
    try:
        treinar_opcoes(db)
    except Exception:
        pass
    try:
        treinar_escalas(db)
    except Exception:
        pass
    try:
        treinar_digitadas(db)
    except Exception:
        pass