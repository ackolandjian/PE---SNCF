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
import visualization

def runTheProgram(d1,d2):
    Qlearning_obj = qlearning.Qlearning(d1,d2)
    actions_list, cumul_reward_list, Q_tables, epsilon_values = Qlearning_obj.getResult()
    # visualization.visualize(epsilon_values, Qlearning_obj.nb_episodes)

if __name__ == '__main__':
    try:
        d1 = sys.argv[1]
        d2 = sys.argv[2]
    except:
        print("TRY AGAIN!")
        d1 = 0
        d2 = 0
    runTheProgram(d1,d2)

