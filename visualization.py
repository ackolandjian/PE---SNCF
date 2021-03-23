import initialize
import qlearning
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def visualize(epsilon_values, nb_episodes):
    x = range(1, len(epsilon_values[0]))
    y=epsilon_values[0][-1]
    plt.bar(x, y)
    plt.show()