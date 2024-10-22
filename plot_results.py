import matplotlib.pyplot as plt
import pandas as pd

def plot_accuracy(history):
    """Trace la courbe de précision."""
    plt.figure(figsize=(10, 5))
    plt.plot(history['accuracy'], label='Précision (Entraînement)')
    plt.plot(history['val_accuracy'], label='Précision (Validation)')
    plt.title('Précision du modèle')
    plt.xlabel('Époques')
    plt.ylabel('Précision')
    plt.legend()
    plt.grid()
    plt.show()

def plot_total_score(scores):
    """Trace la courbe du score total de l'IA."""
    plt.figure(figsize=(10, 5))
    plt.plot(scores, label='Score total par partie', marker='o')
    plt.title('Score total de l\'IA par partie')
    plt.xlabel('Parties')
    plt.ylabel('Score total')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    # Charger les résultats d'entraînement depuis un fichier CSV (si disponible)
    history_df = pd.read_csv('training_history.csv')
    
    # Charger les scores totaux de l'IA depuis un fichier CSV
    try:
        scores_df = pd.read_csv('ai_scores.csv')  # Remplacez par votre fichier de scores
        scores = scores_df['total_score'].tolist()  # Assurez-vous que votre fichier a cette colonne
    except FileNotFoundError:
        print("Le fichier ai_scores.csv n'a pas été trouvé. Veuillez vérifier.")
        scores = []

    # Plot des résultats
    plot_accuracy(history_df)
    plot_total_score(scores)

if __name__ == "__main__":
    main()
