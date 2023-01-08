import math

import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import eel
import warnings

from constants import *
from DataManagment.file_system import load_file, save_to_file, ensure_dir

pd.options.mode.chained_assignment = None  # Ignores pandas unreasonable future warnings


class StatisticsController:
    STATISTICS_PATH = DATA_PATH / "Statistics"
    GUESSES_DF_PICKLE_PATH = STATISTICS_PATH / "guesses.pickle"
    GUESSES_DF_CSV_PATH = STATISTICS_PATH / "guesses.csv"

    PLOT_DETAIL = 10

    colors = ["#912f40", "#00008B", "#40434E"]
    COLORS = {"article": colors[0], "meaning": colors[1], "english_names": colors[2]}

    def __init__(self):
        if not self.GUESSES_DF_PICKLE_PATH.exists():
            ensure_dir(self.GUESSES_DF_PICKLE_PATH.parent)
            self.guesses_df = pd.DataFrame(columns=["category", "name", "guess", "correct_answer", "is_correct",
                                                    "time"])
            # cast time column to datetime and is_correct to bool
            self.guesses_df["time"] = pd.to_datetime(self.guesses_df["time"])
            self.guesses_df["is_correct"] = self.guesses_df["is_correct"].astype("bool")
            self.save_statistics()

        self.load_statistics()

    def save_statistics(self):
        self.guesses_df.to_pickle(self.GUESSES_DF_PICKLE_PATH)
        self.guesses_df.to_csv(self.GUESSES_DF_CSV_PATH)

    def load_statistics(self):
        self.guesses_df = pd.read_pickle(self.GUESSES_DF_PICKLE_PATH)

    def add_guess(self, category, name, guess, correct_answer, is_correct):
        # save current date and time in time column
        self.guesses_df = pd.concat([self.guesses_df, pd.DataFrame(
            data=[[category, name, guess, correct_answer, is_correct, datetime.now()]],
            columns=["category", "name", "guess", "correct_answer", "is_correct", "time"])])
        self.save_statistics()

    def plot_category_accuracy(self, category: str):
        """
        Plots the accuracy of the guesses for the given category over groups of 20
        sorted by time.
        :param category: which category to plot the accuracy for.
        """
        self.load_statistics()
        category_df = self.guesses_df[self.guesses_df["category"] == category]
        group_size = math.ceil(len(category_df) / self.PLOT_DETAIL)
        if group_size == 0:
            return
        category_df.sort_values(by="time", inplace=True)
        category_df["id"] = range(len(category_df))
        category_df["group"] = category_df["id"] // group_size
        accuracies = category_df.groupby("group").mean(numeric_only=True)["is_correct"]
        accuracies.index *= group_size
        plt.ylim(-0.1, 1.1)
        plt.plot(accuracies, label=category, marker="o", markersize=3, linewidth=1, linestyle="-", alpha=0.75,
                 color=self.COLORS[category])


statistics_controller = StatisticsController()


def get_controller():
    return statistics_controller


@eel.expose
def show_statistics():
    statistics_controller.plot_category_accuracy("article")
    statistics_controller.plot_category_accuracy("meaning")
    statistics_controller.plot_category_accuracy("english_names")
    plt.xlabel("Guesses")
    plt.ylabel("Accuracy")
    plt.title("Accuracy over time")
    plt.gca().yaxis.set_major_formatter(lambda x, pos: f"{x * 100:.0f}%")
    plt.legend(loc="upper left")
    plt.savefig(ACCURACY_PLOT_PATH)
    plt.close()
    return
