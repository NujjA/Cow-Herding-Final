from mesa import Agent, Model
import rl_methods
#import random
#import movement_control
#import numpy as np


class TDAgent(Agent):
    """ Temporal Difference agent """
    
    def __init__(self, unique_id, model, vision_range, alpha, gamma, Q_old):
        super().__init__(unique_id, model)
        print("creating TD agent")
        # take previous w
        self.previousA = None
        self.previousS = None
        self.Aprime = None
        self.Sprime = None
        self.reward = None
        self.vision = vision_range
        self.alpha = alpha
        self.Q = Q_old
        

    def step(self):
        print("TD step")
        # Choose an action A from S using Pi
        # take action A
        
        if(self.previousA):
            # there was a previousA, selectA prime and get Sprime
            # update w            
            self.previousA = self.Aprime
            self.previousS = self.Sprime
            
            self.update_w()
            
            self.Aprime = self.select_action()
            self.Sprime = rl_methods.encode_state_range(self, self.vision)

            pass
        else:
            # there was not a previousA, select first previousA, store first previousS
            self.previousA = self.select_action()
            self.previousS = rl_methods.encode_state_range(self, self.vision)
            pass
            
        self.move()

    def move(self):
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
    def select_action(self):
        return None

    def update_w(self):
        #w = self.alpha * (self.reward + self.gamma
        return None

    def update_TDAgent(self, current_reward):
        ''' called by model at the end of the step '''
        # Observe R
        self.reward = current_reward
