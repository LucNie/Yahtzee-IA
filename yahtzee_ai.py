import tensorflow as tf
import pandas as pd
import numpy as np

# Chargement des données
data = pd.read_csv('game_data.csv')

# Prétraitement des données
# Convertir les dés en entrées numériques
data['dice'] = data['dice'].apply(lambda x: [int(d) for d in x.strip("[]").split(",")])
X = np.array(data['dice'].tolist())
y = pd.get_dummies(data['score_category']).values

# Création du modèle
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),  # 5 dés comme entrée
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(y[0]), activation='softmax')  # Nombre de catégories de score
])

# Compilation du modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
model.fit(X, y, epochs=10, batch_size=32)

# Sauvegarder le modèle
model.save('yahtzee_model.h5')
print("Modèle entraîné et enregistré sous 'yahtzee_model.h5'.")
