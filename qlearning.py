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
        self.data = []
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
    

    def getResult(self, d1=None,d2=None):
        """
        This function is the primary function of the program, it calls the other functions
        in the right order
        """
        self.validate_datetimes(self)
        self.call_initialize()
        # Define Total number of actions
        self.number_of_actions = 1
    
