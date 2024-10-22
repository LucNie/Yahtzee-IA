import numpy as np
import pandas as pd
import random

def generate_game_data(num_games=10000):
    """Génère des données de jeu aléatoires pour entraîner l'IA."""
    data = []
    
    for _ in range(num_games):
        # Simule l'état du jeu
        dice = [random.randint(1, 6) for _ in range(5)]
        score_category = random.choice([
            'ones', 'twos', 'threes', 'fours', 
            'fives', 'sixes', 'three_of_a_kind', 
            'four_of_a_kind', 'full_house', 
            'small_straight', 'large_straight', 
            'yahtzee', 'chance'
        ])
        score = random.randint(0, 50)  # Score aléatoire pour la catégorie choisie

        data.append((dice, score_category, score))

    # Créer un DataFrame pandas
    df = pd.DataFrame(data, columns=['dice', 'score_category', 'score'])
    df.to_csv('game_data.csv', index=False)
    print("Données de jeu générées et enregistrées dans 'game_data.csv'.")

if __name__ == "__main__":
    generate_game_data()
