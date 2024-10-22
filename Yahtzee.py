import random
import numpy as np
import tensorflow as tf

class Yahtzee:
    def __init__(self):
        self.dice = [0] * 5  # 5 dés
        self.scorecard = {
            'ones': None,
            'twos': None,
            'threes': None,
            'fours': None,
            'fives': None,
            'sixes': None,
            'three_of_a_kind': None,
            'four_of_a_kind': None,
            'full_house': None,
            'small_straight': None,
            'large_straight': None,
            'yahtzee': None,
            'chance': None
        }
        self.roll_count = 0

    def roll_dice(self, dice_to_reroll=None):
        """Lance les dés. Reroll les dés donnés dans dice_to_reroll (index)."""
        if dice_to_reroll is None:
            dice_to_reroll = [0, 1, 2, 3, 4]  # relance tous les dés par défaut
        for i in dice_to_reroll:
            self.dice[i] = random.randint(1, 6)
        self.roll_count += 1
        print(f'Dés: {self.dice}')

    def reset_rolls(self):
        """Réinitialise le compteur de lancers."""
        self.roll_count = 0

    def choose_score(self, category):
        """Choisir la catégorie où marquer les points."""
        if self.scorecard[category] is not None:
            print("Cette catégorie a déjà été utilisée.")
            return

        if category == 'ones':
            self.scorecard['ones'] = self.dice.count(1) * 1
        elif category == 'twos':
            self.scorecard['twos'] = self.dice.count(2) * 2
        elif category == 'threes':
            self.scorecard['threes'] = self.dice.count(3) * 3
        elif category == 'fours':
            self.scorecard['fours'] = self.dice.count(4) * 4
        elif category == 'fives':
            self.scorecard['fives'] = self.dice.count(5) * 5
        elif category == 'sixes':
            self.scorecard['sixes'] = self.dice.count(6) * 6
        elif category == 'three_of_a_kind':
            if self.has_n_of_a_kind(3):
                self.scorecard['three_of_a_kind'] = sum(self.dice)
            else:
                self.scorecard['three_of_a_kind'] = 0
        elif category == 'four_of_a_kind':
            if self.has_n_of_a_kind(4):
                self.scorecard['four_of_a_kind'] = sum(self.dice)
            else:
                self.scorecard['four_of_a_kind'] = 0
        elif category == 'full_house':
            if self.is_full_house():
                self.scorecard['full_house'] = 25
            else:
                self.scorecard['full_house'] = 0
        elif category == 'small_straight':
            if self.is_small_straight():
                self.scorecard['small_straight'] = 30
            else:
                self.scorecard['small_straight'] = 0
        elif category == 'large_straight':
            if self.is_large_straight():
                self.scorecard['large_straight'] = 40
            else:
                self.scorecard['large_straight'] = 0
        elif category == 'yahtzee':
            if self.has_n_of_a_kind(5):
                self.scorecard['yahtzee'] = 50
            else:
                self.scorecard['yahtzee'] = 0
        elif category == 'chance':
            self.scorecard['chance'] = sum(self.dice)
        print(f'Vous avez choisi {category} avec {self.scorecard[category]} points.')

    def has_n_of_a_kind(self, n):
        """Vérifie si on a n dés identiques."""
        for die_value in set(self.dice):
            if self.dice.count(die_value) >= n:
                return True
        return False

    def is_full_house(self):
        """Vérifie si on a un full house (3 d'une valeur, 2 d'une autre)."""
        unique_counts = set([self.dice.count(i) for i in set(self.dice)])
        return unique_counts == {2, 3}

    def is_small_straight(self):
        """Vérifie si on a une petite suite (4 dés consécutifs)."""
        unique_sorted_dice = sorted(set(self.dice))
        return any([unique_sorted_dice[i:i+4] == list(range(unique_sorted_dice[i], unique_sorted_dice[i]+4)) for i in range(len(unique_sorted_dice)-3)])

    def is_large_straight(self):
        """Vérifie si on a une grande suite (5 dés consécutifs)."""
        unique_sorted_dice = sorted(set(self.dice))
        return unique_sorted_dice in [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]

    def show_scorecard(self):
        """Affiche la feuille de score actuelle."""
        print("\nFeuille de score:")
        for category, score in self.scorecard.items():
            print(f'{category}: {score}')

    def play_turn(self):
        """Simule un tour pour un joueur."""
        self.reset_rolls()
        self.roll_dice()  # Premier lancer
        for _ in range(2):  # Deux relances possibles
            reroll = input("Voulez-vous relancer des dés? Entrez les indices à relancer (ex: 0 1 2) ou 'non' pour garder: ")
            if reroll.lower() == 'non':
                break
            indices = list(map(int, reroll.split()))
            self.roll_dice(indices)
        self.show_scorecard()
        category = input("Choisissez une catégorie pour marquer les points: ")
        self.choose_score(category)

    def total_score(self):
        """Calcule le score total du joueur."""
        return sum(score for score in self.scorecard.values() if score is not None)


class YahtzeeAI:
    def __init__(self, model_path='yahtzee_model.h5'):
        self.model = tf.keras.models.load_model(model_path)

    def choose_action(self, dice):
        """Choisir la meilleure action (catégorie de score) basée sur l'état du jeu."""
        input_data = np.array(dice).reshape(1, -1)  # Préparer les données pour le modèle
        prediction = self.model.predict(input_data)
        return np.argmax(prediction)  # Retourne l'indice de la meilleure catégorie


# Exemple d'utilisation
def main():
    game = Yahtzee()
    ai = YahtzeeAI()
    for _ in range(13):  # 13 tours au total dans le Yahtzee
        print("\nTour du joueur:")
        game.play_turn()  # Tour du joueur

        print("\nTour de l'IA:")
        action = ai.choose_action(game.dice)  # Action de l'IA
        category_name = list(game.scorecard.keys())[action]  # Obtenir le nom de la catégorie à partir de l'indice
        print(f"L'IA choisit la catégorie: {category_name}")
        game.choose_score(category_name)  # IA choisit de marquer des points

    print(f'\nScore final: {game.total_score()}')


if __name__ == "__main__":
    main()
