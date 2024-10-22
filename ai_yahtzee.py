import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import Adam

class YahtzeeAI:
    def __init__(self):
        self.memory = []
        self.gamma = 0.99  # Taux d'actualisation
        self.epsilon = 1.0  # Taux d'exploration
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32

        # Modèle de réseau de neurones
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=22, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(13, activation='softmax'))  # Choix de catégorie
        model.add(Dense(5, activation='sigmoid'))  # Choix des dés à relancer
        model.add(Dense(1, activation='sigmoid'))  # Continuer à relancer
        model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001))
        return model

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def choose_category_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(13)  # Choix aléatoire
        act_values = self.model.predict(state)
        return np.argmax(act_values[0][:13])  # Choix de catégorie

    def choose_reroll_action(self, state):
        if np.random.rand() <= self.epsilon:
            reroll_choices = [random.choice([0, 1]) for _ in range(5)]  # Choix aléatoire pour chaque dé
            reroll_flag = random.choice([0, 1])  # Choix aléatoire pour continuer à relancer
            return reroll_choices, reroll_flag
        act_values = self.model.predict(state)
        reroll_choices = (act_values[0][13:18] > 0.5).astype(int).tolist()  # Booléens pour relancer
        reroll_flag = 1 if act_values[0][18] > 0.5 else 0  # Booléen pour continuer à relancer
        return reroll_choices, reroll_flag

    def learn(self):
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state in minibatch:
            target = self.model.predict(state)
            print("Shape of target:", target.shape)  # Pour le débogage

            # Vérifiez que l'action est valide
            if 0 <= action < target.shape[1]:
                target[0][action] = reward + self.gamma * np.max(self.model.predict(next_state)[0])
            else:
                print(f"Invalid action: {action}")  # Alerte si l'action n'est pas valide

            self.model.fit(state, target, epochs=1, verbose=0)

    def update_epsilon(self, episode):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

