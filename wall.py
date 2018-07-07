from mesa import Agent, Model
import random

class WallAgent(Agent):
    """ An agent which represents a static object."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


    def step(self):
        """ Wall agents do not move """
        pass
