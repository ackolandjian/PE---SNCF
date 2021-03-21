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
        self.Q = torch.empty([self.number_of_states, self.number_of_actions])
           
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

    def set_initial_state(self):
        """This function sets the initial state (train, station)
        """
        file_content = open(self.windowHours_file)
        reader = csv.reader(file_content)
        self.initial_state[reader[1][0]]=reader[1][1]

    
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
        self.initial_state = self.set_initial_state()
    

    def getResult(self, d1=None,d2=None):
        """
        This function is the primary function of the program, it calls the other functions
        in the right order
        """
        self.validate_datetimes(self)
        self.call_initialize()
        # Define Total number of actions
        self.number_of_actions = 1

       
    def run_qlearning(self, learning_rate=0.2, discount_rate=0.8, egreedy_init=0.7, egreedy_final=0.1):
        """
        This function run the Q-learning algorithm once the initializations have been done
        
        Args:
            learning_rate: float, factor to balance the ratio of action taken based on past
                            experience to current situation
            discount_rate: float, discount on reward
            egreedy: float, start with 70% random actions to explore the environment
            egreedy_final: float
        """

        nb_episodes, steps_total, rewards_total, egreedy_total = 30, [], [], []
