import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

def find_longest_epsilon_list(n):
    with open('output_files/epsilon_'+str(n)+".csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            print(len(row), row)

def visualize(epsilon_values):
    x = range(1, len(epsilon_values))
    y=epsilon_values
    plt.bar(x, y)
    plt.show()

def main():
    find_longest_epsilon_list(100)

main()