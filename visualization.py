import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns

def find_longest_epsilon_list(n):
    with open('output_files/epsilon_'+str(n)+".csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        m = next(csv_reader)
        for row in csv_reader:
            if len(row)>len(m):
                m=row
    res = [float(i) for i in m]
    return res

def visualize_epsilon(epsilon_list, nb_episodes):
    plt.clf()
    x = range(len(epsilon_list))
    y = epsilon_list
    plt.plot(x, y)
    plt.xlabel("Steps in one episode")
    plt.ylabel("Epsilon")
    plt.savefig('Figures/Epsilon_'+str(nb_episodes)+'.png', dpi = 1200)
    # plt.show()

def visualize_cumul_reward(nb_episodes):
    plt.clf()
    df = pd.read_csv('output_files/cumul_'+str(nb_episodes)+'.csv')
    x=range(len(df))
    y=df.iloc[:,0]
    plt.scatter(x, y, color = 'blue', marker = 'D', s = 10)
    plt.xlabel('Number of episodes')
    plt.ylabel('Cumulative Reward')
    plt.savefig('Figures/Cumul_reward_'+str(nb_episodes)+'.png', dpi = 1200)
    # plt.show()

def visualize_qtable(n):
    plt.clf()
    res=[]

    with open('output_files/Qtables_'+str(n)+".csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        m = next(csv_reader)
    
    for i in range(len(m)):
        res.append(float(m[i].split('[')[1].split(']')[0]))
    
    plt.scatter(range(len(res)), res, color = 'blue', marker = 'D', s = 10)
    plt.xlabel('Steps in one episode')
    plt.ylabel('Value of the Qtable')
    plt.savefig('Figures/Qtable_'+str(n)+'.png', dpi = 1200)
    # plt.show()


def main():
    epsilon = find_longest_epsilon_list(100)
    visualize_epsilon(epsilon, 100)
    visualize_cumul_reward(100)
    visualize_qtable(100)

main()