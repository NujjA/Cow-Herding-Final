import rl_methods
from mesa import Agent, Model
import numpy as np
import random

class TrainedMonteCarloAgent(Agent):
    """ Pretrained Monte Carlo agent
        Must be run with same number of agents as were used for training Q table"""
    
    def __init__(self, unique_id, model, Q_old, vision = None):
        super().__init__(unique_id, model)
        print("creating trained mc agent with vision range ", vision)
        nA = len(rl_methods.action_space)
        self.Q = Q_old # load previous episode Q table
        
        self.vision_range = vision
        self.action = -1


    def step(self):
        print("trained monte carlo step")
        if self.vision_range:
            self.state = rl_methods.encode_state_range(self, self.vision_range) 
        else:
            self.state = rl_methods.encode_state(self.model.grid)
                
        possible_actions = rl_methods.possible_action_space(self)

        if self.state in self.Q:
            self.action = rl_methods.max_action_with_choice(self.Q, self.state, possible_actions) #always a small chance of picking non_greedy to avoid loops
            print("The max action is ", self.action)
            if self.action not in possible_actions:
                self.action = random.choice(possible_actions)
                print("Max action not in possible actions, picking randomly")
        else:
            self.action = random.choice(possible_actions)
            print("I havent seen this before, picking randomly")
            
        
        print("The action I choose is ", rl_methods.action_word(self.action))
        self.move(self.action)

    def move(self,action):
        new_position = rl_methods.action_next_location(self, self.model.grid, action)
        print("Old location ", self.pos, " new position ", new_position)
        self.model.grid.move_agent(self, new_position)

 #   def mc_action_selection(self, possible_steps):
 #       print("I've seen this before")
 #       return rl_methods.select_e_greedy_action(self.Q, self.epsilon, possible_steps, self.state)
        
#    def Q_table_update(self, shared_Q_table = None):
#        """Called by the model at the end of the episode to update the Q table"""        
#        if(shared_Q_table): # If sharing Q table, get the last updated Q table from the team
#            self.Q = shared_Q_table
#        for i in range(len(self.states)): #for each timestep
#            state = self.states[i]
#            action = self.actions[i]
#            reward = 0.0
#            for r in range(i, len(self.rewards)):
#                reward = reward + (self.rewards[r] * self.gamma**i)
#            prev_Q = self.Q[state][action]
#            self.Q[state][action] = prev_Q + (self.alpha * (reward - prev_Q))
#        return self.Q
        
 #   def update_rewards(self, reward):
 #       """Called by the model at the end of the step to get the reward for the current state and action"""
 #       self.rewards.append(float(reward))
