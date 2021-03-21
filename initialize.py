# -*- coding: utf-8 -*-

"""

"""

# This contains the class Initialize and the subclass InitializeVariables that is created
# 
#
#
#

import csv
import pandas as pd
import json
import datetime
import torch

class Initialize():
    """This is the base class inherited by the subclass InitializeVariables for 
    datetime d1 and d2.
    """
    
    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2
        self.number_of_actions = 0
        self.number_of_states = 0
        self.windowHours_file = 'usefulData/lineJ_windowHours.csv'
        self.reward_QS = {}
        self.reward_RT = {}
        self.reward = {}
        self.Q = torch.empty([self.number_of_states, self.number_of_actions])
        
    def createFileWindowHours(self):
        """This function creates a .csv file containing all trains during a time slot d1-d2
        """
        
        # read Line J preprocessed without P
        with open('usefulData/trains_J_from_psl.json', 'r') as J:
            trains_J = json.load(J)
        # combine all ref ids: origin and destination
        for x in trains_J:
            if int(x['nomCourse']) % 2 != 0:
                origineUtcHoraire = datetime.datetime.strptime(x["origineUtcHoraire"], '%Y-%m-%dT%H:%M:%S.%fZ')
                destinationUtcHoraire = datetime.datetime.strptime(x["destinationUtcHoraire"], '%Y-%m-%dT%H:%M:%S.%fZ')
                if (self.d1 < origineUtcHoraire < self.d2) or (self.d1 < destinationUtcHoraire < self.d2):
                    for jalon in x["pointsJalonnement"]:
                        pointsHoraire = jalon['pointsHoraire']
                        horairePrevu = datetime.datetime.strptime(pointsHoraire[0]['horairePrevu'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        if (self.d1 < horairePrevu < self.d2):
                            if (len(pointsHoraire)!=1):
                                self.data.append([x["nomCourse"],jalon['ref'],pointsHoraire[0]['horairePrevu'],pointsHoraire[1]['horairePrevu'],pointsHoraire[0]['typeHoraire']])
                            else:
                                self.data.append([x["nomCourse"],jalon['ref'],pointsHoraire[0]['horairePrevu'],pointsHoraire[0]['horairePrevu'],pointsHoraire[0]['typeHoraire']])
        # create a dataframe with two columns
        df = pd.DataFrame(self.data, columns=['nomCourse','ref','horairePrevuDepart','horairePrevuArrive','typeHoraire'])
        df.to_csv(self.windowHours_file, index=False)
    
        
    def set_reward(self):
        """ This function sets all the rewards: reward_QS and reward_RT and return the
        total rewards.
        """
        self.reward_RT["P"] = -1.30 # reward on RT if stop is skipped
        self.reward_QS["noP"] = 0 # 0 reward if stop is not skipped
        
        # Find the waiting time per station by looking at refs
        with open('usefulData/WT_from_PSL.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                self.reward_QS[row[0]]=float(row[2])
        
        # Check the time window and find the normalized flow per station
        with open('OD/J_normalized.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                t1,t2= self.get_t1_t2(row[0])
                ref = row[1]
                flow = row[4]
                if (self.d1.time() <= t1 <= self.d2.time()) and (self.d1.time() <= t2 <= self.d2.time()):
                    try:
                        self.reward_QS[ref] = self.reward_QS[ref] * float(flow)     
                    except:
                        pass
                    
        # Calculate the total reward
        for key in self.reward_QS:
            self.reward[key] = self.reward_QS[key] + self.reward_RT["P"]
        
        
    def get_t1_t2(self,time_margin):
        """This function takes the whole time margin and split them into two: t1 and t2.
        It returns t1 & t2 as a time.
        """
        t1 = time_margin[3:11]
        t2 = time_margin[15:23]
        t1 = datetime.datetime.strptime(t1, '%H:%M:%S').time()
        t2 = datetime.datetime.strptime(t2, '%H:%M:%S').time()
        return t1,t2
    
    def get_reward(self):
        return self.reward

    def get_Q(self):
        return self.Q

    def get_number_of_states(self):
        """This function calculates the total number of rows of .csv file and returns it.
        """
        file_content = open(self.windowHours_file)
        reader = csv.reader(file_content)
        return (len(list(reader)) - 1)
    
    def get_number_of_actions(self):
        return self.number_of_actions
        
    def set_variables(self):
        """"This method...
        """
        self.createFileWindowHours()
        self.number_of_states = self.get_number_of_states()
        self.number_of_actions = 1
        self.set_reward()
        self.Q = torch.zeros([self.number_of_states, self.number_of_actions])
