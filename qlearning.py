"""
Q Learning algorithm

"""

# Reinforcement Learning briefly is a paradigm of Learning Process in which a learning agent 
# learns, overtime, to behave optimally in a certain environment by interacting continuously 
# in the environment.

# Each timestep, the agent chooses an action, and the environment returns an observation and 
# a reward.


# import libraries
import pandas as pd
import datetime
import json
import csv
import initialize
import torch
import numpy as np

class Qlearning():
    """ This class ... 
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
        self.epsilon_decay = 0.995
        self.nb_episodes = 30
        self.initial_delay = 20
        self.Q_previous = 0
        self.count_skip = 0
           
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
    

    def getResult(self, d1=None,d2=None):
        """
        This function is the primary function of the program, it calls the other functions
        in the right order
        """
        self.validate_datetimes(self)
        self.call_initialize()
        # Define Total number of actions
        self.number_of_actions = 1

    def get_ind(self, nomCourse, ref):
        df = pd.read_csv(self.windowHours_file)
        count = 0
        while df['nomCourse'].iloc[count] != nomCourse and df['ref'].iloc[count] != ref:
            count+=1
        return count

    def get_current_state_ind(self, current_state):
        train, station = list(current_state.keys())[0], s[list(current_state.keys())[0]]
        current_ind = self.get_ind(train, station)
        return current_ind+1
    
    def get_state(self, ind):
        d={}
        df = pd.read_csv(self.windowHours_file)
        train = df['nomCourse'].iloc[ind]
        station = df['ref'].iloc[ind]
        d[train] = station
        return d, train, station
       
    def run_qlearning(self):
        """
        This function run the Q-learning algorithm once the initializations have been done
        """
        cumul_reward_list, actions_list = [], [] 

        for i in range(self.nb_episodes):
            actions = []
            initial_state = self.initial_state
            cumul_reward = 0
            Q = self.Q[index_initial:]

            proba = np.random(0,1)
            index_initial_state = self.get_ind(list(initial_state.keys())[0], initial_state[list(initial_state.keys())[0]])
            current_state = self.get_state(index_initial_state+1)[0]

            if proba<=0:
                Q[0] = reward[initial_state[list(initial_state.keys())[0]]]
            else:
                Q[0]=0

            self.Q_previous = Q[0]
            train_initial = list(current_state.keys())[0]
            nb_stations = self.get_row(train)

            while cumul_reward<self.initial_delay:
                train, station = list(current_state.keys())[0], current_state[list(current_state.keys())[0]]
                ind = self.get_ind(train, station)-index_initial_state

                if train_initial!=train:
                    # create reset_function
                    self.count_skip = 0
                    self.Q_previous = Q[0]
                    train_initial = train
                    nb_stations = self.get_row(train)

                elif nb_stations<=6 or self.count_skip>=int(nb_stations/2):
                    last_ind_before_PSL = ind + nb_stations -1
                    current_state = self.get_state(last_ind_before_PSL+2)
                    train, station = list(current_state.keys())[0], current_state[list(current_state.keys())[0]]
                    # Appeler reset
                 
                x=np.random(0,1)
                if x<=self.epsilon:
                    action = self.randomAction() # Return 0 for stop, 1 for skip
                    # Get reward with ref
                    # reward =
                    if action == 1:
                        self.count_skip+=1
                else:
                    action, reward = self.getMaxValueAction(station) #return 0 for stop, reward[station] for skip
                    if action == 1:
                        self.count_skip+=1
                actions.append(action)

                if reward<0:
                    cumul_reward+=(-reward)
                else:
                    cumul_reward+=reward

                Q[ind] = reward
                self.updateQvalues(Q[ind])
                self.Q_previous = Q[ind]
                current_state = self.get_state(ind+1)
      
        
        actions_list.append(actions)
        cumul_reward_list.append(cumul_reward)





