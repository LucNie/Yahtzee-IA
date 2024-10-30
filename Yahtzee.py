from ai_game import play_game
from ai_yahtzee import get_ia_yahtzee
import numpy as np
import matplotlib.pyplot as plt
import os
MAX_EPISODES = 200
MAX_ROUNDS = 13 # 13 rounds in a game of Yahtzee STATIC
MAX_ROLLS = 3 # 3 rolls per round in Yahtzee STATIC

def InfoGame(bestScore, historyScores, game, episode, round, dice, inputs, outputs):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Episode {episode}")
    print(f"Round {round}")
    print(f"Best score: {bestScore}")
    print(f"History scores: {historyScores}")
    print(f"Game: {game}")
    print(f"Dice: {dice}")
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Scored categories: {game.get_categories_already_scored()}")
    print(f"Scores categories: {game.scores}")

def plot_scores(historyScores):
    plt.plot(historyScores)
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.savefig("yahtzee_scores.png")
    plt.show()

def main():
    print("Starting Yahtzee AI")
    historyScores = []
    bestScore = 0
    ia = get_ia_yahtzee()
    # create model
    print("Creating model")
    ia.create_model()
    
    for episode in range(MAX_EPISODES):
        game = play_game()
        
        for round in range(MAX_ROUNDS):
            # roll dice
            dice = game.first_roll()
            # let AI predict what to do
            inputs = dice + game.get_categories_already_scored() + game.scores + [game.round]
            outputs = ia.predict([inputs])
            
            # reroll dice ?
            while outputs[0][0] < 0.5 and game.rolls < MAX_ROLLS:
                # dice to reroll 1 - 5
                dice_to_reroll = [i for i in range(5) if outputs[0][i + 1] < 0.5]
                dice = game.reroll(dice_to_reroll)
                inputs = dice + game.get_categories_already_scored() + game.scores + [game.round]
                outputs = ia.predict([inputs])

                

            # choose category
            category = np.argmax(outputs[0][6:]) # 6: means we skip the first 6 outputs

            score = game.score_category(category, dice)
            InfoGame(bestScore, historyScores, game, episode, round, dice, inputs, outputs)
            # train model
            ia.train_with_reward(inputs, score)


        # end of game
        print(f"End of game, score: {game.scores[-1]}")
        historyScores.append(game.get_total_score()) # -1 means we get the last score
        if game.get_total_score() > bestScore:
            bestScore = game.get_total_score()
            print(f"New best score: {bestScore}")

    print("Yahtzee AI finished")
    # save ia model
    ia.save("yahtzee_model.h5")
    print("Model saved")
    plot_scores(historyScores)


if __name__ == "__main__":
    main()


    
