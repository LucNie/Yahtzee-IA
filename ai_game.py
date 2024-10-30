# API for Yahtzee game

import random


class YahtzeeGame:
    def __init__(self):
        self.dice = [0, 0, 0, 0, 0]
        self.rolls = 0
        self.max_rolls = 3
        self.round = 0
        self.scores = [0] * 13
        self.scoreTaked = [False] * 13

        self.categories = {
            "ones": 0,
            "twos": 0,
            "threes": 0,
            "fours": 0,
            "fives": 0,
            "sixes": 0,
            "three_of_a_kind": 0,
            "four_of_a_kind": 0,
            "full_house": 0,
            "small_straight": 0,
            "large_straight": 0,
            "yahtzee": 0,
            "chance": 0
        }

    def get_dice(self):
        return self.dice
    
    def get_categories_already_scored(self):
        # return a list of booleans indicating which categories have already been scored
        return self.scoreTaked

    def first_roll(self):
        self.dice = [random.randint(1, 6) for _ in range(5)]
        self.rolls = 1
        return self.dice
    
    def reroll(self, dice_to_reroll): # dice_to_reroll is a list of indices of dice to reroll
        if self.rolls == 0:
            return self.first_roll()
        if self.rolls == self.max_rolls:
            return self.dice
        for i in dice_to_reroll:
            self.dice[i] = random.randint(1, 6)
        self.rolls += 1
        return self.dice

    
    
    def choose_ones(self, dice):
        # verifi qu'au moins un dé est égal à 1
        if 1 in dice:
            return sum([1 for die in dice if die == 1])
        return 0
    
    def choose_twos(self, dice):
        if 2 in dice:
            return sum([2 for die in dice if die == 2])
        return 0
    
    def choose_threes(self, dice):
        if 3 in dice:
            return sum([3 for die in dice if die == 3])
        return 0
    
    def choose_fours(self, dice):
        if 4 in dice:
            return sum([4 for die in dice if die == 4])
        return 0
    
    def choose_fives(self, dice):
        if 5 in dice:
            return sum([5 for die in dice if die == 5])
        return 0
    
    def choose_sixes(self, dice):
        if 6 in dice:
            return sum([6 for die in dice if die == 6])
        return 0
    
    def choose_three_of_a_kind(self, dice):
        if len(set(dice)) <= 3:
            return sum(dice)
        return 0
    
    def choose_four_of_a_kind(self, dice):
        if len(set(dice)) <= 2:
            return sum(dice)
        return 0
    
    def choose_full_house(self, dice):
        if len(set(dice)) == 2:
            return 25
        return 0
    
    def choose_small_straight(self, dice):
        if len(set(dice)) >= 4:
            return 30
        return 0
    
    def choose_large_straight(self, dice):
        if len(set(dice)) == 5:
            return 40
        return 0
    
    def choose_yahtzee(self, dice):
        if len(set(dice)) == 1:
            return 50
        return 0
    
    def choose_chance(self, dice):
        return sum(dice)
    
    
    
    def choose_category(self, category, dice): #category is a int from 0 to 12
        match category:
            case 0:
                return self.choose_ones(dice)
            case 1:
                return self.choose_twos(dice)
            case 2:
                return self.choose_threes(dice)
            case 3:
                return self.choose_fours(dice)
            case 4:
                return self.choose_fives(dice)
            case 5:
                return self.choose_sixes(dice)
            case 6:
                return self.choose_three_of_a_kind(dice)
            case 7:
                return self.choose_four_of_a_kind(dice)
            case 8:
                return self.choose_full_house(dice)
            case 9:
                return self.choose_small_straight(dice)
            case 10:
                return self.choose_large_straight(dice)
            case 11:
                return self.choose_yahtzee(dice)
            case 12:
                return self.choose_chance(dice)
            
    def score_category(self, category, dice):
        score = 0
        # vérification si la catégorie est déjà prise
        if self.scoreTaked[category]:
            # alors choisi une au hasard non prise
            for i in range(13):
                if not self.scoreTaked[i]:
                    score = self.choose_category(i, dice)
                    category = i

        else:
            score = self.choose_category(category, dice)

        self.scores[category] = score
        self.scoreTaked[category] = True
        return score
    
    def get_all_scores(self, dice):
        return [self.choose_category(i, dice) for i in range(13)]
    
    def get_score(self, category):
        return self.scores[category]
    
    def get_total_score(self):
        return sum(self.scores)
    
    def get_total_score(self):
        return sum(self.scores)

    def get_round(self):
        return self.round


def play_game():
    return YahtzeeGame()






