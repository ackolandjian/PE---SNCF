# -*- coding: utf-8 -*-
"""
Q Learning algorithm

"""

# This file contains the Qlearning class which takes two datetimes.
# The getResult() method will call the other methods and print the cumulated rewards and the Q-table.


# import libraries
import datetime
import json
import csv
import initialize
import random
import pandas as pd
import numpy as np

class Qlearning():
    """ This class will call the initialize.py methods and print the obtained result.
    """
    
    def __init__(self, d1=None, d2=None):
        self.d1 = d1
        self.d2 = d2
        self.number_of_actions = 0
        self.number_of_states = 0
        self.initial_state={}
        self.windowHours_file = 'usefulData/lineJ_windowHours.csv'
        self.reward = {}
        self.Q = np.empty([self.number_of_states, self.number_of_actions])
        self.learning_rate = 0.2
        self.discount_rate = 0.8
        self.epsilon = 0.7
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.99
        self.nb_episodes = 50
        self.initial_delay = 30
        self.Q_previous = 0
        self.count_skip = 0
        self.first_train_appearance = 0
        self.current_state = {}
           
    def validate_datetimes(self, d1=None, d2=None):
        validate = 0
        if (type(self.d1) is datetime.date) and (type(self.d2) is datetime.date):
            validate == 2
            return
        if type(self.d1) is not datetime.date:
            self.d1 = str(input("Enter proper d1: "))
            try:
                self.d1 = datetime.datetime.strptime(self.d1,"%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                validate = 1
        if type(self.d2) is not datetime.date:
            self.d2 = str(input("Enter proper d2: "))
            try:
                self.d2 = datetime.datetime.strptime(self.d2,"%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                validate = 1
        if validate == 1:
            self.validate_datetimes()

    
    def call_initialize(self):
        '''Initializes the class object, calls initialize method
        and returns a dictionary containing individual word counts.
        '''

        self.initialize_obj = initialize.Initialize(self.d1, self.d2)
        self.initialize_obj.set_variables()
        self.number_of_states = self.initialize_obj.get_number_of_states()
        self.number_of_actions = self.initialize_obj.get_number_of_actions()
        self.reward = self.initialize_obj.get_reward()
        self.Q = self.initialize_obj.get_Q()
        self.initial_state = self.initialize_obj.get_initial_state()

    def get_ind(self, nomCourse, ref):
        df = pd.read_csv(self.windowHours_file)
        for i in range(len(df)):
            if df['nomCourse'].iloc[i] == nomCourse and df['ref'].iloc[i] == ref:
                return i

    def get_next_PSL(self, ind):
        df= pd.read_csv(self.windowHours_file)
        for i in range(ind, len(df)+1):
            if df['ref'].iloc[i] == 'PR/0087-384008-00':
                return i


    def get_current_state_ind(self, current_state):
        train, station = list(current_state.keys())[0], s[list(current_state.keys())[0]]
        current_ind = self.get_ind(train, station)
        return current_ind+1
    
    def get_state(self, ind):
        """Returns the state thanks to its index"""
        d={}
        df = pd.read_csv(self.windowHours_file)
        train = df['nomCourse'].iloc[ind]
        station = df['ref'].iloc[ind]
        d[train] = station
        return d, train, station

    def get_nb_row(self, train):
        """Returns the number of station served by one train"""
        df = pd.read_csv(self.windowHours_file)
        df2 = df[df['nomCourse']==train]
        return len(df2)

    def get_reward(self, station):
        """ This function returns the reward for skipping a station"""
        return self.reward[station]

    def reset_function(self, Q, train):
        self.count_skip = 0
        self.Q_previous = Q[0]
        train_initial = train
        nb_stations = self.get_nb_row(train)
        return train_initial, nb_stations
    
    def randomAction(self):
        """
        This function returns randomly 0 or 1
        """
        return np.random.randint(2)

    def getMaxValueAction(self, station):
        try:
            reward_if_P = self.get_reward(station)
        except:
            reward_if_P = 0

        reward_if_noP = self.get_reward("noP")

        if reward_if_P<=1:
            return 1, reward_if_P
        else:
            return 0, reward_if_noP

    def updateQvalues(self, q_ind, reward):
        if self.Q_previous !=0:
            self.Q_previous = self.Q_previous + self.learning_rate*(reward + self.discount_rate*max(q_ind, self.Q_previous))


    def run_qlearning(self):
        """
        This function runs the Q-learning algorithm once the initializations have been done
        """
        cumul_reward_list, actions_list, Q_tables, epsilon_values = [], [], [], []

        for i in range(self.nb_episodes):
            actions, cumul_reward, epsilons = [], 0, []

            self.epsilon = 0.7

            initial_state = self.initial_state
            index_initial_state = self.get_ind(list(initial_state.keys())[0], initial_state[list(initial_state.keys())[0]])
            self.first_train_appearance = index_initial_state
    
            Q = self.Q[index_initial_state:]

            proba = random.uniform(-1,1)
            self.current_state = self.get_state(index_initial_state+1)[0]

            if proba<=0:
                Q[0] = self.reward[initial_state[list(initial_state.keys())[0]]]
            else:
                Q[0]=0

            self.Q_previous = Q[0]
            train_initial = list(self.current_state.keys())[0]
            nb_stations = self.get_nb_row(train_initial)

            while cumul_reward<self.initial_delay:
                train, station = list(self.current_state.keys())[0], self.current_state[list(self.current_state.keys())[0]]
                ind = self.get_ind(train, station)

                # If we have changed train ie the current train reached it arrival station
                if train_initial!=train:
                    train_initial, nb_stations = self.reset_function(Q, train)
                    self.first_train_appearance = self.get_ind(train,station)

                # If the limit of the number of stations to delete has been reached,
                # we can't do any other action on this train so we take the next train.
                # If the number of stations served by a train are limited,
                # we can't remove stations so we considered the next train
                elif nb_stations<=6 or self.count_skip>=int(nb_stations/2):
                    last_ind_before_PSL = self.get_next_PSL(ind)-1
                    for j in range(ind, last_ind_before_PSL+1):
                        self.current_state = self.get_state(j)[0]
                        actions.append([self.current_state, 0])
                    self.current_state, train, station = self.get_state(last_ind_before_PSL+2)
                    self.first_train_appearance = self.get_ind(self.get_state(last_ind_before_PSL+1)[1],self.get_state(last_ind_before_PSL+1)[2])
                    train_initial, nb_stations = self.reset_function(Q, train)
                    ind = self.get_ind(train, station)
                
                 
                x=random.random()
                epsilons.append(self.epsilon)
                if x<=self.epsilon:
                    action = self.randomAction() # Return 0 for stop, 1 for skip
                    try:
                        reward = self.get_reward(station) # Get reward with ref station
                    except:
                        reward=0
                    
                else:
                    action, reward = self.getMaxValueAction(station) #return (0,0) for stop, (1,reward[station]) for skip

                if self.epsilon > self.epsilon_min:
                    self.epsilon = self.epsilon*self.epsilon_decay
                
                if action == 1:
                    self.count_skip+=1
                else:
                    reward = 0
                
                actions.append([self.current_state, action])

                if reward<0:
                    reward = -reward
                cumul_reward+=reward

                Q[ind-index_initial_state] = reward
                self.updateQvalues(Q[ind-index_initial_state], reward)
                self.Q_previous = Q[ind-index_initial_state]
                if ind == len(self.Q)-1:
                    break
                else:
                    self.current_state = self.get_state(ind+1)[0]
      
            actions_list.append(actions)
            cumul_reward_list.append(cumul_reward)
            Q_tables.append(Q)
            epsilon_values.append(epsilons)

        return actions_list, cumul_reward_list, Q_tables, epsilon_values

    def getResult(self, d1=None,d2=None):
        """
        This method is the primary function of the program and does the work of calling the required
        methods of the class in the correct order to get the cumulated reward and the Q-table.
        If two datetimes are passed to this class, the first step of this method is to validate the format of 
        these datetimes.
        """
        self.validate_datetimes(self)
        self.call_initialize()
        # Define Total number of actions
        self.number_of_actions = 1
        # runQlearning here
        actions_list, cumul_reward_list, Q_tables, epsilon_values = self.run_qlearning()
        return actions_list, cumul_reward_list, Q_tables, epsilon_values


