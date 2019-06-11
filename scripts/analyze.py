import pandas as pd
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_data_one = "./data/responses_one.csv"
_data_two = "./data/responses_two.csv"

analyzer = SentimentIntensityAnalyzer()


def get_sentiment_score(desc):
    """
    Returns max of positive, negative or neutral sentiment from description data
    """
    scores = analyzer.polarity_scores(desc)
    del scores["compound"]
    return (max(scores, key=scores.get), scores[max(scores, key=scores.get)])


def plot_off_task(df):
    """
    Plots the off task data
    """
    off_task = []
    off_task_sent = []
    not_off_task = []
    not_off_task_sent = []

    for index, row in df.iterrows():
        if row["off_task"] == "Y":
            off_task.append(row["off_task"])
            off_task_sent.append(get_sentiment_score(row["description"]))
        elif row["off_task"] == "N":
            not_off_task.append(row["off_task"])
            not_off_task_sent.append(get_sentiment_score(row["description"]))

    colors_off = []
    for value in off_task_sent:
        if value[0] == "neg":
            colors_off.append("red")
        elif value[0] == "neu":
            colors_off.append("blue")
        elif value[0] == "pos":
            colors_off.append("green")

    colors_not_off = []
    for value in not_off_task_sent:
        if value[0] == "neg":
            colors_not_off.append("red")
        elif value[0] == "neu":
            colors_not_off.append("blue")
        elif value[0] == "pos":
            colors_not_off.append("green")

    plt.title("Mind Wandering Sentiment")
    plt.scatter([val[1] for val in off_task_sent], off_task, color=colors_off)
    plt.scatter(
        [val[1] for val in not_off_task_sent], not_off_task, color=colors_not_off
    )
    plt.ylabel("Off Task?")
    plt.xlabel("Sentiment Confidence %")
    red_patch = mpatches.Patch(color='red', label='Negative Sentiment')
    blue_patch = mpatches.Patch(color='blue', label='Neutral Sentiment')
    green_patch = mpatches.Patch(color='green', label='Positive Sentiment')
    plt.legend(handles=[red_patch, blue_patch, green_patch])
    plt.show()


def plot_valence(df):
    """
    Plots the valence data.

    Don't add data that does not contain numbers
    """
    valence = []
    valence_sentiment = []

    for index, row in df.iterrows():
        val = row["valence"]
        try:
            val = int(val)
        except ValueError:
            continue

        if val > 9:
            continue
        
        valence.append(val)
        valence_sentiment.append(get_sentiment_score(row["description"]))

    colors = []
    for value in valence_sentiment:
        if value[0] == "neg":
            colors.append("red")
        elif value[0] == "neu":
            colors.append("blue")
        elif value[0] == "pos":
            colors.append("green")

    plt.title("Valence Sentiment")
    plt.scatter([val[1] for val in valence_sentiment], valence, color=colors)
    plt.ylabel("Valence (1-9)")
    plt.xlabel("Sentiment Confidence %")
    plt.show()


def plot_arousal(df):
    """
    Plots user arousal data
    """
    arousal = []
    arousal_sentiment = []

    for index, row in df.iterrows():
        val = row["arousal"]
        try:
            val = int(val)
        except ValueError:
            continue

        if val > 9:
            continue
        
        arousal.append(val)
        arousal_sentiment.append(get_sentiment_score(row["description"]))

    colors = []
    for value in arousal_sentiment:
        if value[0] == "neg":
            colors.append("red")
        elif value[0] == "neu":
            colors.append("blue")
        elif value[0] == "pos":
            colors.append("green")

    plt.title("Arousal Sentiment")
    plt.scatter([val[1] for val in arousal_sentiment], arousal, color=colors)
    plt.ylabel("Arousal (1-9)")
    plt.xlabel("Sentiment Confidence %")
    plt.show()


def plot_wandering(df):
    """
    Plot wandering data
    """
    wandering = []
    wandering_sentiment = []

    for index, row in df.iterrows():
        val = row["wandering"]
        try:
            val = int(val)
        except ValueError:
            continue

        if val > 9:
            continue
        
        wandering.append(val)
        wandering_sentiment.append(get_sentiment_score(row["description"]))

    colors = []
    for value in wandering_sentiment:
        if value[0] == "neg":
            colors.append("red")
        elif value[0] == "neu":
            colors.append("blue")
        elif value[0] == "pos":
            colors.append("green")

    plt.title("Wandering Sentiment")
    plt.scatter([val[1] for val in wandering_sentiment], wandering, color=colors)
    plt.ylabel("Wandering (1-6)")
    plt.xlabel("Sentiment Confidence %")
    plt.show()

if __name__ == "__main__":
    df_one = pd.read_csv(_data_one)
    df_two = pd.read_csv(_data_two)

    df = df_one.append([df_two], ignore_index=True)  # concat trial data

    plot_off_task(df)
    plot_valence(df)
    plot_arousal(df)
    plot_wandering(df)