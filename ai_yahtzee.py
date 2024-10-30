import tensorflow as tf
from tensorflow.keras.models import Sequential
from keras.optimizers import Adam
from tensorflow.keras.layers import Dense, LSTM, Input, BatchNormalization, Dropout
import numpy as np
import random


class ReplayMemory:
    def __init__(self, max_size):
        self.memory = []
        self.max_size = max_size

    def add(self, experience):
        # Ajouter une nouvelle expérience
        if len(self.memory) >= self.max_size:
            self.memory.pop(0)  # Supprimer la plus ancienne expérience
        self.memory.append(experience)

    def sample(self, batch_size):
        # Échantillonner un lot d'expériences
        return random.sample(self.memory, min(batch_size, len(self.memory)))

    def size(self):
        return len(self.memory)

class YahtzeeAI:
    def __init__(self, replay_memory_size=1000):
        self.model = self.create_model()
        self.best_score = 0
        self.replay_memory = ReplayMemory(max_size=replay_memory_size)

    def create_model(self):
        # Define model architecture
        model = Sequential([
            Input(shape=(32,)), # 5 dice values + 13 booleans + 13 scores + 1 round = 32 inputs
            Dense(128, activation='relu'),  # Augmenté pour mieux capturer les combinaisons
            # BatchNormalization(),  # Normalisation pour aider à la stabilité de l'apprentissage
            Dropout(0.2),  # Dropout pour éviter le surapprentissage
            Dense(64, activation='relu'),
            Dense(64, activation='relu'),
            Dense(19, activation='softmax')  # 1 roll vs category, 5 dice reroll indicators, 13 category scores
        ])
        # Compile model
        model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    

    def train(self, inputs, outputs, epochs=10,reward=0):
        # Convert inputs and outputs to numpy arrays
        inputs = np.array(inputs, dtype=np.float32)  # Ensure inputs are a NumPy array of type float32
        outputs = np.array(outputs, dtype=np.float32)  # Ensure outputs are a NumPy array of type float32
        print("Shape of inputs:", inputs.shape)
        print("Shape of outputs:", outputs.shape)
        self.model.fit(inputs, outputs, epochs=epochs)

    def save(self, filename):
        self.model.save(filename)

    def load(self, filename):
        self.model = tf.keras.models.load_model(filename)
        
    def predict(self, inputs):
        # Ensure input is a NumPy array
        inputs = np.array(inputs, dtype=np.float32)
        return self.model.predict(inputs) # Return the model's prediction 1 roll vs category, 5 dice reroll indicators, 13 category scores
    
    def evaluate_score(self, final_score):
        """Evaluate the score and update the model based on rewards."""
        reward = 0

        # Compare with the best score
        if final_score > self.best_score:
            reward = 1  # Reward for improvement
            self.best_score = final_score  # Update best score
            print(f"New best score: {final_score}")
        else:
            reward = -1  # Punishment for not improving
            print(f"Score did not improve: {final_score}")

        return reward

    def train_with_reward(self, inputs, score , epochs=10):
        """Entraîner le modèle avec une récompense basée sur le score final."""
        # Évaluer le score
        if score == 0:
            reward = -0.1
        else:
            reward = self.evaluate_score(score)
            

        # Créer les outputs avec la récompense
        outputs = np.zeros((19), dtype=np.float32)
        action_index = 0
        outputs[action_index] = reward

        if action_index == 0:
            outputs[1] = 1

        # Ajouter l'expérience à la mémoire de replay
        self.replay_memory.add((inputs, outputs))

        # Si la mémoire contient suffisamment d'expériences, entraînez le modèle
        if self.replay_memory.size() > 32:  # Par exemple, utilisez un lot de 32
            batch = self.replay_memory.sample(32)
            batch_inputs, batch_outputs = zip(*batch)
            print(f"batch_outputs: {np.array(batch_outputs).shape}")
            self.train(np.array(batch_inputs), np.array(batch_outputs), epochs)
        
        
    
def get_ia_yahtzee():
    return YahtzeeAI()