# -*- coding: utf-8 -*-
"""
@authors: Anna Christiane and Clarisse
"""

# This program uses the Q-learning approach for train rescheduling. 
# It prints the cumulated rewards and the Q-table.

# Run this program from the command line as
# $ python3 run.py

import qlearning
import sys
import pandas as pd
import csv

def clean_lists(action, cumul_reward, qtables, epsilon):
    """
    This function removes the episodes where only one action had been taken
    """
    for ele in action:
        if len(ele)==1:
            index = action.index(ele)
            action.remove(ele)
            del qtables[index]
            del cumul_reward[index]
            del epsilon[index]
    return action, cumul_reward, qtables, epsilon

# The functions below save the lists returned by run_qlearning
def write_in_files(name, a_list):
    with open(name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(a_list)

def save_action(l, nb_episodes):
    name_file= "output_files/actions_"+str(nb_episodes)+".csv"
    write_in_files(name_file, l)

def save_Qtables(l, nb_episodes):
    name_file= "output_files/Qtables_"+str(nb_episodes)+".csv"
    write_in_files(name_file, l)

def save_epsilon(l, nb_episodes):
    name_file= "output_files/epsilon_"+str(nb_episodes)+".csv"
    write_in_files(name_file, l)

def save_cumul(l, nb_episodes):
    name_file = "output_files/cumul_"+str(nb_episodes)+".csv"
    df = pd.DataFrame(l)
    df.to_csv(name_file, sep=',', index=False)
    
def runTheProgram(d1,d2):
    Qlearning_obj = qlearning.Qlearning(d1,d2)
    actions_list, cumul_reward_list, Q_tables, epsilon_values = Qlearning_obj.getResult()
    actions_list, cumul_reward_list, Q_tables, epsilon_values = clean_lists(actions_list, cumul_reward_list, Q_tables, epsilon_values)
    save_action(actions_list, Qlearning_obj.nb_episodes)
    save_Qtables(Q_tables, Qlearning_obj.nb_episodes)
    save_epsilon(epsilon_values, Qlearning_obj.nb_episodes)
    save_cumul(cumul_reward_list, Qlearning_obj.nb_episodes)

if __name__ == '__main__':
    try:
        d1 = sys.argv[1]
        d2 = sys.argv[2]
    except:
        print("TRY AGAIN!")
        d1 = 0
        d2 = 0
    runTheProgram(d1,d2)

