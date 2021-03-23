import initialize
import qlearning
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns


def visualize(epsilon_values, nb_episodes):
    x = range(1, nb_episodes+1)
    y=[epsilon_values[i][-1] for i in range(len(epsilon_values))]
    plt.bar(x, y)
    plt.show()