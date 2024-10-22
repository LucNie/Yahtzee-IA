import random
import numpy as np
from ai_yahtzee import YahtzeeAI
from matplotlib import pyplot as plt

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
            dice_to_reroll = [0, 1, 2, 3, 4]  # Relance tous les dés par défaut
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
            return 0  # Catégorie déjà utilisée

        score = 0
        if category == 'ones':
            score = self.dice.count(1) * 1
        elif category == 'twos':
            score = self.dice.count(2) * 2
        elif category == 'threes':
            score = self.dice.count(3) * 3
        elif category == 'fours':
            score = self.dice.count(4) * 4
        elif category == 'fives':
            score = self.dice.count(5) * 5
        elif category == 'sixes':
            score = self.dice.count(6) * 6
        elif category == 'three_of_a_kind':
            if self.has_n_of_a_kind(3):
                score = sum(self.dice)
        elif category == 'four_of_a_kind':
            if self.has_n_of_a_kind(4):
                score = sum(self.dice)
        elif category == 'full_house':
            if self.is_full_house():
                score = 25
        elif category == 'small_straight':
            if self.is_small_straight():
                score = 30
        elif category == 'large_straight':
            if self.is_large_straight():
                score = 40
        elif category == 'yahtzee':
            if self.has_n_of_a_kind(5):
                score = 50
        elif category == 'chance':
            score = sum(self.dice)

        self.scorecard[category] = score
        print(f'Catégorie: {category}, Score: {score}')
        return score

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

    def total_score(self):
        """Calcule le score total du joueur."""
        return sum(score for score in self.scorecard.values() if score is not None)

def main():
    ai = YahtzeeAI()
    game = Yahtzee()
    score = []

    for episode in range(25):  # Nombre de parties à jouer
        game.reset_rolls()
        state = np.zeros(22)  # État initial (modifié)
        total_reward = 0  # Récompense totale pour l'épisode

        for turn in range(13):  # 13 tours dans le Yahtzee
            game.roll_dice()  # Lancer les dés
            available_categories = list(game.scorecard.keys())  # Actions disponibles

            category_choice = ai.choose_category_action(state.reshape(1, 22))  # Choisir une catégorie (action) ou relancer
            print(f'IA choisit: {available_categories[category_choice]}')

            # si l'ia a choisi de relancer les dés 
            if available_categories[category_choice] in ['reroll', 'continue']: # Relancer les dés
                reroll_choices, reroll_flag = ai.choose_reroll_action(state.reshape(1, 22)) # Choix de dés à relancer
                print(f'IA choisit de relancer: {reroll_choices}, Continuer à relancer: {reroll_flag}') # Afficher les choix de l'IA
                game.roll_dice([i for i, choice in enumerate(reroll_choices) if choice == 1]) # Relancer les dés choisis
                state[13:18] = reroll_choices # Mettre à jour l'état
                state[18] = reroll_flag # Mettre à jour l'état 
                # baisse le tours de 1 pour que l'ia ne choisisse pas de catégorie
                turn -= 1
                continue

            # Vérifier si la catégorie a déjà un score
            if game.scorecard[available_categories[category_choice]] is not None:
                # Choisir une catégorie aléatoire non utilisée
                available_categories.remove(available_categories[category_choice])
                if available_categories:
                    category_choice = random.choice(range(len(available_categories)))
                else:
                    print("Toutes les catégories sont utilisées.")
                    break

            reward = game.choose_score(available_categories[category_choice])  # Obtenir la récompense
            next_state = np.zeros(22)  # État suivant (modifié)
            total_reward += reward

            ai.remember(state.reshape(1, 22), category_choice, reward, next_state.reshape(1, 22))  # Mémoriser l'expérience
            state = next_state  # Mettre à jour l'état


        
        ai.learn()  # Entraîner l'IA
        ai.update_epsilon(episode)
        print(f'Partie {episode + 1}, Score total: {game.total_score()}, Récompense totale: {total_reward}')
        score.append(game.total_score())

        # reset le scorecard pour la prochaine partie
        game.scorecard = {k: None for k in game.scorecard.keys()}

    # crée un graphique du score total par partie
    plt.figure(figsize=(10, 5))
    plt.plot(score, label='Score total par partie', marker='o')
    plt.title('Score total de l\'IA par partie')
    plt.xlabel('Parties')
    plt.ylabel('Score total')
    plt.legend()
    plt.grid()
    # sauvegarde "Last_game_score_graph.png"
    plt.savefig('Last_game_score_graph.png')
    plt.show()



if __name__ == "__main__":
    main()
