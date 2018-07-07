from mesa import Agent, Model
import random
import movement_control, rl_methods
import numpy as np
from collections import defaultdict
import copy


class MonteCarloAgent(Agent):
    """ Monte Carlo agent """
    
    def __init__(self, unique_id, model, Q_old, epsilon_ep, gamma = 1, alpha = 0.008, vision = None):
        super().__init__(unique_id, model)
        print("creating monte carlo agent with vision range ", vision)
        nA = len(rl_methods.action_space)
        self.Q = Q_old # load previous episode Q table
        self.epsilon = epsilon_ep # episilon calculated by episode
        self.gamma = gamma
        self.alpha = alpha
        self.states = []
        self.rewards = []
        self.actions = []
        
        self.vision_range = vision
        
        # initialize empty dictionaries of arrays
        #Q = defaultdict(lambda: np.zeros(nA))
        #N = defaultdict(lambda: np.zeros(nA))
        #returns_sum = defaultdict(lambda: np.zeros(env.action_space.n))


    def step(self):
        print("monte carlo step")
        if self.vision_range:
            self.state = rl_methods.encode_state_range(self, self.vision_range) 
            #print(self.state)
        else:
            self.state = rl_methods.encode_state(self.model.grid)
        
        #possible_steps = movement_control.find_empty_location(self.pos, self.model)
        
        possible_actions = rl_methods.possible_action_space(self)
        
        if self.state in self.Q:
            action = self.mc_action_selection(possible_actions)
        else:
            action = random.choice(possible_actions)
            
        #print("selected action ", action, " from ", possible_actions)
        #save state, action
        self.actions.append(action)
        self.states.append(copy.deepcopy(self.state))
        
        self.move(action)

    def move(self,action):
        new_position = rl_methods.action_next_location(self, self.model.grid, action)
        #possible_steps = movement_control.find_empty_location(self.pos, self.model)
        #new_position = random.choice(possible_steps)
        #print(self.unique_id, " moving from ", self.pos, " to ", new_position)
        self.model.grid.move_agent(self, new_position)

    def mc_action_selection(self, possible_steps):
        print("I've seen this before")
        return rl_methods.select_e_greedy_action(self.Q, self.epsilon, possible_steps, self.state)
        
    def Q_table_update(self, shared_Q_table = None):
        """Called by the model at the end of the episode to update the Q table"""
        #N = defaultdict(lambda: np.zeros(nA)) # how many times visit state action pair
        #returns_sum = defaultdict(lambda: np.zeros(env.action_space.n))
        
        if(shared_Q_table): # If sharing Q table, get the last updated Q table from the team
            self.Q = shared_Q_table
        
        for i in range(len(self.states)): #for each timestep
            #state = rl_methods.state_to_tuple(self.states[i])
            state = self.states[i]
            action = self.actions[i]
            #reward = self.rewards[i]
            

            reward = 0.0
            for r in range(i, len(self.rewards)):
                reward = reward + (self.rewards[r] * self.gamma**i)
            #print("reward ", reward)
            #print("state ", state)
            #print("Q[state]" , self.Q[state])
            #print("action ", action)
           
            #print("all rewards", self.rewards)
            #print("prev Q", self.Q[state][action])
            #print("alpha ", self.alpha)
            #print("reward ", reward)
            
                
            
            prev_Q = self.Q[state][action]
            self.Q[state][action] = prev_Q + (self.alpha * (reward - prev_Q))
            #print("next Q", prev_Q + (self.alpha * (reward - prev_Q)))

        return self.Q
        
    def update_rewards(self, reward):
        """Called by the model at the end of the step to get the reward for the current state and action"""
        self.rewards.append(float(reward))
