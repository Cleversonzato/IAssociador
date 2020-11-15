import pandas as pd 
import tensorflow as tf

def treinar_opcoes(db):
    dados = pd.DataFrame(list(db.opcoes_limpinhas.find({})))
    dados = dados.drop(['_id', 'id_teste'], axis=1)
    escolha = dados.pop('escolha')

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(103, activation='softmax'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(50, activation='softmax'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax'),  
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',  loss='binary_crossentropy',  metrics=['accuracy'])
    model.fit(dados, escolha, validation_split=0.3, epochs=3)
    model.save('nn_models/opcoes')


def treinar_escalas(db):
    dados = pd.DataFrame(list(db.escalas_limpinhas.find({})))
    dados = dados.drop(['_id', 'id_teste'], axis=1)
    escolha = dados.pop('escolha')

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(41, activation='softmax'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(20, activation='softmax'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(5, activation='softmax'),  
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy',  metrics=['accuracy'])
    model.fit(dados, escolha, validation_split=0.3, epochs=3)
    model.save('nn_models/escalas')

def treinar_digitadas(db):
    dados = pd.DataFrame(list(db.digitadas_limpinhas.find({})))
    dados = dados.drop(['_id', 'id_teste'], axis=1)
    escolha = dados.pop('escolha')

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(19, activation='softmax'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',  loss='binary_crossentropy',  metrics=['accuracy'])
    model.fit(dados, escolha, validation_split=0.3, epochs=3)
    model.save('nn_models/digitadas')


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