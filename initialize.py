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

class Initialize():
    """This is the base class inherited by the subclass InitializeVariables for 
    datetime d1 and d2.
    """
    
    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2
        self.number_of_actions = 0
        self.number_of_states = 0
        self.data = []
        self.windowHours_file = 'usefulData/lineJ_windowHours.csv'
        self.reward_QS = {}
        self.reward_RT = {}
        self.reward = {}
        
    def createFileWindowHours(self):
        """This function creates a .csv file containing all trains during a time slot d1-d2
        """
        
        # read Line J preprocessed without P
        with open('usefulData/trains_J_from_psl.json', 'r') as J:
            trains_J = json.load(J)
        # combine all ref ids: origin and destination
        for x in trains_J:
            print(x['nomCourse'])
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
        self.reward_RT["P"] = -1.30 #reward on RT if stop is skipped
        
        # self.reward_QS["P"] dict avec les ids des stations et leur flux 
        
        self.reward["noP"] = 0 # noP pour les deux rewards
        # compare csv ref values and find their attributes
        with open('usefulData/WT_from_PSL.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                self.reward[row[0]]=float(row[2])
        
        for key in self.reward:
            self.reward[key] = self.reward[key] + self.reward_RT["P"]
            print(key, "corresponds to:", self.reward[key])
        
    def get_reward(self):
        return self.reward

    def get_number_of_states(self):
        """This function calculates the total number of rows of .csv file and returns it.
        """
        file_content = open(self.windowHours_file)
        reader = csv.reader(file_content)
        return (len(list(reader)) - 1)
    
        
    def set_variables(self):
        """"This method...
        """
        # Create the file .csv containing all trains during a time slot d1-d2
        self.createFileWindowHours()
        self.number_of_states = self.get_number_of_states()
        self.set_reward()
        #print(self.number_of_states)
