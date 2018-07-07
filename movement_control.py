from mesa import Agent, Model
import random
import numpy as np

def find_empty_location(position, model):
    """ returns a list of surrounding empty locations (x,y) """
    all_cells = model.grid.get_neighborhood(position, moore=True, include_center=True)
    empty_cells = []
    for cell in all_cells:
        if model.grid.is_cell_empty(cell):
            empty_cells.append(cell)
    return empty_cells

def get_distance(grid, pos_1, pos_2):
        """ Get the distance between two point, accounting for toroidal space.
        Args:
            pos_1, pos_2: Coordinate tuples for both points.
            
        adapted from Mesa space.ContinuousSpace
        """
        x1, y1 = pos_1
        x2, y2 = pos_2

        dx = np.abs(x1 - x2)
        dy = np.abs(y1 - y2)

        #looping grid
        dx = min(dx, grid.width - dx)
        dy = min(dy, grid.height - dy)

        return np.sqrt(dx * dx + dy * dy)


def is_greater_x(pos_1, pos_2):
    """ True if position 1 has a bigger x value than position 2"""
    #print("comparing ", pos_1, pos_2)
    return pos_1[0] > pos_2[0]
    
def is_smaller_x(pos_1, pos_2):
    """ True if position 1 has a smaller x value than position 2"""
    #print("comparing ", pos_1, pos_2)
    return pos_1[0] < pos_2[0]
    
def is_greater_y(pos_1, pos_2):
    """ True if position 1 has a bigger y value than position 2"""
    #print("comparing ", pos_1, pos_2)
    return pos_1[1] > pos_2[1]
    
def is_smaller_y(pos_1, pos_2):
    """ True if position 1 has a smaller y value than position 2"""
    #print("comparing ", pos_1, pos_2)
    return pos_1[1] < pos_2[1]

def move_towards(agent, target_pos):
    """ Returns the next position to move to when moving towards target_pos"""
    possible_moves = []
    if target_pos[1] < agent.pos[1]:
        # decrease y position
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]+1, agent.pos[1]-1)))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0], agent.pos[1]-1)))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]-1, agent.pos[1]-1)))
    elif target_pos[1] > agent.pos[1]:
        # see if any free spots in increase y position
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]+1, agent.pos[1]+1)))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0], agent.pos[1]+1)))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]-1, agent.pos[1]+1)))
    elif target_pos[0] < agent.pos[0]:
        # see if free spots in decrease x position
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]-1, agent.pos[1]+1)))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]-1, agent.pos[1])))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]-1, agent.pos[1]-1)))
    elif target_pos[0] > agent.pos[0]:
        # see if any free spots in increase x position
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]+1, agent.pos[1]+1)))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]+1, agent.pos[1])))
        possible_moves.append(agent.model.grid.torus_adj((agent.pos[0]+1, agent.pos[1]-1)))
        
    # Note: some locations may be listed twice, this increases the chances of selection
    # These locations are beneficial in two directions
    empty_locations = [loc for loc in possible_moves if agent.model.grid.is_cell_empty(loc)]
    # randomly choose one of the empty locations
    if empty_locations:
        new_position = random.choice(empty_locations)
        #print(agent.unique_id, " moving towards")
        agent.model.grid.move_agent(agent, new_position)
        
def compute_score(model):
        return model.score
