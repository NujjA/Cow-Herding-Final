from mesa import Agent, Model, space
import random
import movement_control, cow_methods
import numpy as np

class CowAgent(Agent):
    """ Cow Agent with swarming behavior."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating cow agent")
        
        #stop moving once in goal
        self.herded = False
        
        #how far the cow can see - used in cell weight calculation
        self.cow_visibility = 3
        
        
        # weights based on cows from Multi Agent Programming Contest
        self.COWWEIGHT = 10.0;
        self.EMPTYWEIGHT = 3.0;
        self.CORRALWEIGHT = 3.0;
        self.AGENTWEIGHT = -200.0;
        self.OBSTACLEWEIGHT = -4.0;

    def step(self):
        if(not(self.herded)):
            self.move()
            self.herded = cow_methods.cow_herded(self)
            if(self.herded):
                # take a step back so entrance isn't blocked
                print("COW HERDED COW HERDED COW HERDED COW HERDED COW HERDED ")
                cow_methods.step_back(self)
        #else:
            #print("cow agent herded, not moving")

    def move(self):
        possible_steps = movement_control.find_empty_location(self.pos, self.model)
        
        #select new position based on cow behavior algorithm from Multi Agent Programming Contest
        new_position = self.cow_behavior(possible_steps)

        if (new_position is not None):
            self.model.grid.move_agent(self, new_position)
        
    def cow_behavior(self, possible_steps):
        new_position = None
        #calculate the weights of each cell and list cells with max weight
        best_locations = self.calculate_weights(possible_steps)
        
        #randomly pick from maximum weight cells
        if best_locations:
            new_position = random.choice(best_locations)
        else:
            new_position = self.pos # don't move if there is nowhere to go
        
        return new_position
        
    def calculate_weights(self, possible_steps):
        best_locations = []
        best_score = -np.inf
        for cell in possible_steps:
            cell_weight = self.calculate_single_weight(cell)
            if cell_weight > best_score:
                best_locations = [cell]
                best_score = cell_weight
            elif cell_weight == best_score:
                best_locations.append(cell)
        return best_locations

    def calculate_single_weight(self, cell):
        """ Calculate the weight of cell based on visibility radius"""
        cell_weight = 0.0
        neighborhood_cells = self.model.grid.get_neighborhood(cell, moore=True, include_center=False, radius=self.cow_visibility)
        for neighbor in neighborhood_cells:
            distance = movement_control.get_distance(self.model.grid, cell, neighbor)
            weight = self.get_weight(neighbor)
            cell_weight += (weight/distance)
        return cell_weight
        
    
    def get_weight(self, cell):
        weight = 0.0
        #print("getting weight of ", cell)
        """ get the weight value based on contents of a cell """
        if self.model.grid.is_cell_empty(cell):
            weight = self.EMPTYWEIGHT
        else:
            agent = self.model.grid.get_cell_list_contents(cell)[0]
            weight = cow_methods.determine_weight(agent)
            #print("the cell contains", type(agent))
            #if type(agent) is WallAgent:
            #    weight = self.OBSTACLEWEIGHT
            #if type(agent) is RandomAgent:
            #    weight = self.AGENTWEIGHT
            #if type(agent) is CowAgent:
            #    weight = self.COWWEIGHT
            #if type(agent) is PlanAgent:
            #    weight = self.AGENTWEIGHT
        #print("weight is ", weight)
        return weight
        


    #def calculate_weights(self, possible_cells):
    #    """Return weights as stated in Multi Agent Programming Contest"""
    #    print("cells are ", possible_cells)
    #    
    #    cells_in_view = 
    #    
    #    for cell in possible_cells:
    #        weight = 0
    #        #if empty/corral, weight = 3
    #        if self.model.grid.is_cell_empty(cell):
    #            weight = 3
    #            print("empty cell weight is 3")
    #        else:
    #            agent = self.model.grid.get_cell_list_contents(cell)
    #            print("the cell contains", type(agent))
            #if cow, weight = 10
        #if agent, weight = -200
        #if obstacle, weight = -4
