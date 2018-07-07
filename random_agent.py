from mesa import Agent, Model
import random
import movement_control

class RandomAgent(Agent):
    """ An agent that moves around randomly."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating random agent")

    def step(self):
        print("random agent step")
        self.move()

    def move(self):
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        new_position = random.choice(possible_steps)
        #print(self.unique_id, " moving from ", self.pos, " to ", new_position)
        self.model.grid.move_agent(self, new_position)
        #TODO: remove code after this, for testing
        #print(self.model.grid.get_neighborhood(self.pos, moore = True, include_center = True, radius = 2))
